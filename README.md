# 💀 BruteX

**BruteX** is a Python-based brute force tool that tests SSH, FTP, and HTTP login pages using wordlists — built for CTF players and penetration testers.

> ⚠️ **Disclaimer:** This tool is for educational purposes and authorized testing only. Only use it on systems you own or have explicit written permission to test. Unauthorized use is illegal.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 SSH Brute Force | Tests SSH login with username/password wordlist |
| 📁 FTP Brute Force | Tests FTP login credentials |
| 🌐 HTTP Brute Force | Tests web login forms |
| 👥 Username List | Supports multiple usernames |
| ⚡ Fast | Optimized for speed |
| 📊 Rich Output | Beautiful terminal tables |

---

## 📦 Installation

```bash
git clone https://github.com/andersonphonom-ui/brutex.git
cd brutex
pip install -r requirements.txt --break-system-packages
sudo cp main.py banner.py /usr/local/bin/
sudo cp -r modules/ /usr/local/bin/modules/
sudo mv /usr/local/bin/main.py /usr/local/bin/brutex
sudo chmod +x /usr/local/bin/brutex
```

---

## 🚀 Usage

```bash
# SSH brute force
brutex -t 192.168.1.1 --service ssh -u root -w /usr/share/wordlists/rockyou.txt

# FTP brute force
brutex -t 192.168.1.1 --service ftp -u admin -w rockyou.txt

# HTTP brute force
brutex -t http://site.com/login --service http -u admin -w rockyou.txt

# Custom port
brutex -t 192.168.1.1 --service ssh --port 2222 -u root -w rockyou.txt

# Username list
brutex -t 192.168.1.1 --service ssh -U users.txt -w rockyou.txt

# HTTP with custom fields
brutex -t http://site.com/login --service http -u admin -w rockyou.txt --user-field email --pass-field pwd

# Help
brutex -h

# Version
brutex -v
```

---

## 📁 Project Structure

```
brutex/
├── main.py            # CLI entry point
├── banner.py          # ASCII art banner
├── requirements.txt
├── README.md
└── modules/
    ├── ssh_brute.py   # SSH attack module
    ├── ftp_brute.py   # FTP attack module
    └── http_brute.py  # HTTP attack module
```

---

## 👨‍💻 Author

**Youssef Mediouni**
- YouTube: [PH4nt0m CYber](https://youtube.com/@PH4nt0mCYber)
- GitHub: [@andersonphonom-ui](https://github.com/andersonphonom-ui)

---

## 📄 License

MIT License — free to use, modify, and distribute.
