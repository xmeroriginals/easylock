import os
import json
import sys
import keyring

if sys.platform == 'win32':
    CONFIG_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'EasyLock')
else:
    CONFIG_DIR = os.path.expanduser('~/.config/EasyLock')

CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

KEYRING_SERVICE = "EasyLock"
KEYRING_PRESET_KEY = "preset_password"

def get_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(config: dict):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def set_preset_password(password: str):
    if password is None:
        try:
            keyring.delete_password(KEYRING_SERVICE, KEYRING_PRESET_KEY)
        except keyring.errors.PasswordDeleteError:
            pass
    else:
        keyring.set_password(KEYRING_SERVICE, KEYRING_PRESET_KEY, password)

def get_preset_password() -> str:
    return keyring.get_password(KEYRING_SERVICE, KEYRING_PRESET_KEY)

def is_auto_start_enabled() -> bool:
    return get_config().get("auto_start", False)

def set_auto_start(enabled: bool):
    config = get_config()
    config["auto_start"] = enabled
    save_config(config)
    
    if sys.platform == 'win32':
        _set_windows_autostart(enabled)
    elif sys.platform.startswith('linux'):
        _set_linux_autostart(enabled)

def _set_linux_autostart(enabled: bool):
    autostart_dir = os.path.expanduser('~/.config/autostart')
    desktop_file = os.path.join(autostart_dir, 'easylock.desktop')
    
    if enabled:
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir, exist_ok=True)
            
        exe_path = sys.executable
        if getattr(sys, 'frozen', False):
            cmd = f'"{exe_path}"'
        else:
            main_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "run.py"))
            cmd = f'"{exe_path}" "{main_py}"'
            
        content = f"""[Desktop Entry]
Type=Application
Name=EasyLock
Exec={cmd}
Icon=easylock
Comment=Secure File Encryption
Terminal=false
X-GNOME-Autostart-enabled=true
"""
        with open(desktop_file, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        if os.path.exists(desktop_file):
            os.remove(desktop_file)

def _set_windows_autostart(enabled: bool):
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        if enabled:
            exe_path = sys.executable
            if getattr(sys, 'frozen', False):
                cmd = f'"{exe_path}"'
            else:
                main_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "run.py"))
                cmd = f'"{exe_path}" "{main_py}"'
            winreg.SetValueEx(key, "EasyLock", 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, "EasyLock")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Autostart Error: {e}")

def detect_language() -> str:
    try:
        import locale
        lang, _ = locale.getdefaultlocale()
        if lang and lang.startswith('tr'):
            return 'TR'
    except Exception:
        pass
    return 'EN'

def get_resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    return os.path.join(base_path, relative_path)
