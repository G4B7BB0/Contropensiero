# Contropensiero

Un diario desktop privato per i pensieri che arrivano quando vogliono. Scegli Italiano o English all'avvio; il diario resta sul computer, senza account né cloud.

> È un vecchio progetto che ho ritrovato facendo pulizia. Non so neanche più bene come funzioni, ma resta mio. Probabilmente è anche un po' vibe-coded.

## Cosa fa

- Diario protetto da password e cifrato con AES-GCM; la password è derivata con scrypt.
- Salvataggio automatico sul dispositivo e blocco dopo dieci minuti di inattività.
- Raccolta con ricerca, calendario, etichette, preferiti e umore per pagina.
- Copie di sicurezza cifrate, ripristino e cambio password.
- Interfaccia desktop in italiano e inglese, con tema scuro caldo.
- Scorciatoie: `Ctrl + N` nuova pagina, `Ctrl + F` cerca, `Ctrl + S` salva, `Ctrl + L` blocca, `Ctrl + W` chiude la pagina aperta.

## Avvio

Serve Python 3.10 o successivo, Tkinter e pip.

**Windows**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

**macOS e Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Al primo avvio crea una password di almeno otto caratteri. La password non si può recuperare.

## Dati e privacy

Le pagine sono salvate in un file cifrato nella cartella dati utente: `%APPDATA%\Contropensiero\diario.enc` su Windows, `~/Library/Application Support/Contropensiero/diario.enc` su macOS e `~/.local/share/contropensiero/diario.enc` su Linux. La preferenza della lingua è salvata a parte in `settings.json`; non contiene dati del diario.

Il file personale del diario non fa parte di questo repository. Il blocco protegge il file cifrato; non protegge copie non cifrate o una sessione già sbloccata da chi può usare il tuo account di sistema.

## Tecnologie

Python, Tkinter, `cryptography` e `hashlib.scrypt`. La workflow GitHub Actions prepara build desktop per Windows, macOS e Linux.

## License

MIT. Vedi [LICENSE](LICENSE).
