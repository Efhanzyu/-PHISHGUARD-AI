"""
Skrip eksekusi Streamlit AppTest untuk memvalidasi rendering dan exception app.py
"""
import os
import sys
from streamlit.testing.v1 import AppTest

def test_app():
    app_path = os.path.abspath("app.py")
    print(f"Inisialisasi AppTest dari {app_path}...")
    try:
        at = AppTest.from_file(app_path, default_timeout=15)
        at.run()
        
        print("\n=== HASIL EKSEKUSI APPTEST ===")
        print(f"Jumlah Exception: {len(at.exception)}")
        if at.exception:
            for i, ex in enumerate(at.exception, 1):
                print(f"Exception #{i}: {ex.value}")
                print(f"Traceback #{i}: {ex.stack_trace}")
            return False
            
        print("Status AppTest: PASS (Tidak ada runtime exception)")
        print(f"Title: {at.title[0].value if at.title else 'No Title'}")
        print(f"Sidebar Elements: {len(at.sidebar)}")
        print(f"Metrics Elements: {len(at.metric)}")
        return True
    except Exception as e:
        import traceback
        print("Gagal menjalankan AppTest:", e)
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app()
    if not success:
        sys.exit(1)

