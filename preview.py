"""
NEXORA INVENTORY INTELLIGENCE — LOCAL PORTAL LAUNCHER
Launches the executive interactive preview portal on a local lightweight web server
and automatically opens it in your default browser.
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 5050
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class NexoraPortalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        # Keep console clean
        pass

def launch_portal():
    url = f"http://localhost:{PORT}/preview.html"
    print("=" * 70)
    print("  NEXORA INVENTORY INTELLIGENCE — LOCAL EXECUTIVE PORTAL")
    print("=" * 70)
    print(f"  [STARTING] Serving portal from: {BASE_DIR}")
    print(f"  [ACCESS URL] {url}")
    print("  [ACTION] Opening in your default web browser...")
    print("  [CONTROL] Press Ctrl+C in this terminal to stop the preview server.")
    print("=" * 70)

    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"  [NOTE] Could not auto-launch browser: {e}")
        print(f"  Please open {url} manually.")

    server = HTTPServer(("127.0.0.1", PORT), NexoraPortalHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  [STOPPED] Preview server stopped.")
        server.server_close()

if __name__ == "__main__":
    launch_portal()
