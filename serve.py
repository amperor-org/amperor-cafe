#!/usr/bin/env python3
"""Tiny no-cache static server for the KURE'D CAFE landing site.

No build step — the site is plain HTML/CSS/JS plus image-frame sequences.
The only reason this exists (instead of `python3 -m http.server`) is the
`Cache-Control: no-store` header, so scroll-scrubbed frame sequences never
show a stale frame after you regenerate them.

Usage:
    python3 serve.py                     # serves ./site on :5501
    python3 serve.py site 5501           # explicit folder + port
    python3 serve.py versions/v2 5502    # run a saved snapshot
    python3 serve.py versions/v1 5503

Then open the printed URL. Ctrl+C to stop.
"""
import os
import sys
import http.server
import socketserver

BASE = os.path.dirname(os.path.abspath(__file__))
directory = sys.argv[1] if len(sys.argv) > 1 else "site"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5501
root = directory if os.path.isabs(directory) else os.path.join(BASE, directory)

if not os.path.isdir(root):
    sys.exit(f"Folder not found: {root}")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=root, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, *a):  # keep the console quiet
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"KURE'D  ->  http://localhost:{port}/            (serving {directory}/)")
    print(f"           journey demo: http://localhost:{port}/demo.html")
    print("Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
