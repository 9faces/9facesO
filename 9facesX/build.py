import PyInstaller.__main__
import hashlib
import os

def build():
    print("[*] Building 9faces Executable...")
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--name=9faces_v1.5.4',
        '--clean',
        '--noconfirm'
    ])

    exe_path = os.path.join("dist", "9faces_v1.5.4.exe")
    
    print("[*] Calculating SHA-256 Hash...")
    with open(exe_path, "rb") as f:
        exe_hash = hashlib.sha256(f.read()).hexdigest()

    print("\n" + "="*50)
    print(f"[!] Build Complete!")
    print(f"[!] Copy this hash into 9facesM/integrity.py")
    print(f"[!] HASH: {exe_hash}")
    print("="*50 + "\n")

if __name__ == "__main__":
    build()
