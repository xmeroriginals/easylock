import sys
import os
from PyQt6.QtWidgets import QApplication
from app.core.crypto import encrypt_file, decrypt_file, CryptoError
from app.gui.dialogs import PasswordDialog, InfoDialog
from app.gui.tray import EasyLockTray
from app.utils.config import get_preset_password, detect_language

def is_meta_pressed():
    """Check if Meta (Windows/Command) key is currently pressed."""
    if sys.platform == "win32":
        try:
            import win32api
            import win32con
            return (
                win32api.GetAsyncKeyState(win32con.VK_LWIN) < 0 or
                win32api.GetAsyncKeyState(win32con.VK_RWIN) < 0
            )
        except ImportError:
            return False

    elif sys.platform.startswith("linux"):
        try:
            from Xlib import display
            d = display.Display()
            root = d.screen().root
            keymap = root.query_pointer()._data["mask"]
            # Mod4 = Meta / Super key mask
            Mod4Mask = 1 << 6
            return bool(keymap & Mod4Mask)
        except Exception:
            return False

    return False

def show_message(title, message, dialog_type="info"):
    """Display a custom dark-themed info/error dialog."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    dialog = InfoDialog(title, message, dialog_type)
    dialog.activateWindow()
    dialog.raise_()
    dialog.exec()

def main():
    """Main execution entry point."""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    args = sys.argv[1:]
    lang = detect_language()
    
    if not args:
        # Start in system tray mode
        tray = EasyLockTray()
        sys.exit(app.exec())
        
    command = args[0]
    
    if command in ["lock", "unlock"] and len(args) > 1:
        file_path = args[1]
        
        # Check if Meta key is held for quick-lock using preset password
        use_preset = is_meta_pressed()  
        password = None
        
        if use_preset:
            password = get_preset_password()
            if not password:
                use_preset = False
        
        if not password:
            dialog_mode = "lock" if command == "lock" else "unlock"
            dialog = PasswordDialog(mode=dialog_mode)
            dialog.activateWindow()
            dialog.raise_()
            
            if dialog.exec():
                password = dialog.password
            else:
                sys.exit(0)
        
        if password:
            try:
                if command == "lock":
                    encrypt_file(file_path, password)
                    title = "Success" if lang == "EN" else "Başarılı"
                    msg = "File encrypted successfully." if lang == "EN" else "Dosya başarıyla şifrelendi."
                    show_message(title, msg, "info")
                else:
                    decrypt_file(file_path, password)
                    title = "Success" if lang == "EN" else "Başarılı"
                    msg = "File decrypted successfully." if lang == "EN" else "Dosyanın şifresi başarıyla çözüldü."
                    show_message(title, msg, "info")
            except CryptoError as e:
                title = "Encryption Error" if lang == "EN" else "Şifreleme Hatası"
                err_msg = str(e)
                if "Invalid password" in err_msg:
                    err_msg = "Invalid password or corrupted file." if lang == "EN" else "Geçersiz şifre veya bozuk dosya."
                elif "already encrypted" in err_msg:
                    err_msg = "File is already encrypted." if lang == "EN" else "Dosya zaten şifrelenmiş."
                elif "corrupted" in err_msg:
                    err_msg = "File is corrupted or invalid." if lang == "EN" else "Dosya bozuk veya geçersiz."
                show_message(title, err_msg, "error")
            except FileNotFoundError:
                title = "File Not Found" if lang == "EN" else "Dosya Bulunamadı"
                msg = "The specified file could not be found." if lang == "EN" else "Belirtilen dosya bulunamadı."
                show_message(title, msg, "error")
            except Exception as e:
                title = "Error" if lang == "EN" else "Hata"
                msg = f"Unexpected error: {str(e)}"
                show_message(title, msg, "error")

    elif command == "install":
        from app.core.registry import register_context_menu
        register_context_menu()
        show_message("EasyLock", "Component installed successfully.")

    elif command == "uninstall":
        from app.core.registry import unregister_context_menu
        unregister_context_menu()
        show_message("EasyLock", "Component uninstalled successfully.")
        
    sys.exit(0)

if __name__ == "__main__":
    main()
