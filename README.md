# Contropensiero

A private desktop diary for capturing thoughts, tracking moods, and revisiting old entries.

> I came across this old project while cleaning up. I can't quite remember how everything works anymore, and some parts may be a little vibe-coded.

## Features

- Password-protected diary encrypted with AES-GCM; the encryption key is derived with scrypt.
- Automatic local saves and a diary that locks after ten minutes of inactivity.
- Searchable collection with a calendar, tags, favorites, and a mood for each entry.
- Encrypted backups, restore, and password changes.
- Warm, dark desktop interface in Italian and English.
- Shortcuts: `Ctrl + N` new entry, `Ctrl + F` search, `Ctrl + S` save, `Ctrl + L` lock, `Ctrl + W` close the current entry.

## Getting started

Requires Python 3.10 or newer, Tkinter, and pip.

**Windows**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

**macOS and Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On first launch, create a password with at least eight characters. The password cannot be recovered.

## Data and privacy

Diary entries are stored in an encrypted file in your user data folder: `%APPDATA%\Contropensiero\diario.enc` on Windows, `~/Library/Application Support/Contropensiero/diario.enc` on macOS, and `~/.local/share/contropensiero/diario.enc` on Linux. Your language preference is saved separately in `settings.json` and contains no diary data.

Your personal diary file is not part of this repository. The lock protects the encrypted file; it does not protect unencrypted copies or an unlocked session from someone using your system account.

## Built with

Python, Tkinter, `cryptography`, and `hashlib.scrypt`. The GitHub Actions workflow builds desktop apps for Windows, macOS, and Linux.

## License

MIT. See [LICENSE](LICENSE).
