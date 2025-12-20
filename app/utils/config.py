import os
import json
import sys
import keyring

# Path configuration
if sys.platform == 'win32':
    CONFIG_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'EasyLock')
else:
    CONFIG_DIR = os.path.expanduser('~/.config/EasyLock')

CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

# Keyring identifiers
KEYRING_SERVICE = "EasyLock"
KEYRING_PRESET_KEY = "preset_password"

def get_config() -> dict:
    """Load the application configuration from the persistent cache."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(config: dict):
    """Persist the configuration dictionary to the local cache file."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def set_preset_password(password: str):
    """Securely store the preset password using system-native storage."""
    if password is None:
        try:
            keyring.delete_password(KEYRING_SERVICE, KEYRING_PRESET_KEY)
        except keyring.errors.PasswordDeleteError:
            pass
    else:
        keyring.set_password(KEYRING_SERVICE, KEYRING_PRESET_KEY, password)

def get_preset_password() -> str:
    """Retrieve the preset password from secure system-native storage."""
    return keyring.get_password(KEYRING_SERVICE, KEYRING_PRESET_KEY)

def is_auto_start_enabled() -> bool:
    """Verify if the application is registered for system startup."""
    return get_config().get("auto_start", False)

def set_auto_start(enabled: bool):
    """Configure the application for automatic system startup."""
    config = get_config()
    config["auto_start"] = enabled
    save_config(config)
    
    if sys.platform == 'win32':
        _set_windows_autostart(enabled)

def _set_windows_autostart(enabled: bool):
    """Manage Windows registry entries for startup integration."""
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        if enabled:
            exe_path = sys.executable
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
    """Detect the system language and return 'TR' or 'EN'."""
    try:
        import locale
        lang, _ = locale.getdefaultlocale()
        if lang and lang.startswith('tr'):
            return 'TR'
    except Exception:
        pass
    return 'EN'
