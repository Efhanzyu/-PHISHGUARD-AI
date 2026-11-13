"""
Script pengujian startup server Streamlit
"""
import subprocess
import time
import urllib.request
import sys

def test_streamlit():
    print("Memulai proses Streamlit...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(5)
    success = False
    try:
        req = urllib.request.urlopen("http://localhost:8501", timeout=5)
        print("STREAMLIT STATUS CODE:", req.getcode())
        if req.getcode() == 200:
            success = True
            print("STREAMLIT SERVER TEST: PASS (200 OK)")
    except Exception as e:
        print("STREAMLIT PROBE FAILED:", e)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    test_streamlit()

