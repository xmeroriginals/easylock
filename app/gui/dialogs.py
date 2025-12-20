from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QHBoxLayout, QWidget, QGraphicsDropShadowEffect, QCheckBox)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QRect
from PyQt6.QtGui import QColor, QFont, QIcon
import os

from app.utils.config import detect_language

# Translation dictionary for multi-language support
TEXTS = {
    "TR": {
        "title_lock": "Dosyayı Şifrele",
        "title_unlock": "Şifreyi Çöz",
        "title_preset": "Ön Ayarlı Şifre",
        "title_confirm": "Onay",
        "title_info": "Bilgi",
        "title_error": "Hata",
        "title_warning": "Uyarı",
        "enter_pass": "Şifreyi Girin",
        "preset_label": "Yeni şifreyi girin (temizlemek için boş bırakın):",
        "show_password": "Şifreyi Göster",
        "ok": "Tamam",
        "yes": "Evet",
        "no": "Hayır",
        "cancel": "İptal",
        "placeholder": "********",
        "empty_password": "Şifre boş olamaz!"
    },
    "EN": {
        "title_lock": "Lock File",
        "title_unlock": "Unlock File",
        "title_preset": "Preset Password",
        "title_confirm": "Confirmation",
        "title_info": "Information",
        "title_error": "Error",
        "title_warning": "Warning",
        "enter_pass": "Enter Password",
        "preset_label": "Enter new preset password (leave empty to clear):",
        "show_password": "Show Password",
        "ok": "OK",
        "yes": "Yes",
        "no": "No",
        "cancel": "Cancel",
        "placeholder": "********",
        "empty_password": "Password cannot be empty!"
    }
}

# Unified design system for application dialogs
DIALOG_STYLESHEET = """
    QDialog {
        background-color: transparent;
    }
    QWidget#MainWidget {
        background-color: #1a1a1a;
        border-radius: 16px;
        border: 1px solid #3e3e3e;
    }
    QLabel {
        color: #ffffff;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 14px;
    }
    QLabel#Title {
        font-size: 20px;
        font-weight: bold;
        color: #4CAF50;
    }
    QLabel#Icon {
        font-size: 48px;
        padding: 10px;
    }
    QLabel#Message {
        font-size: 14px;
        color: #b3b3b3;
        line-height: 1.6;
    }
    QLineEdit {
        background-color: #2d2d2d;
        border: 2px solid #3e3e3e;
        border-radius: 8px;
        color: white;
        padding: 10px 12px;
        font-size: 14px;
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }
    QLineEdit:focus {
        border: 2px solid #4CAF50;
        background-color: #252525;
    }
    QLineEdit:hover {
        border-color: #4a4a4a;
    }
    QCheckBox {
        color: #b3b3b3;
        font-size: 13px;
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid #3e3e3e;
        background-color: #2d2d2d;
    }
    QCheckBox::indicator:checked {
        background-color: #4CAF50;
        border-color: #4CAF50;
        image: url(none);
    }
    QCheckBox::indicator:hover {
        border-color: #4CAF50;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #3d8b40;
    }
    QPushButton#CancelButton {
        background-color: #333333;
        color: #b3b3b3;
    }
    QPushButton#CancelButton:hover {
        background-color: #3e3e3e;
        color: #ffffff;
    }
    QPushButton#DestructiveButton {
        background-color: #d32f2f;
    }
    QPushButton#DestructiveButton:hover {
        background-color: #b71c1c;
    }
"""


class PasswordDialog(QDialog):
    """Modern dark-themed password input dialog for lock/unlock operations."""
    
    def __init__(self, mode="lock"):
        super().__init__()
        self.lang = detect_language()
        self.texts = TEXTS.get(self.lang, TEXTS["EN"])
        self.mode = mode
        self.password = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(DIALOG_STYLESHEET)
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        layout.addWidget(self.main_widget)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.main_widget.setGraphicsEffect(shadow)
        
        inner_layout = QVBoxLayout(self.main_widget)
        inner_layout.setContentsMargins(30, 30, 30, 30)
        inner_layout.setSpacing(7)
        
        title_text = self.texts["title_lock"] if self.mode == "lock" else self.texts["title_unlock"]
        self.lbl_title = QLabel(title_text)
        self.lbl_title.setObjectName("Title")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_title)
        
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText(self.texts["placeholder"])
        self.input_pass.setFocus()
        self.input_pass.returnPressed.connect(self.accept_password)
        inner_layout.addWidget(self.input_pass)
        
        self.chk_show = QCheckBox(self.texts["show_password"])
        self.chk_show.stateChanged.connect(self.toggle_password_visibility)
        inner_layout.addWidget(self.chk_show)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_cancel = QPushButton(self.texts["cancel"])
        self.btn_cancel.setObjectName("CancelButton")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_ok = QPushButton(self.texts["ok"])
        self.btn_ok.clicked.connect(self.accept_password)
        self.btn_ok.setDefault(True)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)
        inner_layout.addLayout(btn_layout)
        
    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
    def accept_password(self):
        pwd = self.input_pass.text()
        if pwd:
            self.password = pwd
            self.accept()
        else:
            self.shake_animation()
            
    def shake_animation(self):
        """Visual feedback for invalid input."""
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(500)
        geometry = self.geometry()
        
        for i in range(5):
            animation.setKeyValueAt(i / 4.0, QRect(geometry.x() + (10 if i % 2 else -10), 
                                                     geometry.y(), geometry.width(), geometry.height()))
        animation.setKeyValueAt(1.0, geometry)
        animation.start()


class PresetPasswordDialog(QDialog):
    """Configuration dialog for preset password management."""
    
    def __init__(self):
        super().__init__()
        self.lang = detect_language()
        self.texts = TEXTS.get(self.lang, TEXTS["EN"])
        self.password = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(DIALOG_STYLESHEET)
        self.setFixedWidth(450)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        layout.addWidget(self.main_widget)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.main_widget.setGraphicsEffect(shadow)
        
        inner_layout = QVBoxLayout(self.main_widget)
        inner_layout.setContentsMargins(30, 30, 30, 30)
        inner_layout.setSpacing(10)
        
        self.lbl_title = QLabel(self.texts["title_preset"])
        self.lbl_title.setObjectName("Title")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_title)
        
        inner_layout.addSpacing(8)
        
        self.lbl_desc = QLabel(self.texts["preset_label"])
        self.lbl_desc.setObjectName("Message")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_desc)
        
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText(self.texts["placeholder"])
        self.input_pass.setFocus()
        self.input_pass.returnPressed.connect(self.accept_password)
        inner_layout.addWidget(self.input_pass)
        
        self.chk_show = QCheckBox(self.texts["show_password"])
        self.chk_show.stateChanged.connect(self.toggle_password_visibility)
        inner_layout.addWidget(self.chk_show)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_cancel = QPushButton(self.texts["cancel"])
        self.btn_cancel.setObjectName("CancelButton")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_ok = QPushButton(self.texts["ok"])
        self.btn_ok.clicked.connect(self.accept_password)
        self.btn_ok.setDefault(True)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)
        inner_layout.addLayout(btn_layout)
        
    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
    def accept_password(self):
        self.password = self.input_pass.text()
        self.accept()


class ConfirmationDialog(QDialog):
    """Generic confirmation dialog with dual-choice actions."""
    
    def __init__(self, title, message, is_destructive=False):
        super().__init__()
        self.lang = detect_language()
        self.texts = TEXTS.get(self.lang, TEXTS["EN"])
        self.title_text = title
        self.message_text = message
        self.is_destructive = is_destructive
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(DIALOG_STYLESHEET)
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        layout.addWidget(self.main_widget)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.main_widget.setGraphicsEffect(shadow)
        
        inner_layout = QVBoxLayout(self.main_widget)
        inner_layout.setContentsMargins(30, 30, 30, 30)
        inner_layout.setSpacing(8)
        
        icon_label = QLabel("❓")
        icon_label.setObjectName("Icon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(icon_label)
        
        inner_layout.addSpacing(5)
        
        self.lbl_title = QLabel(self.title_text)
        self.lbl_title.setObjectName("Title")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_title)
        
        inner_layout.addSpacing(8)
        self.lbl_message = QLabel(self.message_text)
        self.lbl_message.setObjectName("Message")
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_message)
        
        inner_layout.addSpacing(12)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_no = QPushButton(self.texts["no"])
        self.btn_no.setObjectName("CancelButton")
        self.btn_no.clicked.connect(self.reject)
        
        self.btn_yes = QPushButton(self.texts["yes"])
        if self.is_destructive:
            self.btn_yes.setObjectName("DestructiveButton")
        self.btn_yes.clicked.connect(self.accept)
        self.btn_yes.setDefault(True)
        
        btn_layout.addWidget(self.btn_no)
        btn_layout.addWidget(self.btn_yes)
        inner_layout.addLayout(btn_layout)


class InfoDialog(QDialog):
    """Information and alert dialog system."""
    
    def __init__(self, title, message, dialog_type="info"):
        super().__init__()
        self.lang = detect_language()
        self.texts = TEXTS.get(self.lang, TEXTS["EN"])
        self.title_text = title
        self.message_text = message
        self.dialog_type = dialog_type
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(DIALOG_STYLESHEET)
        self.setFixedWidth(380)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        layout.addWidget(self.main_widget)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.main_widget.setGraphicsEffect(shadow)
        
        inner_layout = QVBoxLayout(self.main_widget)
        inner_layout.setContentsMargins(30, 30, 30, 30)
        inner_layout.setSpacing(8)
        
        icon_map = {"info": "ℹ️", "error": "❌", "warning": "⚠️"}
        icon_label = QLabel(icon_map.get(self.dialog_type, "ℹ️"))
        icon_label.setObjectName("Icon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(icon_label)
        
        inner_layout.addSpacing(5)
        
        self.lbl_title = QLabel(self.title_text)
        self.lbl_title.setObjectName("Title")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_title)
        
        inner_layout.addSpacing(8)
        
        self.lbl_message = QLabel(self.message_text)
        self.lbl_message.setObjectName("Message")
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(self.lbl_message)
        
        inner_layout.addSpacing(12)
        
        self.btn_ok = QPushButton(self.texts["ok"])
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        inner_layout.addWidget(self.btn_ok)
