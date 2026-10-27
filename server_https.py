#!/usr/bin/env python3
"""
AegisVault Gateway Server
Starts HTTP server on port 8000 and launches a trusted Cloudflare/Localtunnel
gateway to ensure mobile browsers allow the WebAuthn API without TLS errors.
"""

import os
import sys

# Forward directly to run_tunnel.py logic
if __name__ == "__main__":
    from run_tunnel import main
    main()
