import os
import time
import subprocess
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from PIL import Image

PORT = 8085
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SCRATCH = r"C:\Users\musfi\.gemini\antigravity-ide\brain\678d45ab-a518-4a1d-836b-fd11f847a81e\scratch"

class DualStackServer(HTTPServer):
    def server_bind(self):
        super().server_bind()
        self.server_name = "localhost"
        self.server_port = PORT

def run_server():
    os.chdir(HERE)
    httpd = DualStackServer(("127.0.0.1", PORT), SimpleHTTPRequestHandler)
    print(f"Serving HTTP on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1)

    # 1. Test HTTP endpoints
    urls = [
        f"http://127.0.0.1:{PORT}/index.html",
        f"http://127.0.0.1:{PORT}/hero-banner.jpg",
        f"http://127.0.0.1:{PORT}/logo-fourteen-park.png",
        f"http://127.0.0.1:{PORT}/footer-logos.png",
    ]

    for u in urls:
        req = urllib.request.Request(u, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=5) as res:
                print(f"GET {u} -> Status {res.status}, Length {res.headers.get('Content-Length')}, Type {res.headers.get('Content-Type')}")
        except Exception as e:
            print(f"FAIL {u}: {e}")

    # 2. Render from HTTP server via headless Edge
    desktop_png = os.path.join(SCRATCH, "server_desktop_650.png")
    cmd = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=650,2010",
        f"--screenshot={desktop_png}",
        f"http://127.0.0.1:{PORT}/index.html"
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Desktop rendered from local server:", os.path.exists(desktop_png), Image.open(desktop_png).size if os.path.exists(desktop_png) else None)

    # 3. Render 500px mobile view from HTTP server
    mobile_png = os.path.join(SCRATCH, "server_view_500.png")
    cmd_m = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=500,2200",
        f"--screenshot={mobile_png}",
        f"http://127.0.0.1:{PORT}/index.html"
    ]
    subprocess.run(cmd_m, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Mobile rendered from local server:", os.path.exists(mobile_png), Image.open(mobile_png).size if os.path.exists(mobile_png) else None)
