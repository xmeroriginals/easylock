/**
 * EasyLock Website Script
 * Handles translations, animations, and mobile navigation.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Translation Data
    const translations = {
        "EN": {
            // Navigation
            "nav_home": "Home",
            "nav_features": "Features",
            "nav_how": "How it Works",
            "nav_faq": "FAQ",
            "btn_download": "Download Now",

            // Hero
            "hero_badge": "AES-256 Encryption",
            "hero_title": "Secure Your Files in Seconds",
            "hero_desc": "EasyLock is the fastest and most secure way to encrypt your files directly from the Context Menu. Powered by military-grade AES-256 encryption.",
            "btn_learn": "Learn More",
            "stat_encryption": "Encryption",
            "stat_speed": "Lock Speed",
            "stat_secure": "Secure",

            // Features
            "features_subtitle": "Everything you need to keep your files secure",
            "feat_fast_title": "Lightning Fast",
            "feat_fast_desc": "Optimized performance ensures your files are encrypted instantly without lag.",
            "feat_secure_title": "AES-256 Security",
            "feat_secure_desc": "Military-grade encryption keeps your data safe from prying eyes. Your keys, your data.",
            "feat_easy_title": "Easy Integration",
            "feat_easy_desc": "Seamlessly integrated into your system shell. Just right-click to encrypt.",
            "feat_smart_title": "Smart Lock",
            "feat_smart_desc": "Hold Meta (Win/Cmd) key to instantly lock/unlock using your preset password.",
            "feat_password_title": "Secure Storage",
            "feat_password_desc": "Passwords stored using OS-native secure storage. Never stored in plain text.",
            "feat_startup_title": "Auto-Start",
            "feat_startup_desc": "Runs quietly in system tray. Always ready when you need it.",

            // Showcase
            "showcase_title": "How it Works",
            "showcase_desc": "Three simple steps to secure your files",
            "step_1": "Right-click any file or folder",
            "step_2": "Select 'Lock File' from the menu",
            "step_3": "Enter password or use Preset mode",

            // FAQ
            "faq_title": "Frequently Asked Questions",
            "faq_subtitle": "Everything you need to know about EasyLock",
            "faq_q1": "Is my data safe?",
            "faq_a1": "Yes! EasyLock uses AES-256 GCM encryption. Your passwords are stored securely using OS-native secure APIs.",
            "faq_q2": "What if I forget my password?",
            "faq_a2": "Encrypted files cannot be recovered without the correct password. This ensures maximum security. We recommend using a password manager.",
            "faq_q3": "Which platforms are supported?",
            "faq_a3": "EasyLock is compatible with Windows 10/11 and Linux (Ubuntu 20.04+). It integrates seamlessly with system file managers.",
            "faq_q4": "How fast is the encryption?",
            "faq_a4": "EasyLock is optimized for speed. Most common files encrypt in under a second on modern systems.",

            // Download
            "download_title": "Get Started Today",
            "download_desc": "Start protecting your files in seconds. Free and open source.",
            "btn_download_windows": "Download for Windows",
            "btn_download_linux": "Download for Linux",

            // Footer
            "footer_tagline": "Secure file encryption made easy",
            "footer_product": "Product",
            "footer_support": "Support",
            "footer_legal": "Links",
            "footer_docs": "Documentation",
            "footer_contact": "Contact",
            "footer_license": "License",
            "footer_rights": "© 2024 EasyLock. All rights reserved."
        },
        "TR": {
            // Navigation
            "nav_home": "Ana Sayfa",
            "nav_features": "Özellikler",
            "nav_how": "Nasıl Çalışır",
            "nav_faq": "S.S.S.",
            "btn_download": "Hemen İndir",

            // Hero
            "hero_badge": "AES-256 Şifreleme",
            "hero_title": "Dosyalarınızı Saniyeler İçinde Koruyun",
            "hero_desc": "EasyLock, dosyalarınızı doğrudan Bağlam Menüsü'nden şifrelemenin en hızlı ve en güvenli yoludur. Askeri düzeyde AES-256 şifreleme ile güçlendirilmiştir.",
            "btn_learn": "Daha Fazla Bilgi",
            "stat_encryption": "Şifreleme",
            "stat_speed": "Kilit Hızı",
            "stat_secure": "Güvenli",

            // Features
            "features_subtitle": "Dosyalarınızı güvende tutmak için ihtiyacınız olan her şey",
            "feat_fast_title": "Işık Hızında",
            "feat_fast_desc": "Optimize edilmiş performans, dosyalarınızın gecikme olmadan anında şifrelenmesini sağlar.",
            "feat_secure_title": "AES-256 Güvenliği",
            "feat_secure_desc": "Askeri düzeyde şifreleme, verilerinizi meraklı gözlerden uzak tutar. Sizin anahtarınız, sizin veriniz.",
            "feat_easy_title": "Kolay Entegrasyon",
            "feat_easy_desc": "Sistem kabuğuyla sorunsuz entegre edilmiştir. Şifrelemek için sadece sağ tıklayın.",
            "feat_smart_title": "Akıllı Kilit",
            "feat_smart_desc": "Ön ayarlı şifrenizi kullanarak anında kilitlemek/çözmek için Meta (Win/Cmd) tuşunu basılı tutun.",
            "feat_password_title": "Güvenli Depolama",
            "feat_password_desc": "Şifreler işletim sistemine özel güvenli alanlarda saklanır. Asla düz metin olarak tutulmaz.",
            "feat_startup_title": "Otomatik Başlatma",
            "feat_startup_desc": "Sistem tepsisinde sessizce çalışır. İhtiyacınız olduğunda her zaman hazırdır.",

            // Showcase
            "showcase_title": "Nasıl Çalışır",
            "showcase_desc": "Dosyalarınızı korumak için üç basit adım",
            "step_1": "Herhangi bir dosyaya veya klasöre sağ tıklayın",
            "step_2": "Menüden 'Lock File' seçeneğini seçin",
            "step_3": "Şifrenizi girin veya Ön Ayarlı modu kullanın",

            // FAQ
            "faq_title": "Sıkça Sorulan Sorular",
            "faq_subtitle": "EasyLock hakkında bilmeniz gereken her şey",
            "faq_q1": "Verilerim güvende mi?",
            "faq_a1": "Evet! EasyLock, AES-256 GCM şifreleme kullanır. Şifreleriniz sistem API'leri kullanılarak güvenli bir şekilde saklanır.",
            "faq_q2": "Şifremi unutursam ne olur?",
            "faq_a2": "Şifrelenmiş dosyalar doğru şifre olmadan kurtarılamaz. Bu, maksimum güvenlik sağlar. Bir şifre yöneticisi kullanmanızı öneririz.",
            "faq_q3": "Hangi platformlar destekleniyor?",
            "faq_a3": "EasyLock, Windows 10/11 ve Linux (Ubuntu 20.04+) ile uyumludur. Dosya yöneticileriyle sorunsuz entegre olur.",
            "faq_q4": "Şifreleme ne kadar hızlı?",
            "faq_a4": "EasyLock hız için optimize edilmiştir. Yaygın dosyalar modern sistemlerde bir saniyeden kısa sürede şifrelenir.",

            // Download
            "download_title": "Bugün Başlayın",
            "download_desc": "Dosyalarınızı saniyeler içinde korumaya başlayın. Ücretsiz ve açık kaynak.",
            "btn_download_windows": "Windows için İndir",
            "btn_download_linux": "Linux için İndir",

            // Footer
            "footer_tagline": "Güvenli dosya şifreleme artık çok kolay",
            "footer_product": "Ürün",
            "footer_support": "Destek",
            "footer_legal": "Bağlantılar",
            "footer_docs": "Belgeler",
            "footer_contact": "İletişim",
            "footer_license": "Lisans",
            "footer_rights": "© 2024 EasyLock. Tüm hakları saklıdır."
        }
    };

    // Language Selection
    let currentLang = "EN";
    const userLang = navigator.language || navigator.userLanguage;
    if (userLang.startsWith('tr')) {
        currentLang = "TR";
    }

    function applyTranslations() {
        document.querySelectorAll('[data-key]').forEach(el => {
            const key = el.getAttribute('data-key');
            if (translations[currentLang][key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = translations[currentLang][key];
                } else {
                    // Preserving inner icons if they exist
                    const icon = el.querySelector('i');
                    if (icon) {
                        el.childNodes.forEach(node => {
                            if (node.nodeType === 3) { // Text node
                                node.textContent = translations[currentLang][key];
                            }
                        });
                    } else {
                        el.textContent = translations[currentLang][key];
                    }
                }
            }
        });
        document.documentElement.lang = currentLang.toLowerCase();
    }

    applyTranslations();

    // Mobile Menu
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const menuOverlay = document.querySelector('.mobile-menu-overlay');
    const menuLinks = document.querySelectorAll('.mobile-nav a');

    function toggleMenu() {
        menuToggle.classList.toggle('active');
        menuOverlay.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    }

    menuToggle.addEventListener('click', toggleMenu);

    menuLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (menuOverlay.classList.contains('active')) {
                toggleMenu();
            }
        });
    });

    // Sticky Header
    const header = document.getElementById('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            faqItems.forEach(i => i.classList.remove('active'));
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});
