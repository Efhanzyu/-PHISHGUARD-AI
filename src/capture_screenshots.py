"""
Skrip otomatis pengambilan screenshot antarmuka PhishGuard AI Redesign
"""
import subprocess
import time
import os
import tempfile

def capture_redesign_pages():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    out_dir = r"E:\01. Matkul\Semester 5\01. KI\UAS\reports\screenshots\redesign"
    os.makedirs(out_dir, exist_ok=True)
    temp_profile = os.path.join(tempfile.gettempdir(), "chrome_cap_prof_redesign")
    
    pages = [
        ("01_intelligence_core_topology.png", "http://localhost:8505/?page=overview"),
        ("02_single_url_scanner.png", "http://localhost:8505/?page=single"),
        ("03_batch_threat_triage.png", "http://localhost:8505/?page=batch"),
        ("04_analytics_validation.png", "http://localhost:8505/?page=eval"),
        ("05_neural_architecture.png", "http://localhost:8505/?page=spec"),
        ("06_defensive_protocol.png", "http://localhost:8505/?page=guide"),
    ]
    
    for filename, url in pages:
        out_file = os.path.join(out_dir, filename)
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--virtual-time-budget=2000",
            "--hide-scrollbars",
            f"--user-data-dir={temp_profile}",
            "--window-size=1400,900",
            f"--screenshot={out_file}",
            url
        ]
        print(f"Capturing: {filename} from {url}...")
        try:
            res = subprocess.run(cmd, capture_output=True, timeout=12)
            print(f" -> Status: {os.path.exists(out_file)} ({os.path.getsize(out_file) if os.path.exists(out_file) else 0:,} bytes)")
        except Exception as e:
            print(f" -> Timeout/Error capturing {filename}: {e}")

if __name__ == "__main__":
    capture_redesign_pages()
