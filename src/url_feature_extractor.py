"""
Modul Ekstraktor Fitur Leksikal dan Struktural URL (Security-Hardened Version)
Nama Sistem: PhishGuard AI
Tujuan: Mengekstrak 16 fitur leksikal dan struktural secara offline murni tanpa network socket.
Proteksi Keamanan:
 - Mencegah SSRF: Tidak pernah melakukan HTTP/socket connection ke URL target.
 - Mencegah ReDoS: Membatasi panjang string input dan menggunakan regex non-backtracking.
"""

import math
import re
from urllib.parse import urlparse
from typing import Dict, Any

POPULAR_TLDS = {'com', 'org', 'net', 'edu', 'gov', 'mil', 'int'}
SUSPICIOUS_EXTENSIONS = {'.exe', '.zip', '.rar', '.7z', '.apk', '.bin', '.scr', '.vbs', '.bat', '.cmd', '.php', '.js'}
MAX_URL_LENGTH = 2048

def calculate_shannon_entropy(text: str) -> float:
    """Menghitung Shannon Entropy dari string URL tanpa komputasi eksponensial."""
    if not text:
        return 0.0
    text_len = len(text)
    prob = [float(text.count(c)) / text_len for c in set(text)]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return float(round(entropy, 6))

def extract_features_from_url(url: str) -> Dict[str, Any]:
    """
    Mengekstrak 16 fitur leksikal dan struktural dari satu string URL mentah.
    Aman dari SSRF: Diproses murni secara offline (string parsing & math).
    """
    # 1. Sanitasi batas panjang input (Mitigasi ReDoS / Memory Exhaustion)
    url_str = str(url).strip()[:MAX_URL_LENGTH]
    
    # 2. Parsing URL secara statis (Tanpa koneksi jaringan)
    if not url_str.startswith(('http://', 'https://')):
        url_parsed = urlparse('http://' + url_str)
    else:
        url_parsed = urlparse(url_str)
        
    netloc = url_parsed.netloc.lower()
    path = url_parsed.path
    query = url_parsed.query
    
    # Fitur 1: url_length
    url_length = len(url_str)
    
    # Fitur 2: has_ip_address (Linear regex tanpa catastrophic backtracking)
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?$'
    has_ip_address = 1 if re.match(ip_pattern, netloc) else 0
    
    # Fitur 3: dot_count
    dot_count = url_str.count('.')
    
    # Fitur 4: https_flag
    https_flag = 1 if url_str.lower().startswith('https://') else 0
    
    # Fitur 5: url_entropy
    url_entropy = calculate_shannon_entropy(url_str)
    
    # Fitur 6: token_count (Split linier)
    tokens = [t for t in re.split(r'[:/?&=._-]', url_str) if t]
    token_count = len(tokens)
    
    # Fitur 7: subdomain_count
    domain_parts = netloc.split('.')
    if len(domain_parts) > 2:
        subdomain_count = len(domain_parts) - 2
    else:
        subdomain_count = 0
        
    # Fitur 8: query_param_count
    query_param_count = len(query.split('&')) if query else 1
    
    # Fitur 9: tld_length & Fitur 10: path_length
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""
    tld_length = len(tld)
    path_length = len(path)
    
    # Fitur 11: has_hyphen_in_domain
    has_hyphen_in_domain = 1 if '-' in netloc else 0
    
    # Fitur 12: number_of_digits
    number_of_digits = sum(c.isdigit() for c in url_str)
    
    # Fitur 13: tld_popularity
    tld_popularity = 1 if tld.lower() in POPULAR_TLDS else 0
    
    # Fitur 14: suspicious_file_extension
    suspicious_file_extension = 1 if any(path.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS) else 0
    
    # Fitur 15: domain_name_length
    domain_name = domain_parts[-2] if len(domain_parts) >= 2 else (domain_parts[0] if domain_parts else "")
    domain_name_length = len(domain_name)
    
    # Fitur 16: percentage_numeric_chars
    percentage_numeric_chars = (number_of_digits / url_length * 100.0) if url_length > 0 else 0.0
    
    return {
        'url_length': int(url_length),
        'has_ip_address': int(has_ip_address),
        'dot_count': int(dot_count),
        'https_flag': int(https_flag),
        'url_entropy': float(url_entropy),
        'token_count': int(token_count),
        'subdomain_count': int(subdomain_count),
        'query_param_count': int(query_param_count),
        'tld_length': int(tld_length),
        'path_length': int(path_length),
        'has_hyphen_in_domain': int(has_hyphen_in_domain),
        'number_of_digits': int(number_of_digits),
        'tld_popularity': int(tld_popularity),
        'suspicious_file_extension': int(suspicious_file_extension),
        'domain_name_length': int(domain_name_length),
        'percentage_numeric_chars': float(round(percentage_numeric_chars, 6))
    }
