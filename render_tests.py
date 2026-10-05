import os
import subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SCRATCH = r"C:\Users\musfi\.gemini\antigravity-ide\brain\678d45ab-a518-4a1d-836b-fd11f847a81e\scratch"

def render(html_path, out_png, width, height, user_agent=None):
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    cmd = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={out_png}",
    ]
    if user_agent:
        cmd.append(f"--user-agent={user_agent}")
    cmd.append(url)
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    # Render desktop (650 width, auto height)
    render("preview_local.html", os.path.join(SCRATCH, "desk.png"), 650, 2010)
    # Render 600px breakpoint
    render("preview_local.html", os.path.join(SCRATCH, "view_500.png"), 500, 2200)
    print("Desktop rendered")
