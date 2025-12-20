document.addEventListener('DOMContentLoaded', () => {
    // Dil çevirileri
    const translations = {
        en: {
            pageTitle: "EasyLock | Secure Your Files with AES-256",
            metaDescription: "Secure your files on Windows and Linux with a single right-click. EasyLock uses AES-256 encryption to protect your data with manual or preset keys.",
            metaKeywords: "file encryption, AES-256, secure files, right-click encrypt, python, windows, linux, EasyLock",
            navHome: "Home",
            navAbout: "About Us",
            navProjects: "Projects",
            navDownload: "Download",
            navContact: "Contact & Donate",
            heroTitle: "EasyLock",
            heroSubtitle: "Secure Your Files with a Single Click.",
            heroDescription: "EasyLock integrates directly into your system's context menu (right-click menu), allowing you to encrypt and decrypt files instantly using powerful AES-256 encryption.",
            featuresTitle: "Key Features",
            feature1Title: "AES-256 Encryption",
            feature1Desc: "Military-grade encryption standard to keep your sensitive data safe.",
            feature2Title: "Seamless Integration",
            feature2Desc: "Encrypt/decrypt files directly from the right-click menu. No need to open an app.",
            feature3Title: "Flexible Keys",
            feature3Desc: "Use a manual key for one-time encryption or set a preset key for quick access.",
            feature4Title: "Cross-Platform",
            feature4Desc: "Works smoothly on both Windows and Linux systems.",
            howToTitle: "How It Works",
            step1: "Install EasyLock to add it to your right-click menu.",
            step2: "Set your optional preset key from the system tray icon.",
            step3: "Right-click any file and choose an encryption option.",
            downloadTitle: "Get EasyLock Now",
            downloadSubtitle: "Download the version compatible with your operating system.",
            downloadWindows: "Download for Windows (.exe)",
            downloadLinux: "Download for Linux (.py)",
            footerRights: "Xmer™ Digital Freedom and Ethical Technology Community"
        },
        tr: {
            pageTitle: "EasyLock | Dosyalarınızı AES-256 ile Koruyun",
            metaDescription: "Windows ve Linux'ta dosyalarınızı tek bir sağ tıklama ile güvence altına alın. EasyLock, verilerinizi manuel veya ön ayarlı anahtarlarla korumak için AES-256 şifrelemesi kullanır.",
            metaKeywords: "dosya şifreleme, AES-256, dosya güvenliği, sağ tıkla şifrele, python, windows, linux, EasyLock",
            navHome: "Anasayfa",
            navAbout: "Hakkımızda",
            navProjects: "Projeler",
            navDownload: "İndir",
            navContact: "İletişim & Bağış",
            heroTitle: "EasyLock",
            heroSubtitle: "Dosyalarınızı Tek Tıkla Güvenle Şifreleyin.",
            heroDescription: "EasyLock, doğrudan sisteminizin sağ tık menüsüne entegre olarak, güçlü AES-256 şifrelemesi kullanarak dosyaları anında şifrelemenize ve çözmenize olanak tanır.",
            featuresTitle: "Ana Özellikler",
            feature1Title: "AES-256 Şifreleme",
            feature1Desc: "Hassas verilerinizi güvende tutmak için askeri düzeyde şifreleme standardı.",
            feature2Title: "Sorunsuz Entegrasyon",
            feature2Desc: "Uygulama açmadan, dosyaları doğrudan sağ tık menüsünden şifreleyin/çözün.",
            feature3Title: "Esnek Anahtarlar",
            feature3Desc: "Tek seferlik şifreleme için manuel bir anahtar kullanın veya hızlı erişim için ön ayarlı bir anahtar belirleyin.",
            feature4Title: "Çapraz Platform",
            feature4Desc: "Hem Windows hem de Linux sistemlerinde sorunsuz çalışır.",
            howToTitle: "Nasıl Çalışır?",
            step1: "EasyLock'u sağ tık menünüze eklemek için kurun.",
            step2: "Sistem tepsisi ikonundan isteğe bağlı ön ayarlı anahtarınızı belirleyin.",
            step3: "Herhangi bir dosyaya sağ tıklayın ve bir şifreleme seçeneği seçin.",
            downloadTitle: "EasyLock'u Şimdi Edinin",
            downloadSubtitle: "İşletim sisteminizle uyumlu sürümü indirin.",
            downloadWindows: "Windows için İndir (.exe)",
            downloadLinux: "Linux için İndir (.py)",
            footerRights: "Xmer™ Dijital Özgürlük ve Etik Teknoloji Topluluğu"
        }
    };

    let currentLang = localStorage.getItem('language') || 'en';

    const langButtons = {
        tr: document.getElementById('lang-tr'),
        en: document.getElementById('lang-en')
    };

    function setLanguage(lang) {
        if (!translations[lang]) return;

        currentLang = lang;
        localStorage.setItem('language', lang);

        document.documentElement.lang = lang;
        document.title = translations[lang].pageTitle;
        document.querySelector('meta[name="description"]').setAttribute('content', translations[lang].metaDescription);
        document.querySelector('meta[name="keywords"]').setAttribute('content', translations[lang].metaKeywords);

        document.querySelectorAll('[data-translate-key]').forEach(el => {
            const key = el.getAttribute('data-translate-key');
            if (translations[lang][key]) {
                el.textContent = translations[lang][key];
            }
        });

        updateLangButtons();
    }

    function updateLangButtons() {
        if (currentLang === 'tr') {
            langButtons.tr.classList.add('bg-primary', 'text-white', 'dark:bg-primary-dark', 'dark:text-black');
            langButtons.tr.classList.remove('text-slate-500', 'dark:text-slate-400');
            langButtons.en.classList.remove('bg-primary', 'text-white', 'dark:bg-primary-dark', 'dark:text-black');
            langButtons.en.classList.add('text-slate-500', 'dark:text-slate-400');
        } else {
            langButtons.en.classList.add('bg-primary', 'text-white', 'dark:bg-primary-dark', 'dark:text-black');
            langButtons.en.classList.remove('text-slate-500', 'dark:text-slate-400');
            langButtons.tr.classList.remove('bg-primary', 'text-white', 'dark:bg-primary-dark', 'dark:text-black');
            langButtons.tr.classList.add('text-slate-500', 'dark:text-slate-400');
        }
    }

    langButtons.tr.addEventListener('click', () => setLanguage('tr'));
    langButtons.en.addEventListener('click', () => setLanguage('en'));

    // Mobil menü
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenuButton.addEventListener('click', () => {
        const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
        mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
        mobileMenu.classList.toggle('hidden');
    });

    // Yükleyiciyi gizle
    window.addEventListener('load', () => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500);
        }
    });
    
    // Sayfa ilk yüklendiğinde dili ayarla
    setLanguage(currentLang);
});