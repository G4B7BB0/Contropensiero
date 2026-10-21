"""Contropensiero — un diario personale che vive sul tuo computer."""

from __future__ import annotations

import base64
import calendar
import json
import os
import secrets
import sys
import tkinter as tk
from datetime import date, datetime
from pathlib import Path
from tkinter import filedialog, messagebox

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

APP_NAME = "Contropensiero"
VERSION = "1.1.0"
BG, PAPER, INK = "#201D1B", "#292522", "#F2E9DF"
MUTED, LINE = "#AA9B8D", "#413932"
ACCENT, ACCENT_DARK, GREEN, SOFT = "#D28A62", "#B96F4B", "#B4B38B", "#352D28"
FIELD, BODY_INK = "#332D28", "#E6D9CC"
GOLD, GOLD_FILL, GOLD_ACTIVE = "#E0BE63", "#514629", "#65552F"
DELETE_FILL, DELETE_INK, DELETE_ACTIVE = "#4B302B", "#E9A18E", "#624039"
TITLE_HINT = "Dai un titolo (facoltativo)"
FONT, SERIF = "Segoe UI", "Georgia"
MOODS = ("Scegli un umore", "Sereno", "Pensieroso", "Ispirato", "Stanco", "Grato")
MOOD_COLORS = {
    "Sereno": "#A9BC91",
    "Pensieroso": "#8FB5C4",
    "Ispirato": "#E0AE72",
    "Stanco": "#B4A0C7",
    "Grato": "#D88F83",
}
MONTHS = ("gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
          "agosto", "settembre", "ottobre", "novembre", "dicembre")
WEEKDAYS = ("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica")
MONTHS_EN = ("January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December")
WEEKDAYS_EN = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MOODS_EN = {
    "Scegli un umore": "Choose a mood", "Sereno": "Calm", "Pensieroso": "Thoughtful",
    "Ispirato": "Inspired", "Stanco": "Tired", "Grato": "Grateful",
}
EN = {
    "il tuo spazio, tutto tuo": "your own private space",
    "Tutto salvato sul tuo dispositivo": "Everything is saved on your device",
    "Uno spazio tutto tuo.": "A space of your own.",
    "Pensieri, appunti, cose da non perdere.": "Thoughts, notes, things worth keeping.",
    "Bentornato.": "Welcome back.",
    "Il tuo diario è cifrato e resta sul tuo computer.": "Your diary is encrypted and stays on your computer.",
    "Password": "Password",
    "Apri il diario": "Open your diary",
    "Crea la tua chiave": "Create your key",
    "Scegli una password che ricorderai: non può essere recuperata.": "Choose a password you can remember: it cannot be recovered.",
    "Password (almeno 8 caratteri)": "Password (at least 8 characters)",
    "Ripeti la password": "Repeat password",
    "Crea il diario": "Create diary",
    "NESSUN ACCOUNT  ·  NESSUN CLOUD  ·  I TUOI PENSIERI RESTANO TUOI": "NO ACCOUNT  ·  NO CLOUD  ·  YOUR THOUGHTS STAY YOURS",
    "Usa almeno 8 caratteri per la password.": "Use at least 8 characters for your password.",
    "Le due password non coincidono.": "The passwords do not match.",
    "Usa almeno 8 caratteri per la password.": "Use at least 8 characters for your password.",
    "Password non corretta. Il diario è ancora al sicuro.": "Incorrect password. Your diary is still safe.",
    "Non riesco ad aprire il diario: ": "Could not open the diary: ",
    "Non riesco a leggere la copia: ": "Could not read the backup: ",
    "La password deve contenere almeno 8 caratteri.": "The password must be at least 8 characters long.",
    "Le due password non coincidono. Riprova.": "The passwords do not match. Try again.",
    "Password non corretta. Il diario è ancora al sicuro.": "Incorrect password. Your diary is still safe.",
    "Blocca il diario": "Lock diary",
    "Sicurezza": "Security",
    "Sicurezza del diario": "Diary security",
    "Nuovo pensiero": "New thought",
    "Le tue pagine": "Your pages",
    "Calendario": "Calendar",
    "Cerca tra i pensieri…": "Search your thoughts…",
    "Azzera": "Clear",
    "☆  Mostra preferiti": "☆  Show favorites",
    "Tutte le pagine": "All pages",
    "Ctrl N   nuovo pensiero": "Ctrl N   new thought",
    "Ctrl F   cerca": "Ctrl F   search",
    "Ctrl S   salva ora": "Ctrl S   save now",
    "Ctrl L   blocca il diario": "Ctrl L   lock diary",
    "Ctrl W   chiudi pagina": "Ctrl W   close page",
    "Nessuna pagina trovata.\nProva un’altra parola.": "No pages found.\nTry another word.",
    "Nessuna pagina per questo giorno.\nProva un’altra data.": "No pages for this day.\nTry another date.",
    "Ancora nessun preferito.\nAggiungi una stella alle tue pagine.": "No favorites yet.\nAdd a star to a page.",
    "Ancora nessun pensiero.\nPuoi cominciare da qui.": "No thoughts yet.\nYou can start here.",
    "Senza titolo": "Untitled",
    "Una pagina ancora da riempire…": "A page waiting to be filled…",
    "Filtro  ·  ": "Filter  ·  ",
    "●  Giorno con pagine": "●  Day with pages",
    "Tutte le date": "All dates",
    "Cambia password": "Change password",
    "Scegli una nuova chiave per proteggere il diario.": "Choose a new key to protect your diary.",
    "Nuova password": "New password",
    "Ripeti la nuova password": "Repeat new password",
    "Almeno 8 caratteri · le due password devono coincidere.": "At least 8 characters · both passwords must match.",
    "La password deve contenere almeno 8 caratteri.": "The password must be at least 8 characters long.",
    "Le due password non coincidono. Riprova.": "The passwords do not match. Try again.",
    "Annulla": "Cancel",
    "Aggiorna password": "Update password",
    "Modifica non riuscita": "Update failed",
    "Password aggiornata": "Password updated",
    "Da ora usa la nuova password per aprire il diario.": "Use your new password to open the diary from now on.",
    "Crea copia cifrata": "Create encrypted backup",
    "Esporta un file protetto": "Export a protected file",
    "Ripristina da una copia": "Restore from backup",
    "Sostituisce le pagine attuali": "Replaces the current pages",
    "Scegli una nuova chiave": "Choose a new key",
    "Salva una copia cifrata": "Save an encrypted backup",
    "Copia cifrata Contropensiero": "Contropensiero encrypted backup",
    "Tutti i file": "All files",
    "Copia di sicurezza": "Backup",
    "Il diario è già salvato in questo file.": "Your diary is already saved in this file.",
    "Copia non riuscita": "Backup failed",
    "Copia cifrata creata": "Encrypted backup created",
    "Calendario delle pagine": "Pages calendar",
    "Scegli una copia cifrata": "Choose an encrypted backup",
    "Copia non valida": "Invalid backup",
    "La copia non corrisponde a questa password o è danneggiata.": "This backup does not match your password or is damaged.",
    "Non riesco a leggere la copia: ": "Could not read the backup: ",
    "Copia non valida": "Invalid backup",
    "Ripristinare la copia?": "Restore this backup?",
    "Le pagine attuali verranno sostituite con quelle della copia.\n\nVuoi continuare?": "Your current pages will be replaced with the backup.\n\nContinue?",
    "Le tue pagine sono al sicuro.": "Your pages are safe.",
    "Scegline una dall’elenco o apri una nuova pagina.": "Choose one from the list or open a new page.",
    "C’è spazio per quello che ti passa per la testa.": "There is room for whatever is on your mind.",
    "Una frase, un appunto, un pensiero senza un perché.": "A sentence, a note, a thought without a reason.",
    "Scrivi il primo": "Write the first one",
    "Elimina pagina": "Delete page",
    "★  Nei preferiti": "★  In favorites",
    "☆  Aggiungi ai preferiti": "☆  Add to favorites",
    "Chiudi": "Close",
    "Oggi mi sento": "Today I feel",
    "ETICHETTE · separate da virgole": "TAGS · separated by commas",
    "Dai un titolo (facoltativo)": "Give it a title (optional)",
    "Salvato sul dispositivo": "Saved on your device",
    "Umore della pagina": "Page mood",
    "Modifiche in corso…": "Saving changes…",
    "parole": "words",
    "parola": "word",
    "caratteri": "characters",
    "pagine": "pages",
    "pagina": "page",
    "Eliminare questa pagina?": "Delete this page?",
    "«": "“",
    "» verrà rimossa dal diario.\n\nQuesta azione non si può annullare.": "” will be removed from your diary.\n\nThis action cannot be undone.",
    "Questa azione non si può annullare.": "This action cannot be undone.",
    "Dai un titolo (facoltativo)": "Give it a title (optional)",
    "Modifiche in corso…": "Saving changes…",
    "Salvato ·": "Saved ·",
    "Vuoi davvero eliminare": "Are you sure you want to delete",
    "Questa azione non può essere annullata.": "This action cannot be undone.",
    "Scegli un umore": "Choose a mood",
    "Filtro  ·  ": "Filter  ·  ",
    "Nessuna pagina con il tag #": "No pages with the tag #",
    "Le pagine attuali verranno sostituite con quelle della copia.\n\nVuoi continuare?": "Your current pages will be replaced with the backup.\n\nContinue?",
    "La pagina ": "The page ",
    " è stata eliminata.": " has been deleted.",
}
AAD = b"contropensiero-v1"


def normalize_tags(value) -> list[str]:
    raw = value if isinstance(value, list) else str(value or "").split(",")
    cleaned, seen = [], set()
    for part in raw:
        tag = str(part).strip().lstrip("#").strip()
        key = tag.casefold()
        if tag and key not in seen:
            cleaned.append(tag[:28])
            seen.add(key)
    return cleaned


def tint_color(base: str, tint: str, amount: float) -> str:
    """Blend a mood accent into a dark surface without reducing text contrast."""
    base_rgb = tuple(int(base[index:index + 2], 16) for index in (1, 3, 5))
    tint_rgb = tuple(int(tint[index:index + 2], 16) for index in (1, 3, 5))
    mixed = tuple(round(left * (1 - amount) + right * amount)
                  for left, right in zip(base_rgb, tint_rgb))
    return "#" + "".join(f"{channel:02X}" for channel in mixed)


def vault_path() -> Path:
    if sys.platform == "win32":
        folder = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Contropensiero"
    elif sys.platform == "darwin":
        folder = Path.home() / "Library" / "Application Support" / "Contropensiero"
    else:
        folder = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "contropensiero"
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        folder.chmod(0o700)
    return folder / "diario.enc"


def derive_key(password: str, salt: bytes) -> bytes:
    import hashlib
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)


def encrypt_vault(password: str, entries: list[dict]) -> bytes:
    salt, nonce = secrets.token_bytes(16), secrets.token_bytes(12)
    plaintext = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ciphertext = AESGCM(derive_key(password, salt)).encrypt(nonce, plaintext, AAD)
    envelope = {"version": 1, "salt": base64.b64encode(salt).decode(),
                "nonce": base64.b64encode(nonce).decode(), "data": base64.b64encode(ciphertext).decode()}
    return json.dumps(envelope, separators=(",", ":")).encode()


def decrypt_vault(password: str, raw: bytes) -> list[dict]:
    envelope = json.loads(raw)
    if envelope.get("version") != 1:
        raise ValueError("Versione del diario non supportata.")
    salt, nonce = base64.b64decode(envelope["salt"]), base64.b64decode(envelope["nonce"])
    ciphertext = base64.b64decode(envelope["data"])
    plaintext = AESGCM(derive_key(password, salt)).decrypt(nonce, ciphertext, AAD)
    entries = json.loads(plaintext.decode("utf-8"))
    if not isinstance(entries, list):
        raise ValueError("Il formato del diario non è valido.")
    return entries


def date_label(iso: str, *, weekday: bool = False, language: str = "it") -> str:
    dt = datetime.fromisoformat(iso)
    months = MONTHS_EN if language == "en" else MONTHS
    weekdays = WEEKDAYS_EN if language == "en" else WEEKDAYS
    if weekday:
        if months is MONTHS_EN:
            return f"{weekdays[dt.weekday()]} {months[dt.month - 1]} {dt.day}, {dt.year}"
        return f"{weekdays[dt.weekday()].capitalize()} {dt.day} {months[dt.month - 1]} {dt.year}"
    return f"{months[dt.month - 1]} {dt.day}, {dt.year}" if months is MONTHS_EN else f"{dt.day:02d} {months[dt.month - 1]} {dt.year}"


class Contropensiero:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.path = vault_path()
        self.settings_path = self.path.parent / "settings.json"
        try:
            self.language = json.loads(self.settings_path.read_text(encoding="utf-8")).get("language", "it")
        except (OSError, ValueError, AttributeError):
            self.language = "it"
        if self.language not in ("it", "en"):
            self.language = "it"
        self.entries: list[dict] = []
        self.password: str | None = None
        self.selected_id: str | None = None
        self.autosave_job = None
        self.lock_job = None
        self.dirty = False
        self.favorite_only = False
        self.selected_date: date | None = None
        self.selected_tag: str | None = None
        self.calendar_dialog = None
        self.active_popup = None
        self.popup_anchor = None
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Tutto salvato sul tuo dispositivo")
        self.root.title(f"{APP_NAME} · {self.tr('il tuo spazio, tutto tuo')}")
        self.root.geometry("1120x760")
        self.root.minsize(880, 620)
        self.root.resizable(True, True)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.option_add("*Font", (FONT, 10))
        for event in ("<KeyPress>", "<Button-1>", "<MouseWheel>"):
            self.root.bind_all(event, self.on_activity, add="+")
        self.root.bind_all("<Button-1>", self.dismiss_popup_if_outside, add="+")
        self.show_lock_screen()

    def clear(self):
        for child in self.root.winfo_children():
            child.destroy()

    def label(self, parent, text, *, size=10, color=INK, family=FONT, weight="normal", **kw):
        return tk.Label(parent, text=self.tr(text), font=(family, size, weight),
                        bg=kw.pop("bg", parent.cget("bg")), fg=color, **kw)

    def tr(self, text):
        if self.language != "en" or not isinstance(text, str):
            return text
        return EN.get(text, text)

    def mood_text(self, mood):
        return MOODS_EN.get(mood, mood) if self.language == "en" else mood

    def title_hint(self):
        return "Give it a title (optional)" if self.language == "en" else TITLE_HINT

    def choose_language(self, language):
        if language == self.language:
            return
        if self.password is not None:
            self.save_current()
        self.language = language
        self.root.title(f"{APP_NAME} · {self.tr('il tuo spazio, tutto tuo')}")
        try:
            self.settings_path.write_text(
                json.dumps({"language": language}, ensure_ascii=False), encoding="utf-8"
            )
        except OSError:
            pass
        if self.password is None:
            self.show_lock_screen()
        else:
            self.show_main()

    def button(self, parent, text, command, *, primary=False, danger=False, gold=False,
               lock_action=False, **kw):
        if primary:
            bg, fg, active_bg = ACCENT, "#FFFFFF", ACCENT_DARK
        elif danger:
            bg, fg, active_bg = DELETE_FILL, DELETE_INK, DELETE_ACTIVE
        elif gold:
            bg, fg, active_bg = GOLD_FILL, GOLD, GOLD_ACTIVE
        elif lock_action:
            bg, fg, active_bg = FIELD, ACCENT, SOFT
        else:
            bg, fg, active_bg = PAPER, INK, SOFT
        return tk.Button(parent, text=self.tr(text), command=command, bg=bg, fg=fg,
                         activebackground=active_bg, activeforeground=fg,
                         relief="flat", bd=0, padx=15 if primary else 12, pady=9, cursor="hand2",
                         font=(FONT, 10, "bold" if primary or lock_action else "normal"),
                         highlightthickness=0 if primary else 1,
                         highlightbackground=ACCENT if lock_action else LINE, **kw)

    def dropdown_button(self, parent, text, command, *, color=GREEN):
        return tk.Button(
            parent, text=f"{self.tr(text)}   ⌄", command=command,
            bg=FIELD, fg=color, activebackground=SOFT, activeforeground=INK,
            relief="flat", bd=0, padx=13, pady=9, cursor="hand2",
            font=(FONT, 10, "bold"), highlightthickness=1, highlightbackground=LINE,
        )

    def show_styled_menu(self, anchor, heading, items, *, width=270):
        if self.active_popup is not None:
            same_anchor = self.popup_anchor is anchor
            self.close_styled_menu()
            if same_anchor:
                return
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.withdraw()
        popup.transient(self.root)
        popup.configure(bg=LINE)
        self.active_popup = popup
        self.popup_anchor = anchor

        shell = tk.Frame(popup, bg=LINE, padx=1, pady=1)
        shell.pack(fill="both", expand=True)
        panel = tk.Frame(shell, bg=PAPER)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text=self.tr(heading).upper(), bg=PAPER, fg=GREEN,
                 font=(FONT, 8, "bold"), anchor="w").pack(fill="x", padx=14, pady=(12, 8))
        for item in items:
            if item is None:
                tk.Frame(panel, bg=LINE, height=1).pack(fill="x", padx=12, pady=5)
                continue
            selected = item.get("selected", False)
            row = tk.Frame(panel, bg=PAPER, cursor="hand2", padx=10, pady=8)
            row.pack(fill="x", padx=5, pady=1)
            mark = tk.Label(row, text=item.get("icon", "·"), width=2, bg=PAPER,
                            fg=item.get("icon_color", GOLD if selected else MUTED),
                            font=(SERIF, 12, "bold"))
            mark.pack(side="left", padx=(2, 8))
            copy = tk.Frame(row, bg=PAPER)
            copy.pack(side="left", fill="x", expand=True)
            title = tk.Label(copy, text=self.tr(item["label"]), bg=PAPER,
                             fg=item.get("label_color", GOLD if selected else INK),
                             font=(FONT, 10, "bold"),
                             anchor="w")
            title.pack(fill="x")
            detail = item.get("detail")
            subtitle = None
            if detail:
                subtitle = tk.Label(copy, text=detail, bg=PAPER, fg=MUTED,
                                    font=(FONT, 8), anchor="w")
                subtitle.pack(fill="x", pady=(2, 0))
            widgets = [row, mark, copy, title]
            if subtitle is not None:
                widgets.append(subtitle)

            def hover(_event, color, row=row, mark=mark, copy=copy, title=title, subtitle=subtitle):
                for widget in (row, mark, copy, title, subtitle):
                    if widget is not None:
                        widget.configure(bg=color)

            def invoke(_event, action=item["command"]):
                self.close_styled_menu()
                self.root.after_idle(action)

            for widget in widgets:
                widget.bind("<Enter>", lambda event, h=hover: h(event, SOFT))
                widget.bind("<Leave>", lambda event, h=hover: h(event, PAPER))
                widget.bind("<Button-1>", invoke)

        popup.bind("<Escape>", lambda _event: self.close_styled_menu())
        popup.update_idletasks()
        x = anchor.winfo_rootx() + anchor.winfo_width() - width
        y = anchor.winfo_rooty() + anchor.winfo_height() + 6
        x = max(8, min(x, popup.winfo_screenwidth() - width - 8))
        height = popup.winfo_reqheight()
        if y + height > popup.winfo_screenheight() - 12:
            y = max(8, anchor.winfo_rooty() - height - 6)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.deiconify()
        popup.update_idletasks()
        # Some Windows window managers first map an overrideredirect Toplevel
        # at (0, 0); reapply the anchor position after it has been mapped.
        popup.geometry(f"+{x}+{y}")
        def place_popup():
            if not popup.winfo_exists() or not anchor.winfo_exists():
                return
            px = anchor.winfo_rootx() + anchor.winfo_width() - width
            py = anchor.winfo_rooty() + anchor.winfo_height() + 6
            px = max(8, min(px, popup.winfo_screenwidth() - width - 8))
            if py + popup.winfo_height() > popup.winfo_screenheight() - 12:
                py = max(8, anchor.winfo_rooty() - popup.winfo_height() - 6)
            popup.geometry(f"+{px}+{py}")
            popup.lift()
        popup.after(80, place_popup)
        popup.lift()
        popup.focus_force()

    def close_styled_menu(self):
        popup, self.active_popup = self.active_popup, None
        self.popup_anchor = None
        if popup is not None:
            try:
                popup.destroy()
            except tk.TclError:
                pass

    @staticmethod
    def _inside_widget(widget, ancestor):
        while widget is not None:
            if widget is ancestor:
                return True
            widget = getattr(widget, "master", None)
        return False

    def dismiss_popup_if_outside(self, event):
        if self.active_popup is None:
            return
        if self._inside_widget(event.widget, self.active_popup):
            return
        if self.popup_anchor is not None and self._inside_widget(event.widget, self.popup_anchor):
            return
        self.close_styled_menu()

    def brand(self, parent, *, big=False):
        row = tk.Frame(parent, bg=parent.cget("bg"))
        tk.Label(row, text="c.", font=(SERIF, 28 if big else 23, "bold"),
                 fg=ACCENT, bg=parent.cget("bg")).pack(side="left", padx=(0, 8))
        tk.Label(row, text="CONTROPENSIERO", font=(FONT, 12 if big else 10, "bold"),
                 fg=INK, bg=parent.cget("bg")).pack(side="left")
        row.pack(anchor="w")
        return row

    def show_lock_screen(self):
        self.clear()
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True)
        center = tk.Frame(frame, bg=BG)
        center.place(relx=.5, rely=.48, anchor="center")
        self.brand(center, big=True)
        language_row = tk.Frame(center, bg=BG)
        language_row.pack(anchor="e", pady=(0, 8))
        self.button(language_row, "Italiano" + ("  ✓" if self.language == "it" else ""),
                    lambda: self.choose_language("it"), gold=self.language == "it").pack(side="left", padx=(0, 6))
        self.button(language_row, "English" + ("  ✓" if self.language == "en" else ""),
                    lambda: self.choose_language("en"), gold=self.language == "en").pack(side="left")
        self.label(center, "Uno spazio tutto tuo.", size=31, family=SERIF).pack(anchor="w", pady=(34, 5))
        self.label(center, "Pensieri, appunti, cose da non perdere.", size=12, color=MUTED).pack(anchor="w")
        card = tk.Frame(center, bg=PAPER, highlightbackground=LINE, highlightthickness=1, padx=28, pady=24)
        card.pack(fill="x", pady=(28, 0))
        if self.path.exists():
            self.label(card, "Bentornato.", size=16, family=SERIF).pack(anchor="w")
            self.label(card, "Il tuo diario è cifrato e resta sul tuo computer.",
                       color=MUTED).pack(anchor="w", pady=(5, 18))
            self.lock_entry = self.make_password_input(card, "Password")
            self.lock_entry.bind("<Return>", lambda _e: self.unlock())
            self.button(card, "Apri il diario", self.unlock, primary=True).pack(fill="x", pady=(1, 0))
        else:
            self.label(card, "Crea la tua chiave", size=16, family=SERIF).pack(anchor="w")
            self.label(card, "Scegli una password che ricorderai: non può essere recuperata.",
                       color=MUTED, wraplength=360, justify="left").pack(anchor="w", pady=(5, 18))
            self.lock_entry = self.make_password_input(card, "Password (almeno 8 caratteri)")
            self.confirm_entry = self.make_password_input(card, "Ripeti la password")
            self.confirm_entry.bind("<Return>", lambda _e: self.create_vault())
            self.button(card, "Crea il diario", self.create_vault, primary=True).pack(fill="x")
        self.error_label = self.label(center, "", color=ACCENT, size=9)
        self.error_label.pack(anchor="w", pady=(10, 0))
        self.label(frame, "NESSUN ACCOUNT  ·  NESSUN CLOUD  ·  I TUOI PENSIERI RESTANO TUOI",
                   size=8, color=MUTED).place(relx=.5, rely=.96, anchor="center")
        self.lock_entry.focus_set()

    def make_password_input(self, parent, placeholder):
        self.label(parent, placeholder, size=9, color=MUTED).pack(anchor="w", pady=(0, 6))
        entry = tk.Entry(parent, show="•", font=(FONT, 11), bg=FIELD, fg=INK,
                         relief="flat", bd=0, highlightthickness=1, highlightbackground=LINE,
                         highlightcolor=GREEN, insertbackground=INK)
        entry.pack(fill="x", ipady=10, pady=(0, 15))
        return entry

    def create_vault(self):
        password, confirm = self.lock_entry.get(), self.confirm_entry.get()
        if len(password) < 8:
            self.error_label.config(text=self.tr("Usa almeno 8 caratteri per la password."))
            return
        if password != confirm:
            self.error_label.config(text=self.tr("Le due password non coincidono."))
            return
        self.password, self.entries = password, []
        self.persist()
        self.show_main()

    def unlock(self):
        try:
            password = self.lock_entry.get()
            self.entries = decrypt_vault(password, self.path.read_bytes())
            self.password = password
        except InvalidTag:
            self.error_label.config(text=self.tr("Password non corretta. Il diario è ancora al sicuro."))
            self.lock_entry.focus_set()
            return
        except Exception as exc:
            self.error_label.config(text=f"{self.tr('Non riesco ad aprire il diario: ')}{exc}")
            return
        self.show_main()

    def persist(self):
        if not self.password:
            return
        payload = encrypt_vault(self.password, self.entries)
        temp = self.path.with_name(f".{self.path.name}.{secrets.token_hex(6)}.tmp")
        try:
            with temp.open("xb") as stream:
                stream.write(payload)
            if os.name != "nt":
                temp.chmod(0o600)
            os.replace(temp, self.path)
        except OSError:
            temp.unlink(missing_ok=True)
            raise
        self.status_var.set(f"{self.tr('Salvato ·')}{datetime.now().strftime('%H:%M')}")

    def show_main(self):
        self.clear()
        self.selected_date = None
        self.selected_tag = None
        self.root.bind("<Control-n>", lambda _e: self.new_entry() if self.password is not None else None)
        self.root.bind("<Control-f>", lambda _e: self.search_box.focus_set() if self.password is not None else None)
        self.root.bind("<Control-s>", lambda _e: self.save_current() if self.password is not None else None)
        self.root.bind("<Control-l>", lambda _e: self.lock())
        self.root.bind("<Control-w>", self.close_current_entry)
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=28, pady=22)
        header = tk.Frame(outer, bg=BG)
        header.pack(fill="x", pady=(0, 22))
        self.brand(header)
        self.button(header, "▣  Blocca il diario", self.lock,
                    lock_action=True).pack(side="right", padx=(0, 3))
        self.security_button = self.dropdown_button(
            header, "Sicurezza", self.show_security_options, color=GREEN)
        self.security_button.pack(side="right", padx=(0, 9))
        self.button(header, "+  Nuovo pensiero", self.new_entry, primary=True).pack(side="right", padx=(0, 9))

        content = tk.Frame(outer, bg=BG)
        content.pack(fill="both", expand=True)
        sidebar = tk.Frame(content, bg=BG, width=290)
        sidebar.pack(side="left", fill="y", padx=(0, 22))
        sidebar.pack_propagate(False)
        now = datetime.now()
        weekdays = WEEKDAYS_EN if self.language == "en" else WEEKDAYS
        months = MONTHS_EN if self.language == "en" else MONTHS
        self.label(sidebar, weekdays[now.weekday()].capitalize(), size=12, color=MUTED).pack(anchor="w", pady=(4, 0))
        sidebar_date = f"{months[now.month - 1]} {now.day}" if self.language == "en" else f"{now.day} {months[now.month - 1]}"
        self.label(sidebar, sidebar_date, size=27, family=SERIF).pack(anchor="w")
        pages_heading = tk.Frame(sidebar, bg=BG)
        pages_heading.pack(fill="x", pady=(20, 8))
        self.label(pages_heading, "Le tue pagine", size=10, color=MUTED).pack(side="left")
        self.button(pages_heading, "▦ Calendario", self.open_calendar).pack(side="right", pady=0)
        self.search_var.set("")
        search = tk.Entry(sidebar, textvariable=self.search_var, font=(FONT, 10), bg=PAPER, fg=MUTED,
                          relief="flat", highlightthickness=1, highlightbackground=LINE,
                          highlightcolor=GREEN, insertbackground=INK)
        search.pack(fill="x", ipady=9, pady=(0, 10))
        search.insert(0, self.tr("Cerca tra i pensieri…"))
        search.bind("<FocusIn>", lambda _e: self.clear_search_hint(search))
        search.bind("<FocusOut>", lambda _e: self.restore_search_hint(search))
        search.bind("<KeyRelease>", lambda _e: self.refresh_list())
        self.search_box = search
        self.results_label = self.label(sidebar, "", size=8, color=MUTED)
        self.results_label.pack(anchor="w", pady=(0, 8))
        self.filter_status_row = tk.Frame(sidebar, bg=BG)
        self.filter_status_label = self.label(self.filter_status_row, "", size=8, color=ACCENT,
                                              wraplength=210, justify="left")
        self.filter_status_label.pack(side="left", fill="x", expand=True, anchor="w")
        self.clear_filter_button = self.button(
            self.filter_status_row, "Azzera", self.clear_collection_filters)
        self.filter_button = self.button(sidebar, "☆  Mostra preferiti", self.toggle_favorites, gold=True)
        self.filter_button.pack(fill="x", pady=(0, 10))
        list_area = tk.Frame(sidebar, bg=BG)
        list_area.pack(fill="both", expand=True)
        self.list_canvas = tk.Canvas(list_area, bg=BG, bd=0, highlightthickness=0)
        list_scrollbar = tk.Scrollbar(list_area, orient="vertical", command=self.list_canvas.yview,
                                      bg=SOFT, troughcolor=BG, activebackground=ACCENT,
                                      relief="flat", bd=0, width=8)
        self.list_canvas.configure(yscrollcommand=list_scrollbar.set)
        self.list_frame = tk.Frame(self.list_canvas, bg=BG)
        self.list_window = self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_frame.bind("<Configure>", lambda _e: self.list_canvas.configure(
            scrollregion=self.list_canvas.bbox("all")))
        self.list_canvas.bind("<Configure>", lambda event: self.list_canvas.itemconfigure(
            self.list_window, width=event.width))
        self.list_canvas.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        foot = tk.Frame(sidebar, bg=BG)
        foot.pack(fill="x", pady=(10, 0))
        tk.Frame(foot, bg=LINE, height=1).pack(fill="x", pady=(0, 12))
        self.label(foot, "Ctrl N   nuovo pensiero", size=8, color=MUTED).pack(anchor="w")
        self.label(foot, "Ctrl F   cerca", size=8, color=MUTED).pack(anchor="w", pady=(4, 0))
        self.label(foot, "Ctrl S   salva ora", size=8, color=MUTED).pack(anchor="w", pady=(4, 0))
        self.label(foot, "Ctrl L   blocca il diario", size=8, color=MUTED).pack(anchor="w", pady=(4, 0))
        self.label(foot, "Ctrl W   chiudi pagina", size=8, color=MUTED).pack(anchor="w", pady=(4, 0))
        self.editor_shell = tk.Frame(content, bg=PAPER, highlightbackground=LINE, highlightthickness=1)
        self.editor_shell.pack(side="left", fill="both", expand=True)
        self.refresh_list()
        if self.entries:
            first = sorted(self.entries, key=lambda e: e.get("updated", ""), reverse=True)[0]
            self.select_entry(first["id"])
        else:
            self.show_empty_editor()
        self.reset_lock_timer()

    def clear_search_hint(self, entry):
        if entry.get() == self.tr("Cerca tra i pensieri…"):
            entry.delete(0, "end")
            entry.config(fg=INK)

    def restore_search_hint(self, entry):
        if not entry.get():
            entry.insert(0, self.tr("Cerca tra i pensieri…"))
            entry.config(fg=MUTED)

    def refresh_list(self):
        if not hasattr(self, "list_frame") or not self.list_frame.winfo_exists():
            return
        for child in self.list_frame.winfo_children():
            child.destroy()
        query = self.search_var.get().strip().lower()
        if query == self.tr("Cerca tra i pensieri…").lower():
            query = ""
        rows = sorted(self.entries, key=lambda e: (bool(e.get("favorite")), e.get("updated", "")), reverse=True)
        if self.favorite_only:
            rows = [e for e in rows if e.get("favorite", False)]
        if self.selected_date:
            rows = [e for e in rows
                    if datetime.fromisoformat(e.get("created", e.get("updated"))).date() == self.selected_date]
        if self.selected_tag:
            tag_key = self.selected_tag.casefold()
            rows = [e for e in rows
                    if any(tag.casefold() == tag_key for tag in normalize_tags(e.get("tags", [])))]
        if query:
            rows = [e for e in rows if query in (
                e.get("title", "") + " " + e.get("body", "") + " " + e.get("mood", "")
                + " " + " ".join(normalize_tags(e.get("tags", [])))
            ).lower()]
        self.update_filter_status()
        count = len(rows)
        page_word = ("pages" if count != 1 else "page") if self.language == "en" else ("pagine" if count != 1 else "pagina")
        self.results_label.config(text=f"{count} {page_word}")
        if not rows:
            if query:
                message = "Nessuna pagina trovata.\nProva un’altra parola."
            elif self.selected_date:
                message = "Nessuna pagina per questo giorno.\nProva un’altra data."
            elif self.selected_tag:
                message = f"{self.tr('Nessuna pagina con il tag #')}{self.selected_tag}."
            elif self.favorite_only:
                message = "Ancora nessun preferito.\nAggiungi una stella alle tue pagine."
            else:
                message = "Ancora nessun pensiero.\nPuoi cominciare da qui."
            self.label(self.list_frame, message,
                       size=10, color=MUTED, justify="left", wraplength=250).pack(anchor="w", pady=18)
        for item in rows:
            active = item["id"] == self.selected_id
            mood = item.get("mood", MOODS[0])
            mood_color = MOOD_COLORS.get(mood)
            base_surface = SOFT if active else BG
            surface = tint_color(base_surface, mood_color, 0.20 if active else 0.11) \
                if mood_color else base_surface
            card = tk.Frame(self.list_frame, bg=surface, cursor="hand2")
            card.pack(fill="x", pady=2)
            accent = tk.Frame(card, bg=mood_color or LINE, width=3)
            accent.pack(side="left", fill="y")
            pad = tk.Frame(card, bg=surface)
            pad.pack(side="left", fill="both", expand=True, padx=(10, 6), pady=9)
            title_text = item.get("title", "")[:33] or self.tr("Senza titolo")
            if item.get("favorite"):
                title_text = "★  " + title_text
            self.label(pad, title_text, size=10, color=GOLD if item.get("favorite") else INK,
                       weight="bold" if active else "normal", anchor="w").pack(fill="x")
            preview = " ".join(item.get("body", "").split())[:62] or self.tr("Una pagina ancora da riempire…")
            self.label(pad, preview, size=8, color=MUTED, anchor="w").pack(fill="x", pady=(3, 0))
            ts = datetime.fromisoformat(item.get("updated", item["created"]))
            months = MONTHS_EN if self.language == "en" else MONTHS
            date_text = f"{months[ts.month - 1]} {ts.day}" if self.language == "en" else f"{ts.day:02d} {months[ts.month - 1]}"
            self.label(pad, f"{date_text}  ·  {ts:%H:%M}",
                       size=8, color=ACCENT if active else MUTED).pack(anchor="w", pady=(5, 0))
            if item.get("mood") and item["mood"] != MOODS[0]:
                self.label(pad, f"●  {self.mood_text(item['mood'])}", size=8,
                           color=mood_color or GREEN).pack(anchor="w", pady=(3, 0))
            tags = normalize_tags(item.get("tags", []))
            if tags:
                tag_row = tk.Frame(pad, bg=surface)
                tag_row.pack(fill="x", pady=(5, 0))
                for tag in tags[:4]:
                    tag_chip = tk.Label(
                        tag_row, text=f"#{tag}", bg=tint_color(surface, mood_color or GREEN, 0.22),
                        fg=mood_color or GREEN, font=(FONT, 7, "bold"), padx=6, pady=3,
                        cursor="hand2",
                    )
                    tag_chip.pack(side="left", padx=(0, 4))
                    tag_chip.bind("<Button-1>",
                                  lambda _e, value=tag: self.filter_by_tag(value) or "break")
                if len(tags) > 4:
                    self.label(tag_row, f"+{len(tags) - 4}", size=7, color=MUTED).pack(side="left")
            for widget in (card, accent, pad, *pad.winfo_children()):
                widget.bind("<Button-1>", lambda _e, eid=item["id"]: self.select_entry(eid))

    def update_filter_status(self):
        parts = []
        if self.selected_date:
            parts.append(date_label(self.selected_date.isoformat(), language=self.language))
        if self.selected_tag:
            parts.append(f"#{self.selected_tag}")
        if parts:
            self.filter_status_label.config(text=self.tr("Filtro  ·  ") + "  ·  ".join(parts))
            if not self.filter_status_row.winfo_manager():
                self.filter_status_row.pack(fill="x", pady=(0, 8), before=self.filter_button)
            if not self.clear_filter_button.winfo_manager():
                self.clear_filter_button.pack(side="right", padx=(5, 0))
        else:
            self.filter_status_row.pack_forget()

    def clear_collection_filters(self):
        self.selected_date = None
        self.selected_tag = None
        self.refresh_list()

    def filter_by_tag(self, tag):
        if self.selected_id:
            self.save_current()
        self.selected_date = None
        self.selected_tag = tag
        self.refresh_list()
        matches = [e for e in self.entries
                   if any(value.casefold() == tag.casefold()
                          for value in normalize_tags(e.get("tags", [])))]
        if matches:
            target = self.selected_id if any(e["id"] == self.selected_id for e in matches) else \
                max(matches, key=lambda e: e.get("updated", ""))["id"]
            self.select_entry(target)

    def open_calendar(self):
        if self.calendar_dialog is not None and self.calendar_dialog.winfo_exists():
            self.calendar_dialog.lift()
            return
        reference = self.selected_date or date.today()
        self.calendar_year, self.calendar_month = reference.year, reference.month
        dialog = tk.Toplevel(self.root)
        self.calendar_dialog = dialog
        dialog.title(self.tr("Calendario delle pagine"))
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.resizable(False, False)
        card = tk.Frame(dialog, bg=PAPER, padx=18, pady=16,
                        highlightbackground=LINE, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=1, pady=1)
        header = tk.Frame(card, bg=PAPER)
        header.pack(fill="x", pady=(0, 10))
        self.button(header, "‹", lambda: self.shift_calendar_month(-1)).pack(side="left")
        self.calendar_month_label = self.label(
            header, "", size=13, family=SERIF, weight="bold")
        self.calendar_month_label.pack(side="left", fill="x", expand=True)
        self.button(header, "›", lambda: self.shift_calendar_month(1)).pack(side="right")
        self.calendar_grid = tk.Frame(card, bg=PAPER)
        self.calendar_grid.pack(fill="x")
        footer = tk.Frame(card, bg=PAPER)
        footer.pack(fill="x", pady=(12, 0))
        self.label(footer, "●  Giorno con pagine", size=8, color=GREEN).pack(side="left")
        self.button(footer, "Tutte le date", self.clear_calendar_filter).pack(side="right")
        dialog.protocol("WM_DELETE_WINDOW", self.close_calendar)
        dialog.bind("<Escape>", lambda _event: self.close_calendar())
        self.render_calendar()
        dialog.update_idletasks()
        width, height = dialog.winfo_reqwidth(), dialog.winfo_reqheight()
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")
        dialog.grab_set()

    def render_calendar(self):
        if not self.calendar_dialog or not self.calendar_dialog.winfo_exists():
            return
        for child in self.calendar_grid.winfo_children():
            child.destroy()
        months = MONTHS_EN if self.language == "en" else MONTHS
        self.calendar_month_label.config(text=f"{months[self.calendar_month - 1].capitalize()} {self.calendar_year}")
        weekday_headers = ("M", "T", "W", "T", "F", "S", "S") if self.language == "en" else ("L", "M", "M", "G", "V", "S", "D")
        for column, name in enumerate(weekday_headers):
            self.label(self.calendar_grid, name, size=8, color=MUTED, weight="bold",
                       anchor="center").grid(row=0, column=column, sticky="nsew", pady=(0, 5))
        entries_by_day = {}
        for entry in self.entries:
            created = datetime.fromisoformat(entry.get("created", entry.get("updated")))
            if created.year == self.calendar_year and created.month == self.calendar_month:
                entries_by_day.setdefault(created.day, []).append(entry)
        first_weekday, month_days = calendar.monthrange(self.calendar_year, self.calendar_month)
        for day_number in range(1, month_days + 1):
            row, column = divmod(first_weekday + day_number - 1, 7)
            day_date = date(self.calendar_year, self.calendar_month, day_number)
            day_entries = entries_by_day.get(day_number, [])
            selected = day_date == self.selected_date
            mood = day_entries[0].get("mood", "") if day_entries else ""
            mood_color = MOOD_COLORS.get(mood, ACCENT)
            if selected:
                bg, fg = ACCENT, "#FFFFFF"
            elif day_entries:
                bg, fg = tint_color(PAPER, mood_color, 0.18), mood_color
            else:
                bg, fg = FIELD, INK
            text = f"{day_number}\n●" if day_entries else str(day_number)
            tk.Button(
                self.calendar_grid, text=text, command=lambda value=day_date: self.choose_calendar_date(value),
                bg=bg, fg=fg, activebackground=SOFT, activeforeground=INK,
                relief="flat", bd=0, width=4, height=2,
                font=(FONT, 9, "bold" if day_entries or selected else "normal"), cursor="hand2",
            ).grid(row=row + 1, column=column, sticky="nsew", padx=2, pady=2)
        for column in range(7):
            self.calendar_grid.grid_columnconfigure(column, weight=1, uniform="calendar-day")

    def shift_calendar_month(self, delta):
        month_index = self.calendar_year * 12 + self.calendar_month - 1 + delta
        self.calendar_year, month_zero = divmod(month_index, 12)
        self.calendar_month = month_zero + 1
        self.render_calendar()

    def close_calendar(self):
        dialog, self.calendar_dialog = self.calendar_dialog, None
        if dialog is not None and dialog.winfo_exists():
            dialog.grab_release()
            dialog.destroy()

    def clear_calendar_filter(self):
        self.close_calendar()
        self.clear_collection_filters()

    def choose_calendar_date(self, chosen_date):
        if self.selected_id:
            self.save_current()
        self.selected_date = chosen_date
        self.selected_tag = None
        self.close_calendar()
        matches = [e for e in self.entries
                   if datetime.fromisoformat(e.get("created", e.get("updated"))).date() == chosen_date]
        if matches:
            target = max(matches, key=lambda e: e.get("updated", ""))["id"]
            self.select_entry(target)
        else:
            self.selected_id = None
            self.refresh_list()
            self.show_empty_editor()

    def toggle_favorites(self):
        self.favorite_only = not self.favorite_only
        self.style_favorite_button(self.filter_button, self.favorite_only,
                                   "Tutte le pagine" if self.favorite_only else "☆  Mostra preferiti")
        self.refresh_list()

    def style_favorite_button(self, button, selected, text):
        button.config(
            text=self.tr(text),
            bg=GOLD_ACTIVE if selected else GOLD_FILL,
            fg=GOLD,
            activebackground=GOLD_ACTIVE,
            activeforeground=GOLD,
            highlightbackground=GOLD if selected else LINE,
        )

    def password_change_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.tr("Cambia password"))
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.resizable(False, False)
        width, height = 470, 390
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")

        card = tk.Frame(dialog, bg=PAPER, padx=28, pady=24)
        card.pack(fill="both", expand=True, padx=1, pady=1)
        self.label(card, "◇", size=18, color=ACCENT).pack(anchor="w")
        self.label(card, "Cambia password", size=20, family=SERIF).pack(anchor="w", pady=(4, 4))
        self.label(card, "Scegli una nuova chiave per proteggere il diario.",
                   size=9, color=MUTED).pack(anchor="w", pady=(0, 18))

        fields = tk.Frame(card, bg=PAPER)
        fields.pack(fill="x")
        password_inputs = []
        for label in ("Nuova password", "Ripeti la nuova password"):
            self.label(fields, label, size=9, color=INK, weight="bold").pack(anchor="w", pady=(0, 6))
            entry = tk.Entry(fields, show="•", font=(FONT, 11), bg=FIELD, fg=INK,
                             relief="flat", bd=0, highlightthickness=1,
                             highlightbackground=LINE, highlightcolor=ACCENT,
                             insertbackground=INK)
            entry.pack(fill="x", ipady=9, pady=(0, 13))
            password_inputs.append(entry)

        error = self.label(card, "Almeno 8 caratteri · le due password devono coincidere.",
                           size=8, color=MUTED, wraplength=410, justify="left")
        error.pack(anchor="w", pady=(0, 15))
        actions = tk.Frame(card, bg=PAPER)
        actions.pack(fill="x")
        result = {"value": None}

        def cancel():
            result["value"] = None
            dialog.destroy()

        def submit():
            password, confirmation = (entry.get() for entry in password_inputs)
            if len(password) < 8:
                error.config(text=self.tr("La password deve contenere almeno 8 caratteri."), fg=DELETE_INK)
                password_inputs[0].focus_set()
                return
            if password != confirmation:
                error.config(text=self.tr("Le due password non coincidono. Riprova."), fg=DELETE_INK)
                password_inputs[1].focus_set()
                return
            result["value"] = password, confirmation
            dialog.destroy()

        self.button(actions, "Annulla", cancel).pack(side="right")
        self.button(actions, "Aggiorna password", submit, primary=True).pack(side="right", padx=(0, 8))
        dialog.bind("<Return>", lambda _event: submit())
        dialog.bind("<Escape>", lambda _event: cancel())
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        dialog.grab_set()
        password_inputs[0].focus_set()
        self.root.wait_window(dialog)
        return result["value"]

    def change_password(self):
        credentials = self.password_change_dialog()
        if credentials is None:
            return
        password, confirmation = credentials
        self.save_current()
        previous = self.password
        self.password = password
        try:
            self.persist()
        except OSError as exc:
            self.password = previous
            messagebox.showerror(self.tr("Modifica non riuscita"), self.tr(str(exc)), parent=self.root)
            return
        messagebox.showinfo(
            self.tr("Password aggiornata"),
            self.tr("Da ora usa la nuova password per aprire il diario."),
            parent=self.root,
        )

    def show_security_options(self):
        self.show_styled_menu(
            self.security_button,
            "Sicurezza del diario",
            [
                {"icon": "↗", "label": "Crea copia cifrata",
                 "detail": "Esporta un file protetto", "command": self.export_backup},
                {"icon": "↻", "label": "Ripristina da una copia",
                 "detail": "Sostituisce le pagine attuali", "command": self.restore_backup},
                None,
                {"icon": "◇", "label": "Cambia password",
                 "detail": "Scegli una nuova chiave", "command": self.change_password},
            ],
            width=280,
        )

    def export_backup(self):
        self.save_current()
        name = f"Contropensiero-{datetime.now():%Y-%m-%d}.enc"
        destination = filedialog.asksaveasfilename(
            parent=self.root, title=self.tr("Salva una copia cifrata"),
            initialfile=name, defaultextension=".enc",
            filetypes=[("Copia cifrata Contropensiero", "*.enc"), ("Tutti i file", "*.*")]
        )
        if not destination:
            return
        try:
            destination_path = Path(destination)
            if destination_path.resolve() == self.path.resolve():
                messagebox.showinfo(self.tr("Copia di sicurezza"), self.tr("Il diario è già salvato in questo file."), parent=self.root)
                return
            destination_path.write_bytes(self.path.read_bytes())
        except OSError as exc:
            messagebox.showerror(self.tr("Copia non riuscita"), self.tr(str(exc)), parent=self.root)
            return
        self.save_label.config(text=self.tr("Copia cifrata creata"), fg=GREEN)

    def restore_backup(self):
        source = filedialog.askopenfilename(
            parent=self.root, title=self.tr("Scegli una copia cifrata"),
            filetypes=[("Copia cifrata Contropensiero", "*.enc"), ("Tutti i file", "*.*")]
        )
        if not source:
            return
        try:
            restored = decrypt_vault(self.password, Path(source).read_bytes())
        except InvalidTag:
            messagebox.showerror(self.tr("Copia non valida"), self.tr("La copia non corrisponde a questa password o è danneggiata."), parent=self.root)
            return
        except Exception as exc:
            messagebox.showerror(self.tr("Copia non valida"), f"{self.tr('Non riesco a leggere la copia: ')}{exc}", parent=self.root)
            return
        if not messagebox.askyesno(
            self.tr("Ripristinare la copia?"),
            self.tr("Le pagine attuali verranno sostituite con quelle della copia.\n\nVuoi continuare?"),
            parent=self.root,
        ):
            return
        self.save_current()
        self.entries = restored
        self.selected_id = None
        self.dirty = False
        self.favorite_only = False
        self.style_favorite_button(self.filter_button, False, "☆  Mostra preferiti")
        self.persist()
        self.refresh_list()
        if self.entries:
            newest = max(self.entries, key=lambda e: e.get("updated", e.get("created", "")))
            self.select_entry(newest["id"])
        else:
            self.show_empty_editor()

    def show_empty_editor(self):
        for child in self.editor_shell.winfo_children():
            child.destroy()
        blank = tk.Frame(self.editor_shell, bg=PAPER)
        blank.place(relx=.5, rely=.47, anchor="center")
        self.label(blank, "✳", size=29, color=ACCENT).pack()
        if self.entries:
            heading = "Le tue pagine sono al sicuro."
            description = "Scegline una dall’elenco o apri una nuova pagina."
            action = "+  Nuovo pensiero"
        else:
            heading = "C’è spazio per quello che ti passa per la testa."
            description = "Una frase, un appunto, un pensiero senza un perché."
            action = "+  Scrivi il primo"
        self.label(blank, heading, size=16, family=SERIF).pack(pady=(12, 6))
        self.label(blank, description, size=10, color=MUTED).pack()
        self.button(blank, action, self.new_entry, primary=True).pack(pady=20)

    def select_entry(self, entry_id):
        if self.selected_id and self.selected_id != entry_id:
            self.save_current()
        self.selected_id = entry_id
        self.refresh_list()
        item = next((e for e in self.entries if e["id"] == entry_id), None)
        if not item:
            return
        for child in self.editor_shell.winfo_children():
            child.destroy()
        panel = tk.Frame(self.editor_shell, bg=PAPER)
        panel.pack(fill="both", expand=True, padx=36, pady=28)
        toolbar = tk.Frame(panel, bg=PAPER)
        toolbar.pack(fill="x")
        self.label(toolbar, date_label(item["created"], weekday=True, language=self.language),
                   size=11, color=INK, weight="bold").pack(side="left")
        self.button(toolbar, "Elimina pagina", lambda: self.delete_entry(entry_id),
                    danger=True).pack(side="right")
        favorite_label = "★  Nei preferiti" if item.get("favorite") else "☆  Aggiungi ai preferiti"
        self.favorite_button = self.button(toolbar, favorite_label,
                                           lambda: self.toggle_entry_favorite(entry_id), gold=True)
        self.style_favorite_button(self.favorite_button, item.get("favorite", False), favorite_label)
        self.favorite_button.pack(side="right", padx=(0, 8))
        self.button(toolbar, "Chiudi", self.close_current_entry).pack(side="right", padx=(0, 8))
        tk.Frame(panel, bg=LINE, height=1).pack(fill="x", pady=(16, 18))
        self.mood_var = tk.StringVar(value=item.get("mood", MOODS[0]))
        current_mood = item.get("mood", MOODS[0])
        mood_color = MOOD_COLORS.get(current_mood, GOLD)
        mood_surface = tint_color(PAPER, mood_color, 0.11)
        mood_row = tk.Frame(panel, bg=mood_surface, padx=11, pady=8)
        mood_row.pack(fill="x", pady=(0, 15))
        mood_accent = tk.Frame(mood_row, bg=mood_color, width=3)
        mood_accent.pack(side="left", fill="y", padx=(0, 10))
        mood_prompt = self.label(mood_row, "Oggi mi sento", size=11,
                                 color=mood_color, weight="bold", bg=mood_surface)
        mood_prompt.pack(side="left", padx=(0, 12))
        mood_picker = self.dropdown_button(
            mood_row, self.mood_text(current_mood), self.show_mood_options,
            color=mood_color)
        mood_picker.pack(side="left")
        self.mood_picker = mood_picker
        self.mood_row = mood_row
        self.mood_accent = mood_accent
        self.mood_prompt = mood_prompt
        tags_row = tk.Frame(panel, bg=PAPER)
        tags_row.pack(fill="x", pady=(0, 15))
        self.label(tags_row, "ETICHETTE · separate da virgole", size=8,
                   color=MUTED, weight="bold").pack(
            side="left", padx=(0, 10))
        self.tags_var = tk.StringVar(value=", ".join(normalize_tags(item.get("tags", []))))
        self.tags_entry = tk.Entry(
            tags_row, textvariable=self.tags_var, font=(FONT, 9), bg=FIELD, fg=INK,
            relief="flat", bd=0, highlightthickness=1, highlightbackground=LINE,
            highlightcolor=GREEN, insertbackground=INK,
        )
        self.tags_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.tags_entry.bind("<KeyRelease>", self.queue_save)
        self.tags_entry.bind("<<Paste>>", self.queue_save)
        self.tags_entry.bind("<<Cut>>", self.queue_save)
        self.title_var = tk.StringVar(value=item.get("title", "") or self.title_hint())
        title = tk.Entry(panel, textvariable=self.title_var, font=(SERIF, 25), bg=PAPER, fg=INK,
                         relief="flat", bd=0, insertbackground=INK)
        if not item.get("title"):
            title.config(fg=MUTED)
        title.bind("<FocusIn>", self.clear_title_hint)
        title.bind("<FocusOut>", self.restore_title_hint)
        title.pack(fill="x", pady=(0, 17))
        title.bind("<KeyRelease>", self.queue_save)
        title.bind("<<Paste>>", self.queue_save)
        title.bind("<<Cut>>", self.queue_save)
        text_area = tk.Frame(panel, bg=PAPER)
        text_area.pack(fill="both", expand=True)
        self.body = tk.Text(text_area, wrap="word", font=(FONT, 12), bg=PAPER, fg=BODY_INK,
                            relief="flat", bd=0, padx=0, pady=2, spacing1=3, spacing3=8,
                            insertbackground=ACCENT, undo=True)
        text_scrollbar = tk.Scrollbar(text_area, orient="vertical", command=self.body.yview,
                                      bg=SOFT, troughcolor=PAPER, activebackground=ACCENT,
                                      relief="flat", bd=0, width=8)
        self.body.configure(yscrollcommand=text_scrollbar.set)
        self.body.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y", padx=(8, 0))
        self.body.insert("1.0", item.get("body", ""))
        self.body.bind("<KeyRelease>", self.queue_save)
        for virtual_event in ("<<Paste>>", "<<Cut>>", "<<Undo>>", "<<Redo>>"):
            self.body.bind(virtual_event, self.queue_save)
        footer = tk.Frame(panel, bg=PAPER)
        footer.pack(fill="x", pady=(12, 0))
        tk.Frame(footer, bg=LINE, height=1).pack(fill="x", pady=(0, 11))
        self.count_label = self.label(footer, "", size=8, color=MUTED)
        self.count_label.pack(side="left")
        self.save_label = self.label(footer, "Salvato sul dispositivo", size=8, color=GREEN)
        self.save_label.pack(side="right")
        self.title_entry = title
        self.dirty = False
        self.update_word_count()
        self.reset_lock_timer()

    def clear_title_hint(self, _event=None):
        if self.title_var.get() == self.title_hint():
            self.title_var.set("")
            self.title_entry.config(fg=INK)

    def restore_title_hint(self, _event=None):
        if not self.title_var.get():
            self.title_var.set(self.title_hint())
            self.title_entry.config(fg=MUTED)

    def set_entry_mood(self, entry_id, mood):
        self.save_current()
        item = next((e for e in self.entries if e["id"] == entry_id), None)
        if not item:
            return
        item["mood"] = mood
        self.mood_var.set(mood)
        item["updated"] = datetime.now().isoformat(timespec="seconds")
        self.persist()
        mood_color = MOOD_COLORS.get(mood, GOLD)
        mood_surface = tint_color(PAPER, mood_color, 0.11)
        self.mood_row.config(bg=mood_surface)
        self.mood_accent.config(bg=mood_color)
        self.mood_prompt.config(bg=mood_surface, fg=mood_color)
        self.mood_picker.config(text=f"{self.mood_text(mood)}   ⌄", fg=mood_color)
        self.refresh_list()

    def show_mood_options(self):
        entry_id = self.selected_id
        if not entry_id:
            return
        choices = [
            {"icon": "●", "icon_color": MOOD_COLORS.get(mood, MUTED),
             "label_color": MOOD_COLORS.get(mood, GOLD) if mood == self.mood_var.get() else INK,
             "label": self.mood_text(mood), "command": lambda value=mood: self.set_entry_mood(entry_id, value),
             "selected": mood == self.mood_var.get()}
            for mood in MOODS
        ]
        self.show_styled_menu(self.mood_picker, "Umore della pagina", choices, width=230)

    def toggle_entry_favorite(self, entry_id):
        self.save_current()
        item = next((e for e in self.entries if e["id"] == entry_id), None)
        if not item:
            return
        item["favorite"] = not item.get("favorite", False)
        item["updated"] = datetime.now().isoformat(timespec="seconds")
        self.persist()
        self.style_favorite_button(
            self.favorite_button, item["favorite"],
            "★  Nei preferiti" if item["favorite"] else "☆  Aggiungi ai preferiti",
        )
        self.refresh_list()

    def new_entry(self):
        if self.selected_id:
            self.save_current()
        if self.favorite_only:
            self.favorite_only = False
            self.style_favorite_button(self.filter_button, False, "☆  Mostra preferiti")
        now = datetime.now().isoformat(timespec="seconds")
        item = {"id": secrets.token_hex(8), "created": now, "updated": now,
                "title": "", "body": "", "tags": []}
        self.entries.append(item)
        self.selected_id = item["id"]
        self.dirty = False
        self.persist()
        self.refresh_list()
        self.select_entry(item["id"])
        self.body.focus_set()

    def queue_save(self, _event=None):
        self.dirty = True
        self.update_word_count()
        self.status_var.set(self.tr("Modifiche in corso…"))
        self.save_label.config(text=self.tr("Modifiche in corso…"), fg=ACCENT)
        if self.autosave_job:
            self.root.after_cancel(self.autosave_job)
        self.autosave_job = self.root.after(700, self.save_current)
        self.reset_lock_timer()

    def update_word_count(self):
        if not hasattr(self, "body") or not self.body.winfo_exists():
            return
        content = self.body.get("1.0", "end-1c")
        words = len(content.split())
        if self.language == "en":
            self.count_label.config(text=f"{words} {'words' if words != 1 else 'word'}  ·  {len(content)} characters")
        else:
            self.count_label.config(text=f"{words} {'parole' if words != 1 else 'parola'}  ·  {len(content)} caratteri")

    def save_current(self):
        if self.autosave_job:
            try:
                self.root.after_cancel(self.autosave_job)
            except tk.TclError:
                pass
            self.autosave_job = None
        if not self.dirty or not self.selected_id or not hasattr(self, "body") or not self.body.winfo_exists():
            return
        item = next((e for e in self.entries if e["id"] == self.selected_id), None)
        if not item:
            return
        title = self.title_var.get().strip()
        item["title"] = "" if title == self.title_hint() else title
        item["body"] = self.body.get("1.0", "end-1c")
        item["tags"] = normalize_tags(self.tags_var.get())
        item["updated"] = datetime.now().isoformat(timespec="seconds")
        self.persist()
        self.dirty = False
        self.save_label.config(text=self.tr("Salvato sul dispositivo"), fg=GREEN)
        self.refresh_list()

    def delete_entry(self, entry_id):
        entry = next((item for item in self.entries if item["id"] == entry_id), None)
        if not entry:
            return
        title = entry.get("title", "").strip() or "Senza titolo"
        confirm_text = (f'“{title}” will be removed from your diary.\n\nThis action cannot be undone.'
                        if self.language == "en" else
                        f"«{title}» verrà rimossa dal diario.\n\nQuesta azione non si può annullare.")
        if not messagebox.askyesno(
            self.tr("Eliminare questa pagina?"),
            confirm_text,
            parent=self.root,
            default=messagebox.NO,
        ):
            return
        if self.autosave_job:
            self.root.after_cancel(self.autosave_job)
            self.autosave_job = None
        self.entries = [e for e in self.entries if e["id"] != entry_id]
        self.selected_id = None
        self.persist()
        self.refresh_list()
        if self.entries:
            self.select_entry(max(self.entries, key=lambda e: e.get("updated", ""))["id"])
        else:
            self.show_empty_editor()

    def close_current_entry(self, _event=None):
        if self.password is not None and self.selected_id:
            self.save_current()
            self.selected_id = None
            self.refresh_list()
            self.show_empty_editor()
        return "break"

    def reset_lock_timer(self):
        if self.lock_job:
            try:
                self.root.after_cancel(self.lock_job)
            except tk.TclError:
                pass
        self.lock_job = self.root.after(10 * 60 * 1000, self.lock)

    def on_activity(self, _event=None):
        if self.password is not None:
            self.reset_lock_timer()
        if _event is None or not hasattr(self, "list_frame"):
            return
        widget = _event.widget
        inside_list = False
        while widget is not None:
            if widget == self.list_frame:
                inside_list = True
                break
            widget = getattr(widget, "master", None)
        if inside_list and _event.type == tk.EventType.MouseWheel:
            delta = getattr(_event, "delta", 0)
            units = int(-delta / 120) or (-1 if delta > 0 else 1)
            self.list_canvas.yview_scroll(units, "units")

    def lock(self):
        if self.password is None:
            return
        self.save_current()
        self.password, self.entries, self.selected_id = None, [], None
        self.dirty = False
        self.favorite_only = False
        if self.lock_job:
            self.root.after_cancel(self.lock_job)
            self.lock_job = None
        self.show_lock_screen()

    def close(self):
        self.save_current()
        self.password = None
        self.root.destroy()


def main():
    root = tk.Tk()
    Contropensiero(root)
    root.mainloop()


if __name__ == "__main__":
    main()
