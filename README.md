# 🔒 EasyLock

<div align="center">

![EasyLock Logo](assets/logotwo.png)

**Fast & Secure File Encryption with AES-256**

[![License: DET-C](https://img.shields.io/badge/License-DET--C-green.svg)](https://raw.githubusercontent.com/xmeroriginals/easylock/refs/heads/main/LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/xmeroriginals/easylock)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)

**[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Technical Details](#-technical-details) • [Security](#-security-considerations)**

</div>

---

## 📖 Overview

**EasyLock** is a lightweight, user-friendly file encryption tool that seamlessly integrates into your operating system's context menu. With military-grade AES-256-GCM encryption, you can secure your sensitive files with just a right-click. Now featuring a fully integrated landing page built directly into the repository.

### Why EasyLock?

- 🚀 **Lightning Fast**: Optimized performance for instant encryption
- 🔐 **Military-Grade Security**: AES-256-GCM encryption standard
- 🖱️ **Seamless Integration**: Right-click context menu support
- 🎨 **Modern UI**: Beautiful dark-themed interface with glassmorphism
- 🌍 **Cross-Platform**: Windows 10/11 and Linux (Ubuntu 20.04+)
- 🔑 **Smart Lock**: Preset password support with keyboard shortcuts (Meta/Win key)
- 🆓 **Open Source**: Completely free and transparent under DET-C license

---

## ✨ Features

### Core Features

- **AES-256-GCM Encryption**: Industry-standard encryption with authenticated encryption
- **Context Menu Integration**: Lock/Unlock files directly from right-click menu
- **Preset Password**: Set a default password for quick encryption (hold Meta/Win key)
- **System Tray Application**: Runs quietly in the background
- **Auto-Start**: Optional automatic startup on system boot
- **Secure Password Storage**: Passwords stored using OS-native secure storage (Windows DPAPI / Linux Secret Service)
- **Dark Theme UI**: Modern interface using Material Symbols Rounded and local fonts
- **Dual Language Support**: English and Turkish (auto-detected)

### Security Features

- **PBKDF2-HMAC-SHA256**: 200,000 iterations for key derivation
- **Random Salt & Nonce**: Unique encryption for each file
- **No Plaintext Storage**: Passwords never stored in plain text
- **Memory Security**: Secure key derivation and handling
- **Extension Protection**: Prevents double encryption

---

## 🚀 Installation

### Prerequisites

- **Windows**: Windows 10 or Windows 11
- **Linux**: Ubuntu 20.04+ or other modern distributions
- **Python**: 3.8 or higher

### Method: From Source

1. **Clone the repository**
```bash
git clone https://github.com/xmeroriginals/easylock.git
cd easylock
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
- **Windows**: `.venv\Scripts\activate`
- **Linux/Mac**: `source .venv/bin/activate`

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run EasyLock**
```bash
python run.py
```

---

## 📋 Usage

### Installation & Setup

1. **Install Context Menu** (Windows only, first-time setup)
```bash
python run.py install
```

2. **Run System Tray Application**
```bash
python run.py
```

### Encrypting Files

- **Right-Click**: Select **"Lock File"** and enter your password.
- **Quick Lock**: Set a preset password, then hold **Windows key** (Meta) while selecting **"Lock File"**.

### Decrypting Files

- Right-click an `.elock` file and select **"Unlock File"**.

---

## 🛠️ Technical Details

### Architecture

```
EasyLock/
├── app/               # Application Core
│   ├── core/          # Encryption & Registry logic
│   ├── gui/           # PyQt6 Dialogs & Tray
│   └── utils/         # Configuration
├── resources/         # Local fonts & icons
├── assets/            # Web assets
├── css/               # Web styles
├── js/                # Web logic
├── index.html         # Integrated landing page
└── run.py             # Entry point
```

---

## 🔐 Security Considerations

⚠️ **Password Recovery**: If you forget your password, files **cannot be recovered**.  
⚠️ **Backup**: Always keep backups of critical data.  
⚠️ **Strong Passwords**: Use complex, unique passwords.

---

## 📄 License

This project is licensed under the **Digital Freedom and Ethical Technology License (DET-C) - v1.0**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI Framework
- [cryptography](https://cryptography.io/) - Cryptographic primitives
- [Material Symbols](https://fonts.google.com/icons) - Rounded icons (Local)
- [Lexend / Poppins / Space Grotesk](https://fonts.google.com/) - Professional typography (Local)

---

## 📧 Contact

- **Website**: [xmeroriginals.com/#contact](https://xmeroriginals.com/#contact)
- **GitHub**: [xmeroriginals/easylock](https://github.com/xmeroriginals/easylock)

---

<div align="center">

**Made with ❤️ by [Xmer™](https://xmeroriginals.com)**

</div>

---

## 🌍 Türkçe / Turkish

**EasyLock**, dosyalarınızı askeri düzeyde AES-256 şifreleme ile güvence altına almanın en kolay yoludur. Windows ve Linux sistemlerine doğrudan entegre olur ve internete bağlı kalmadan yerel kaynaklarla çalışır.

- 🔐 **AES-256-GCM**: Maksimum güvenlik
- 🖱️ **Sağ Tık Entegrasyonu**: Kolay kullanım
- ⚡ **Hızlı Kilit**: Meta tuşu desteği
- 🌍 **Yerel Kaynaklar**: Google API veya harici CDN gerektirmez
