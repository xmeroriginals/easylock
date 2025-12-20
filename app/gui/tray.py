import sys
import os
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from app.utils.config import (set_preset_password, is_auto_start_enabled, 
                              set_auto_start, detect_language, get_resource_path)
from app.gui.dialogs import PresetPasswordDialog, InfoDialog

class EasyLockTray(QSystemTrayIcon):
    """System tray application controller for EasyLock."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lang = detect_language()
        
        # Initialize resources
        icon_path = get_resource_path(os.path.join("resources", "logotwo.png"))
        
        self.setIcon(QIcon(icon_path))
        self.setToolTip("EasyLock")
        
        self.init_menu()
        
        # Ensure context menu is installed on Windows systems
        if sys.platform == 'win32':
            from app.core.registry import is_context_menu_installed, register_context_menu
            if not is_context_menu_installed():
                register_context_menu()
            
        self.show()

    def init_menu(self):
        """Initialize the context menu for the system tray icon."""
        menu = QMenu()
        
        # Preset Password Action
        self.act_preset = QAction("Set Preset Password" if self.lang == "EN" else "Ön Ayarlı Şifre Belirle", menu)
        self.act_preset.triggered.connect(self.change_preset_password)
        menu.addAction(self.act_preset)
        
        menu.addSeparator()
        
        # Auto-Start Toggle
        self.act_autostart = QAction("Auto Start" if self.lang == "EN" else "Otomatik Başla", menu)
        self.act_autostart.setCheckable(True)
        self.act_autostart.setChecked(is_auto_start_enabled())
        self.act_autostart.triggered.connect(self.toggle_autostart)
        menu.addAction(self.act_autostart)
        
        # Repair Action
        self.act_repair = QAction("Repair EasyLock" if self.lang == "EN" else "EasyLock Onar", menu)
        self.act_repair.triggered.connect(self.repair_app)
        menu.addAction(self.act_repair)
        
        menu.addSeparator()
        
        # Exit Application
        self.act_exit = QAction("Exit" if self.lang == "EN" else "Çıkış", menu)
        self.act_exit.triggered.connect(QApplication.instance().quit)
        menu.addAction(self.act_exit)
        
        self.setContextMenu(menu)
        
    def change_preset_password(self):
        """Display configuration dialog for setting a preset password."""
        dialog = PresetPasswordDialog()
        
        if dialog.exec():
            try:
                pwd = dialog.password if dialog.password else None
                set_preset_password(pwd)
                
                msg = "Preset password updated." if self.lang == "EN" else "Ön ayarlı şifre güncellendi."
                self.showMessage("EasyLock", msg, QSystemTrayIcon.MessageIcon.Information)
            except Exception as e:
                title = "Error" if self.lang == "EN" else "Hata"
                InfoDialog(title, str(e), "error").exec()

    def toggle_autostart(self):
        """Enable or disable system startup integration."""
        state = self.act_autostart.isChecked()
        try:
            set_auto_start(state)
        except Exception as e:
            title = "Error" if self.lang == "EN" else "Hata"
            InfoDialog(title, str(e), "error").exec()
            self.act_autostart.setChecked(not state)

    def repair_app(self):
        """Re-install system context menu and configuration files."""
        try:
            from app.core.registry import register_context_menu
            register_context_menu()
            
            msg = "Application shell integration repaired." if self.lang == "EN" else "Uygulama kabuk entegrasyonu onarıldı."
            self.showMessage("EasyLock", msg, QSystemTrayIcon.MessageIcon.Information)
        except Exception as e:
            title = "Error" if self.lang == "EN" else "Hata"
            InfoDialog(title, str(e), "error").exec()
