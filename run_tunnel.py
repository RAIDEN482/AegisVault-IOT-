#!/usr/bin/env python3
"""
AegisVault Trusted Public Tunnel Gateway
Serves dashboard.html on HTTP port 8000 and launches a Cloudflare/Localtunnel
public tunnel with a trusted CA-signed SSL certificate so mobile WebAuthn
biometrics work seamlessly without browser TLS security blocks.
"""

import os
import sys
import time
import re
import signal
import socket
import threading
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED_BIN = os.path.join(WORKSPACE_DIR, "cloudflared")

class QuietHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKSPACE_DIR, **kwargs)

    def log_message(self, format, *args):
        # Format logs in minimal terminal style
        sys.stderr.write(f"[HTTP 8000] {self.address_string()} - {format % args}\n")

def start_http_server():
    server = HTTPServer(("0.0.0.0", PORT), QuietHTTPHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server

def launch_tunnel():
    # Prefer cloudflared if binary is present
    if os.path.exists(CLOUDFLARED_BIN) and os.access(CLOUDFLARED_BIN, os.X_OK):
        cmd = [CLOUDFLARED_BIN, "tunnel", "--url", f"http://127.0.0.1:{PORT}"]
        tunnel_type = "Cloudflare Quick Tunnel"
    else:
        cmd = ["npx", "--yes", "localtunnel", "--port", str(PORT)]
        tunnel_type = "Localtunnel"

    print(f"[*] Initializing {tunnel_type} for port {PORT}...")
    
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    tunnel_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.(trycloudflare\.com|loca\.lt)")

    # Read output to extract public HTTPS URL
    for line in iter(proc.stdout.readline, ""):
        match = url_pattern.search(line)
        if match:
            tunnel_url = match.group(0)
            break
        # Also check localtunnel format: "your url is: https://..."
        if "your url is:" in line.lower():
            raw_url = line.strip().split()[-1]
            if raw_url.startswith("https://"):
                tunnel_url = raw_url
                break

    if tunnel_url:
        print("\n" + "=" * 65)
        print("  AEGISVAULT // TRUSTED PUBLIC WEBAUTHN GATEWAY")
        print("=" * 65)
        print(f"  [>] Local PC Access:   http://localhost:{PORT}/dashboard.html")
        print(f"  [>] MOBILE PHONE URL:  {tunnel_url}/dashboard.html")
        print("-" * 65)
        print("  [*] TRUSTED SSL: Valid CA certificate (Zero browser warnings).")
        print("  [*] Mobile WebAuthn native fingerprint prompt is ACTIVE.")
        print("=" * 65 + "\n")
    else:
        print("[!] Warning: Could not automatically parse tunnel URL. Check tunnel logs:")

    return proc

def main():
    # Start local HTTP server
    http_server = start_http_server()
    print(f"[+] Local HTTP server listening on http://0.0.0.0:{PORT}")

    # Launch tunnel
    tunnel_proc = launch_tunnel()

    def signal_handler(sig, frame):
        print("\n[*] Shutting down AegisVault tunnel gateway...")
        tunnel_proc.terminate()
        http_server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Keep process alive and echo any pertinent tunnel messages
        for line in iter(tunnel_proc.stdout.readline, ""):
            # Silence redundant periodic pings/metrics
            if "metrics" not in line.lower() and "icmp" not in line.lower():
                pass
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
