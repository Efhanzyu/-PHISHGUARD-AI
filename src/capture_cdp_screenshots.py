import asyncio
import json
import base64
import os
import subprocess
import tempfile
import urllib.request
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9222

async def capture_page(target_url, output_path, wait_time=4):
    # Get tab list
    req = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")
    tabs = json.loads(req.read().decode())
    ws_url = tabs[0]["webSocketDebuggerUrl"]

    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Navigate
        await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": target_url}}))
        # Wait for Streamlit to render
        await asyncio.sleep(wait_time)
        # Capture screenshot
        await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        
        while True:
            resp = json.loads(await ws.recv())
            if resp.get("id") == 2:
                img_data = base64.b64decode(resp["result"]["data"])
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"Captured: {output_path} ({len(img_data):,} bytes)")
                break

async def main():
    temp_dir = os.path.join(tempfile.gettempdir(), "chrome_cdp_prof")
    proc = subprocess.Popen([
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={temp_dir}",
        "--window-size=1440,950"
    ])
    
    await asyncio.sleep(2) # wait for Chrome to start
    
    out_dir = r"E:\01. Matkul\Semester 5\01. KI\UAS\reports\screenshots\redesign"
    os.makedirs(out_dir, exist_ok=True)
    
    pages = [
        ("01_intelligence_core_topology.png", "http://localhost:8505/?page=overview", 4),
        ("02_single_url_scanner.png", "http://localhost:8505/?page=single", 3),
        ("03_batch_threat_triage.png", "http://localhost:8505/?page=batch", 3),
        ("04_analytics_validation.png", "http://localhost:8505/?page=eval", 3),
        ("05_neural_architecture.png", "http://localhost:8505/?page=spec", 3),
        ("06_defensive_protocol.png", "http://localhost:8505/?page=guide", 3),
    ]
    
    try:
        for fname, url, wait_s in pages:
            out_file = os.path.join(out_dir, fname)
            await capture_page(url, out_file, wait_s)
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    asyncio.run(main())

