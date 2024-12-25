import os
import zipfile
import sys
import ctypes
from typing import List, Tuple, Optional
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from time import time, sleep

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class OptimizedDownloadManager:
    def __init__(self, local_file: str, extract_path: str):
        self.local_file = local_file
        self.extract_path = extract_path
        self.error_message = None

    def extract_local_file(self) -> bool:
        """Extract local ZIP file"""
        try:
            if not os.path.exists(self.local_file):
                self.error_message = f"Local file not found: {self.local_file}"
                return False

            print("\nExtracting files...")
            try:
                if os.path.exists(self.extract_path):
                    for root, dirs, files in os.walk(self.extract_path):
                        for f in files:
                            try:
                                os.remove(os.path.join(root, f))
                            except PermissionError:
                                self.error_message = f"Cannot remove existing file: {f}. Please close VRChat and try again."
                                return False
                
                with zipfile.ZipFile(self.local_file, 'r') as zip_ref:
                    zip_ref.extractall(self.extract_path)
                return True

            except PermissionError as e:
                self.error_message = f"Permission denied during extraction. Please close VRChat and try again: {str(e)}"
                return False

        except zipfile.BadZipFile as e:
            self.error_message = f"Invalid zip file: {str(e)}"
            return False
        except Exception as e:
            self.error_message = f"Extract Error: {str(e)}"
            return False

def clear_console():
    """Clear console screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def set_console_title(title: str):
    """Set console window title"""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def get_vrchat_path() -> str:
    """Get VRChat cache directory from user"""
    default_path = os.path.join(os.getenv('APPDATA'), '..', 'LocalLow', 'VRChat', 'VRChat')
    default_path = os.path.abspath(default_path)
    
    while True:
        print(f"VRChat Cache Folder Location (press Enter for default):")
        print(f"Default: {default_path}")
        user_path = input("> ").strip()
        
        path_to_check = user_path if user_path else default_path
        
        if os.path.exists(path_to_check):
            return path_to_check
        else:
            print("❌ VRChat Cache folder not found. Please try again.")

def main():
    try:
        local_file = get_resource_path('00000000000000000000000026000000.zip')
        
        print("="*60)
        print("ZyaNight Bar 🍷")
        print("="*60)
        print("\nℹ️ This tool only works for:")
        print("World Name: Information")
        print("World ID: wrld_951da35a-1b9f-4260-973e-5210c89ce693")
        print("-"*60)
        print("\n")
        
        vrchat_base = get_vrchat_path()
        
        extract_path = os.path.join(vrchat_base, 'Cache-WindowsPlayer', 'DC07F804E3F2FFA5', '00000000000000000000000026000000')
        
        clear_console()
        set_console_title("ZyaNight Bar 🍷")
        
        print("="*60)
        print("🚀 Starting file extraction...")
        print("="*60)
        
        download_manager = OptimizedDownloadManager(local_file, extract_path)
        success = download_manager.extract_local_file()
        
        clear_console()
        print("="*60)
        if success:
            print("✅ Process completed successfully")
            print("➡️ You can now start the game.")
        else:
            print("❌ Download process failed:")
            if download_manager.error_message:
                print(f"⚠️ Error details: {download_manager.error_message}")
            else:
                print("⚠️ No specific error details available")
        print("="*60)
    
    except Exception as e:
        print("\n"+"="*60)
        print(f"❌ Unexpected Error: {str(e)}")
        print("🔄 Please check your internet connection and try again.")
        print("="*60)
    
    finally:
        print("\n📝 Press Enter to exit...")
        input()
        sleep(2)

if __name__ == "__main__":
    main()