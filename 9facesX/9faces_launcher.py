import os, sys, subprocess
import tkinter as tk
from tkinter import filedialog

os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = "_obfuscated"
ALLOWED_EXTENSIONS = [".luau", ".lua", ".txt"]

BANNER = r"""
 ________________________  _________ ___________ _________
/   __   \_   _____/  _  \ \_   ___ \\_   _____//   _____/
\____    /|    __)/  /_\  \/    \  \/ |    __)_ \_____  \ 
   /    / |     \/    |    \     \____|        \/        \
  /____/  \___  /\____|__  /\______  /_______  /_______  /
              \/         \/        \/        \/        \/
"""

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter to continue...")

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def process_luau_file(file_path):
    if not file_path:
        print("\n[!] No path provided.")
        pause()
        return

    # Clean up quotes if they dragged and dropped it
    file_path = file_path.strip().strip('"').strip("'")

    if not os.path.exists(file_path):
        print(f"\n[!] Error: Could not find file at: {file_path}")
        pause()
        return

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        print(f"\n[!] Invalid file type: {ext}")
        pause()
        return

    ensure_output_dir()

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_path = os.path.abspath(os.path.join(OUTPUT_DIR, f"{base_name}.obf.luau"))
    cmd = [sys.executable, "main.py", "-i", file_path, "-o", out_path, "--dev"]
    
    print(f"\n[*] Obfuscating: {os.path.basename(file_path)}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        size = os.path.getsize(out_path)
        print("\n" + "="*60)
        print(f"[+] SUCCESS! Saved to:\n    {out_path}")
        print(f"[+] Size: {size} bytes")
        print("="*60)
    else:
        print(f"\n[!] Failed to obfuscate.")
    
    pause()

def main():
    if not os.path.exists("main.py"):
        print("[!] ERROR: main.py not found! Make sure this launcher is in the same folder.")
        pause()
        return

    while True:
        clear()
        print(BANNER)
        print("  [1] Obfuscate a Luau script (File Picker)")
        print("  [2] Obfuscate a Luau script (Path Obfuscation)")
        print("  [3] Open the _obfuscated folder")
        print("  [0] Exit\n")
        
        choice = input("  Select an option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            print("\n[*] Opening file browser...")
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            file_path = filedialog.askopenfilename(
                title="Select a script to obfuscate",
                filetypes=[
                    ("Supported Scripts", "*.luau;*.lua;*.txt"),
                    ("Luau Scripts", "*.luau"),
                    ("Lua Scripts", "*.lua"),
                    ("Text Files", "*.txt")
                ]
            )
            root.destroy()

            if not file_path:
                print("[*] Cancelled.")
                pause()
                continue

            process_luau_file(file_path)

        elif choice == "2":
            print("\n[*] Enter the full path to your script file.")
            print("[*] TIP: You can drag and drop the file into this window.")
            file_path = input("  > ")
            
            process_luau_file(file_path)

        elif choice == "3":
            if os.path.exists(OUTPUT_DIR):
                os.startfile(os.path.abspath(OUTPUT_DIR))
            else:
                print("\n[!] The _obfuscated folder hasn't been created yet.")
                pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting.")
        sys.exit(0)
