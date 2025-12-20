import sys
import os

def register_context_menu():
    """Register the application in the system shell context menu."""
    if sys.platform == 'win32':
        _register_windows()
    elif sys.platform.startswith('linux'):
        _register_linux()

def unregister_context_menu():
    """Remove the application from the system shell context menu."""
    if sys.platform == 'win32':
        _unregister_windows()
    elif sys.platform.startswith('linux'):
        _unregister_linux()

def is_context_menu_installed() -> bool:
    """Check if the context menu integration is currently active."""
    if sys.platform == 'win32':
        return _is_installed_windows()
    return False

def _register_windows():
    """Implement Windows registry entries for shell integration."""
    try:
        import winreg
        exe_path = sys.executable
        
        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller bundle
            base_cmd = f'"{exe_path}"'
        else:
            # Running from source
            main_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "run.py"))
            base_cmd = f'"{exe_path}" "{main_py}"'
        
        # Add to '*' (all files)
        _create_key(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Lock", "Lock File", f'{base_cmd} lock "%1"')
        _create_key(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Unlock", "Unlock File", f'{base_cmd} unlock "%1"')
        
    except Exception as e:
        print(f"Windows Registry Error: {e}")

def _create_key(hkey, path, title, command):
    import winreg
    from app.utils.config import get_resource_path
    key = winreg.CreateKey(hkey, path)
    winreg.SetValue(key, "", winreg.REG_SZ, title)
    
    # Set Icon if available
    icon_path = get_resource_path(os.path.join("resources", "logotwo.ico"))
    if os.path.exists(icon_path):
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
        
    cmd_key = winreg.CreateKey(key, "command")
    winreg.SetValue(cmd_key, "", winreg.REG_SZ, command)

def _unregister_windows():
    import winreg
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Lock\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Lock")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Unlock\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Unlock")
    except OSError:
        pass

def _is_installed_windows() -> bool:
    import winreg
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\EasyLock.Lock")
        return True
    except WindowsError:
        return False

def _register_linux():
    """Implement Linux .desktop entries for file manager integration."""
    apps_dir = os.path.expanduser('~/.local/share/applications')
    os.makedirs(apps_dir, exist_ok=True)
    
    exe_path = sys.executable
    if getattr(sys, 'frozen', False):
        base_cmd = exe_path
    else:
        main_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "run.py"))
        base_cmd = f'{exe_path} {main_py}'
    
    # Create main app desktop entry
    desktop_file = os.path.join(apps_dir, 'easylock.desktop')
    content = f"""[Desktop Entry]
Type=Application
Name=EasyLock
Exec={base_cmd} %F
Icon=easylock
Comment=Secure Your Files
Terminal=false
Categories=Utility;Security;
MimeType=application/octet-stream;
"""
    with open(desktop_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # For deep integration (Nautilus/Nemo/Caja actions could be added here)
    # For now, we rely on the application being in the "Open With" menu 
    # and the system tray for general management.

def _unregister_linux():
    """Remove Linux-specific desktop entries."""
    desktop_file = os.path.expanduser('~/.local/share/applications/easylock.desktop')
    if os.path.exists(desktop_file):
        os.remove(desktop_file)
