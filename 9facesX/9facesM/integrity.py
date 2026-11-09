import hashlib
import sys
import os

EXPECTED_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

def check_integrity():
    if getattr(sys, 'frozen', False):
        target_file = sys.executable
    else:
        target_file = sys.argv[0]

    try:
        with open(target_file, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        if file_hash != EXPECTED_HASH and EXPECTED_HASH != "0000000000000000000000000000000000000000000000000000000000000000":
            print("[-] SECURITY ALERT: Integrity check failed! This file has been tampered with.")
            input("Press Enter to exit...")
            sys.exit(1)
    except Exception as e:
        print(f"[-] Integrity Check Error: {e}")
        sys.exit(1)
