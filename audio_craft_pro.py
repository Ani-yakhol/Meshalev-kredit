#!/usr/bin/env python3
"""
AudioCraft Pro v0.5  —  משלב הקרדיט
PyQt6 UI  |  RTL Hebrew + LTR English  |  Persistent settings
"""

import sys, os, json, threading, subprocess, logging
from pathlib import Path
from datetime import datetime

# ── logging to file ──────────────────────────────────────────────────────────
def _get_base():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent

LOG_PATH = _get_base() / "audiocraftpro.log"
logging.basicConfig(
    filename=str(LOG_PATH), level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
log = logging.getLogger("acp")

# ── Optional audio deps ───────────────────────────────────────────────────────
try:
    from pydub import AudioSegment
    PYDUB_OK = True
except ImportError:
    PYDUB_OK = False
    log.warning("pydub not installed")

def _setup_ffmpeg_local():
    base = str(_get_base())
    ffmpeg  = os.path.join(base, "ffmpeg.exe")
    ffprobe = os.path.join(base, "ffprobe.exe")
    if os.path.isfile(ffmpeg) and PYDUB_OK:
        AudioSegment.converter = ffmpeg
        if os.path.isfile(ffprobe):
            AudioSegment.ffprobe = ffprobe
        log.info(f"FFmpeg local: {ffmpeg}")
        return True
    return False

_FFMPEG_LOCAL = _setup_ffmpeg_local()

try:
    from mutagen.id3 import ID3, APIC, error as MutagenError
    from mutagen.flac import FLAC, Picture
    from mutagen.mp4 import MP4, MP4Cover
    MUTAGEN_OK = True
except ImportError:
    MUTAGEN_OK = False
    log.warning("mutagen not installed")

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

SUPPORTED_FORMATS = [".mp3",".wav",".flac",".aac",".ogg",".m4a",".wma",".opus"]
APP_NAME    = "AudioCraft Pro"
APP_VERSION = "0.7"
SETTINGS_PATH = _get_base() / "settings.json"

# ══════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════════════════════════════════════════

_DEFAULT_SETTINGS = {
    "lang":        "he",
    "theme":       "light",
    "output_dir":  "",
    "output_mode": "original",   # original | add_credit | custom
    "output_suffix": "קרדיט",
    "output_format": "source",
    "ffmpeg_path": "",
}

def load_settings() -> dict:
    s = dict(_DEFAULT_SETTINGS)
    try:
        if SETTINGS_PATH.exists():
            s.update(json.loads(SETTINGS_PATH.read_text(encoding="utf-8")))
    except Exception as e:
        log.warning(f"load_settings: {e}")
    return s

def save_settings(s: dict):
    try:
        SETTINGS_PATH.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log.warning(f"save_settings: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# STRINGS  (i18n)
# ══════════════════════════════════════════════════════════════════════════════

_S = {
    "he": {
        "app_subtitle":      "משלב הקרדיט",
        "nav_files":         "📁  קבצי שמע",
        "nav_credits":       "🎙  קרדיטים",
        "nav_cover":         "🖼  תמונת כיסוי",
        "nav_export":        "📤  ייצוא",
        "nav_settings":      "⚙  הגדרות",
        "nav_about":         "ℹ  אודות",
        "files_title":       "קבצי שמע לעריכה",
        "files_subtitle":    "גרור קבצים לכאן או לחץ לבחירה",
        "btn_add_files":     "📂  הוסף קבצים",
        "btn_add_folder":    "📁  הוסף תיקיה",
        "btn_remove":        "✕  הסר נבחר",
        "btn_clear":         "🗑  נקה הכל",
        "col_type":          "סוג",
        "col_name":          "שם קובץ",
        "col_dur":           "משך",
        "col_size":          "גודל",
        "drop_hint":         "גרור קבצי שמע לכאן\nMP3 · WAV · FLAC · AAC · OGG · M4A · WMA · OPUS",
        "n_files":           "{n} קבצים נבחרו",
        "credits_title":     "נקודות קרדיט",
        "duck_label":        "הנמך את הקובץ הראשי בזמן הקרדיט (Duck −30 dB)",
        "btn_add_cp":        "➕  הוסף",
        "btn_edit_cp":       "✏  ערוך",
        "btn_del_cp":        "🗑  מחק",
        "col_pos":           "מיקום",
        "col_time":          "זמן",
        "col_file":          "קובץ קרדיט",
        "col_vol":           "עוצמה",
        "pos_start":         "🟢  התחלה",
        "pos_mid":           "🔵  אמצע",
        "pos_end":           "🔴  סוף",
        "cover_title":       "תמונת כיסוי",
        "cover_desc":        "התמונה תוטמע בתגיות של כל קובץ פלט.\nתמיכה: MP3, FLAC, M4A.  פורמט: JPG/PNG, ריבועי, 500×500+",
        "cover_path_lbl":    "נתיב קובץ תמונה:",
        "btn_browse_cover":  "📂  בחר תמונה",
        "embed_cover_chk":   "הטמע תמונה בכל קובץ פלט",
        "export_title":      "ייצוא ועיבוד",
        "export_files_lbl":  "קבצים לעיבוד:",
        "outdir_lbl":        "תיקיית שמירה:",
        "outdir_default":    "(ברירת מחדל — לצד הכלי)",
        "btn_browse_dir":    "📂",
        "format_lbl":        "פורמט פלט:",
        "fmt_source":        "זהה למקור",
        "fmt_mp3":           "MP3 · 320kbps",
        "fmt_wav":           "WAV · ללא דחיסה",
        "fmt_flac":          "FLAC · ללא אובדן",
        "fmt_aac":           "AAC · 256kbps",
        "suffix_lbl":        "שם קובץ פלט:",
        "suffix_original":   "שם מקורי (ללא שינוי)",
        "suffix_credit":     "הוסף 'קרדיט' לפני הסיומת",
        "suffix_custom":     "הוסף תחילית מותאמת:",
        "cover_exp_lbl":     "תמונת כיסוי:",
        "embed_exp_chk":     "הטמע תמונה",
        "btn_start":         "🚀  התחל עיבוד",
        "btn_cancel":        "⛔  בטל",
        "status_ready":      "מוכן",
        "status_processing": "מעבד…",
        "status_done":       "הושלם ✓",
        "status_cancelled":  "בוטל",
        "msg_no_files":      "לא נבחרו קבצי שמע.",
        "msg_no_credits":    "לא הוגדרו נקודות קרדיט.",
        "msg_no_pydub":      "pydub אינו מותקן.\nהרץ: pip install pydub",
        "msg_done":          "הושלם: {ok} קבצים\nכשלונות: {fail}",
        "msg_done_title":    "עיבוד הושלם",
        "settings_title":    "הגדרות",
        "lang_lbl":          "שפה / Language:",
        "theme_lbl":         "מצב תצוגה:",
        "theme_dark":        "כהה",
        "theme_light":       "בהיר",
        "ffmpeg_lbl":        "תיקיית FFmpeg (bin):",
        "btn_save_ffmpeg":   "שמור",
        "about_title":       "אודות",
        "cp_dialog_title":   "נקודת קרדיט",
        "cp_pos_lbl":        "מיקום:",
        "cp_time_lbl":       "זמן (mm:ss):",
        "cp_file_lbl":       "קובץ קרדיט:",
        "cp_vol_lbl":        "עוצמה:",
        "btn_ok":            "✓  אישור",
        "btn_cancel_dlg":    "ביטול",
        "btn_browse":        "📂",
        "err_no_file":       "יש לבחור קובץ קרדיט.",
        "err_file_missing":  "הקובץ לא קיים.",
        "cp_mode_lbl":       "אופן שילוב הקרדיט:",
        "cp_mode_insert":    "הוספה (לפני/אחרי/באמצע)",
        "cp_mode_overlay":   "ניגון מקביל (overlay)",
        "cp_interval_lbl":   "הוסף בכל מרווח זמן:",
        "cp_interval_hint":  "השאר ריק לנקודה בודדת",
        "theme_toggle":      "☀  מצב בהיר",
        "theme_toggle_dark": "🌙  מצב כהה",
    },
    "en": {
        "app_subtitle":      "Credit Mixer",
        "nav_files":         "📁  Audio Files",
        "nav_credits":       "🎙  Credits",
        "nav_cover":         "🖼  Cover Art",
        "nav_export":        "📤  Export",
        "nav_settings":      "⚙  Settings",
        "nav_about":         "ℹ  About",
        "files_title":       "Audio Files",
        "files_subtitle":    "Drag files here or click to select",
        "btn_add_files":     "📂  Add Files",
        "btn_add_folder":    "📁  Add Folder",
        "btn_remove":        "✕  Remove",
        "btn_clear":         "🗑  Clear All",
        "col_type":          "Type",
        "col_name":          "File Name",
        "col_dur":           "Duration",
        "col_size":          "Size",
        "drop_hint":         "Drag audio files here\nMP3 · WAV · FLAC · AAC · OGG · M4A · WMA · OPUS",
        "n_files":           "{n} files selected",
        "credits_title":     "Credit Points",
        "duck_label":        "Duck main audio during credit (−30 dB)",
        "btn_add_cp":        "➕  Add",
        "btn_edit_cp":       "✏  Edit",
        "btn_del_cp":        "🗑  Delete",
        "col_pos":           "Position",
        "col_time":          "Time",
        "col_file":          "Credit File",
        "col_vol":           "Volume",
        "pos_start":         "🟢  Start",
        "pos_mid":           "🔵  Middle",
        "pos_end":           "🔴  End",
        "cover_title":       "Cover Art",
        "cover_desc":        "Image will be embedded in every output file's tags.\nSupported: MP3, FLAC, M4A.  Format: JPG/PNG, square, 500×500+",
        "cover_path_lbl":    "Image file path:",
        "btn_browse_cover":  "📂  Browse",
        "embed_cover_chk":   "Embed image in every output file",
        "export_title":      "Export & Process",
        "export_files_lbl":  "Files to process:",
        "outdir_lbl":        "Output folder:",
        "outdir_default":    "(default — next to the tool)",
        "btn_browse_dir":    "📂",
        "format_lbl":        "Output format:",
        "fmt_source":        "Same as source",
        "fmt_mp3":           "MP3 · 320kbps",
        "fmt_wav":           "WAV · Uncompressed",
        "fmt_flac":          "FLAC · Lossless",
        "fmt_aac":           "AAC · 256kbps",
        "suffix_lbl":        "Output file name:",
        "suffix_original":   "Original name (no change)",
        "suffix_credit":     "Add 'credit' before extension",
        "suffix_custom":     "Add custom suffix:",
        "cover_exp_lbl":     "Cover art:",
        "embed_exp_chk":     "Embed cover",
        "btn_start":         "🚀  Start Processing",
        "btn_cancel":        "⛔  Cancel",
        "status_ready":      "Ready",
        "status_processing": "Processing…",
        "status_done":       "Done ✓",
        "status_cancelled":  "Cancelled",
        "msg_no_files":      "No audio files selected.",
        "msg_no_credits":    "No credit points defined.",
        "msg_no_pydub":      "pydub is not installed.\nRun: pip install pydub",
        "msg_done":          "Done: {ok} files\nFailed: {fail}",
        "msg_done_title":    "Processing Complete",
        "settings_title":    "Settings",
        "lang_lbl":          "Language / שפה:",
        "theme_lbl":         "Theme:",
        "theme_dark":        "Dark",
        "theme_light":       "Light",
        "ffmpeg_lbl":        "FFmpeg folder (bin):",
        "btn_save_ffmpeg":   "Save",
        "about_title":       "About",
        "cp_dialog_title":   "Credit Point",
        "cp_pos_lbl":        "Position:",
        "cp_time_lbl":       "Time (mm:ss):",
        "cp_file_lbl":       "Credit file:",
        "cp_vol_lbl":        "Volume:",
        "btn_ok":            "✓  OK",
        "btn_cancel_dlg":    "Cancel",
        "btn_browse":        "📂",
        "err_no_file":       "Please select a credit file.",
        "err_file_missing":  "File does not exist.",
        "cp_mode_lbl":       "Credit mode:",
        "cp_mode_insert":    "Insert (before/after/at time)",
        "cp_mode_overlay":   "Overlay (play in parallel)",
        "cp_interval_lbl":   "Repeat every interval:",
        "cp_interval_hint":  "Leave empty for single point",
        "theme_toggle":      "☀  Light",
        "theme_toggle_dark": "🌙  Dark",
    }
}

def T(key, lang="he", **kw):
    s = _S.get(lang, _S["he"]).get(key, key)
    return s.format(**kw) if kw else s

# ══════════════════════════════════════════════════════════════════════════════
# AUDIO UTILS
# ══════════════════════════════════════════════════════════════════════════════

def fmt_dur(s):
    if s < 0: return "00:00"
    h, r = divmod(int(s), 3600); m, sc = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{sc:02d}" if h else f"{m:02d}:{sc:02d}"

def parse_time(t):
    t = t.strip()
    if not t: return 0.0
    try:
        p = list(map(float, t.split(":")))
        return p[0] if len(p)==1 else (p[0]*60+p[1] if len(p)==2 else p[0]*3600+p[1]*60+p[2])
    except: return 0.0

def get_duration(path):
    if not PYDUB_OK: return 0.0
    try:
        ext = Path(path).suffix.lower().lstrip(".")
        return len(AudioSegment.from_file(path, format=ext)) / 1000.0
    except: return 0.0

def get_info(path):
    p = Path(path); sz = p.stat().st_size / (1024*1024); dur = get_duration(path)
    return {"name": p.name, "ext": p.suffix.upper().lstrip("."),
            "sz": sz, "dur": dur, "dur_str": fmt_dur(dur)}

# ══════════════════════════════════════════════════════════════════════════════
# AUDIO PROCESSOR  (unchanged logic)
# ══════════════════════════════════════════════════════════════════════════════

class AudioProcessor:
    def __init__(self, log_fn=None, progress_fn=None):
        self.log_fn = log_fn or (lambda m, l="info": None)
        self.progress_fn = progress_fn or (lambda v, t, label="": None)

    def build(self, main_path, credit_points, mute_main=False):
        ext = Path(main_path).suffix.lower().lstrip(".")
        main = AudioSegment.from_file(main_path, format=ext)
        dur_ms = len(main)

        # Expand interval-based credit points into individual time points
        expanded = []
        for cp in credit_points:
            interval_ms = cp.get("interval_ms", 0)
            if interval_ms and interval_ms > 0:
                t = cp["time_sec"]
                start_ms = 0 if t in (0, 0.0, "start") else (dur_ms if t == "end" else int(float(t)*1000))
                pos = start_ms
                while pos < dur_ms:
                    new_cp = dict(cp)
                    new_cp["time_sec"] = pos / 1000.0
                    new_cp["interval_ms"] = 0  # prevent infinite expansion
                    expanded.append(new_cp)
                    pos += interval_ms
            else:
                expanded.append(cp)

        points = sorted(expanded,
            key=lambda c: float("inf") if c["time_sec"]=="end" else float(c["time_sec"]))

        # Separate overlay vs insert points
        insert_pts  = [c for c in points if c.get("mode","insert") == "insert"]
        overlay_pts = [c for c in points if c.get("mode","insert") == "overlay"]

        # ── Build inserted version ──────────────────────────────────────────
        result = AudioSegment.empty(); cursor = 0
        for cp in insert_pts:
            t = cp["time_sec"]
            ins = dur_ms if t=="end" else max(0, min(int(float(t)*1000), dur_ms))
            cf = cp.get("file", "")
            if not cf or not Path(cf).exists(): continue
            try:
                cseg = AudioSegment.from_file(cf, format=Path(cf).suffix.lower().lstrip("."))
            except Exception as e:
                self.log_fn(f"Credit load error: {e}", "error"); continue
            vol = cp.get("volume", 1.0)
            if vol != 1.0: cseg = cseg + (20*(vol-1))
            duck_db = cp.get("duck_db", 0)
            if ins > cursor:
                chunk = main[cursor:ins]
                if duck_db > 0: chunk = chunk - duck_db
                elif mute_main: chunk = chunk - 30
                result += chunk
            result += cseg; cursor = ins
        if cursor < dur_ms: result += main[cursor:]

        # ── Apply overlay points (mix credit over result) ───────────────────
        for cp in overlay_pts:
            t = cp["time_sec"]
            cf = cp.get("file","")
            if not cf or not Path(cf).exists(): continue
            try:
                cseg = AudioSegment.from_file(cf, format=Path(cf).suffix.lower().lstrip("."))
            except Exception as e:
                self.log_fn(f"Overlay load error: {e}", "error"); continue
            vol = cp.get("volume", 1.0)
            if vol != 1.0: cseg = cseg + (20*(vol-1))
            offset_ms = 0 if t in (0, 0.0, "start") else (len(result)-len(cseg) if t=="end" else int(float(t)*1000))
            offset_ms = max(0, min(offset_ms, len(result)))
            duck_db = cp.get("duck_db", 30 if mute_main else 0)
            if duck_db > 0:
                # duck the section under the overlay
                pre   = result[:offset_ms]
                mid   = result[offset_ms:offset_ms+len(cseg)] - duck_db
                post  = result[offset_ms+len(cseg):]
                result = pre + mid + post
            result = result.overlay(cseg, position=offset_ms)

        return result

    def embed_cover(self, audio_path, image_path, fmt):
        if not MUTAGEN_OK: return
        try:
            img_data = open(image_path, "rb").read()
            mime = "image/jpeg" if image_path.lower().endswith((".jpg",".jpeg")) else "image/png"
            if fmt == "mp3":
                try: tags = ID3(audio_path)
                except MutagenError: tags = ID3()
                tags.add(APIC(encoding=3, mime=mime, type=3, desc="Cover", data=img_data))
                tags.save(audio_path)
            elif fmt == "flac":
                a = FLAC(audio_path); pic = Picture()
                pic.data = img_data; pic.mime = mime; pic.type = 3
                a.add_picture(pic); a.save()
            elif fmt in ("mp4","m4a"):
                a = MP4(audio_path)
                fmt2 = MP4Cover.FORMAT_JPEG if "jpeg" in mime else MP4Cover.FORMAT_PNG
                a["covr"] = [MP4Cover(img_data, imageformat=fmt2)]; a.save()
            self.log_fn(f"Cover embedded: {Path(audio_path).name}", "success")
        except Exception as e:
            self.log_fn(f"Cover embed failed: {e}", "warning")

    def _out_name(self, main_path, out_fmt, mode, custom_suffix):
        stem = Path(main_path).stem
        ext  = out_fmt if out_fmt != "mp4" else "m4a"
        if mode == "add_credit":
            return f"{stem}_קרדיט.{ext}"
        elif mode == "custom" and custom_suffix:
            return f"{stem}_{custom_suffix}.{ext}"
        else:
            return f"{stem}.{ext}"

    def process_file(self, main_path, credit_points, out_dir, fmt,
                     cover=None, mute=False, bitrate="320k",
                     suffix_mode="original", custom_suffix=""):
        self.log_fn(f"Processing: {Path(main_path).name}", "info")
        log.info(f"process_file: {main_path}")
        merged = self.build(main_path, credit_points, mute)
        src_ext = Path(main_path).suffix.lower().lstrip(".")
        out_fmt = src_ext if fmt == "source" else fmt
        if out_fmt == "m4a": out_fmt = "mp4"
        out_name = self._out_name(main_path, out_fmt, suffix_mode, custom_suffix)
        out_path = str(Path(out_dir) / out_name)
        kw = {"format": out_fmt}
        if out_fmt == "mp3": kw["bitrate"] = bitrate
        elif out_fmt in ("mp4","aac"): kw["codec"] = "aac"; kw["bitrate"] = bitrate
        merged.export(out_path, **kw)
        if cover and Path(cover).exists():
            self.embed_cover(out_path, cover, out_fmt)
        self.log_fn(f"Done: {out_name}", "success")
        log.info(f"Done: {out_path}")
        return out_path

    def process_batch(self, files, credit_points, out_dir, fmt,
                      cover=None, mute=False, bitrate="320k",
                      done_cb=None, cancel=None,
                      suffix_mode="original", custom_suffix=""):
        results = []; total = len(files)
        for i, f in enumerate(files):
            if cancel and cancel.is_set():
                self.log_fn("Cancelled", "warning"); log.info("Batch cancelled"); break
            self.progress_fn(i, total, Path(f).name)
            try:
                out = self.process_file(f, credit_points, out_dir, fmt,
                                        cover, mute, bitrate, suffix_mode, custom_suffix)
                results.append({"file": f, "output": out, "ok": True})
            except Exception as e:
                self.log_fn(f"Error: {Path(f).name}: {e}", "error")
                log.error(f"process_file failed {f}: {e}")
                results.append({"file": f, "output": None, "ok": False, "error": str(e)})
            self.progress_fn(i+1, total, Path(f).name)
        self.progress_fn(total, total, "Done")
        if done_cb: done_cb(results)
        return results

# ══════════════════════════════════════════════════════════════════════════════
# PyQt6 UI
# ══════════════════════════════════════════════════════════════════════════════

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QTreeWidget,
    QTreeWidgetItem, QFileDialog, QLineEdit, QComboBox, QCheckBox,
    QRadioButton, QButtonGroup, QSlider, QProgressBar, QDialog,
    QDialogButtonBox, QSplitter, QFrame, QScrollArea, QSizePolicy, QFormLayout,
    QStackedWidget, QGroupBox, QMessageBox, QSpacerItem, QAbstractItemView,
    QHeaderView, QToolButton
)
from PyQt6.QtCore import (
    Qt, QThread, QObject, pyqtSignal, QTimer, QSize, QMimeData, QUrl
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QIcon, QDragEnterEvent, QDropEvent,
    QFontMetrics
)

# ── Color palettes ────────────────────────────────────────────────────────────

PALETTES = {
    "dark": {
        "bg":        "#0d0f14", "bg2":      "#13161e", "bg3":     "#181c26",
        "bg4":       "#1e2332", "input":    "#0f1219", "panel":   "#151820",
        "accent":    "#5b8cff", "accent2":  "#3d6bde", "success": "#3ecf8e",
        "warning":   "#f5a623", "danger":   "#f05252",
        "fg":        "#e8ecf4", "fg2":      "#8b97b3", "fg3":     "#505a72",
        "border":    "#1e2538", "border2":  "#334273",
        "sel_bg":    "#334273", "sel_fg":   "#7fa8ff",
    },
    "light": {
        "bg":        "#f0f2f7", "bg2":      "#ffffff", "bg3":     "#ffffff",
        "bg4":       "#f5f7ff", "input":    "#f8f9fc", "panel":   "#eef0f6",
        "accent":    "#3b6cf0", "accent2":  "#2a56cc", "success": "#1aaa6e",
        "warning":   "#c97a00", "danger":   "#d93535",
        "fg":        "#1a1d27", "fg2":      "#505878", "fg3":     "#9aa3b8",
        "border":    "#dce0ec", "border2":  "#bcc4de",
        "sel_bg":    "#dce0ff", "sel_fg":   "#2a56cc",
    }
}

def _qss(p: dict, rtl: bool) -> str:
    align_h = "right" if rtl else "left"
    return f"""
QMainWindow, QDialog, QWidget {{
    background: {p['bg']}; color: {p['fg']};
    font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 14px;
}}
QFrame#sidebar {{
    background: {p['bg2']};
    border-right: 1px solid {p['border']};
}}
QPushButton#navbtn {{
    background: transparent; color: {p['fg2']};
    border: none; border-radius: 0;
    padding: 10px 16px; text-align: {align_h};
    font-size: 14px;
}}
QPushButton#navbtn:hover {{ background: {p['bg3']}; color: {p['fg']}; }}
QPushButton#navbtn[active="true"] {{
    background: {p['bg3']}; color: {p['accent']};
    border-{align_h}: 3px solid {p['accent']};
}}
QPushButton {{
    background: {p['panel']}; color: {p['fg']};
    border: 1px solid {p['border2']}; border-radius: 6px;
    padding: 6px 14px; font-size: 13px;
}}
QPushButton:hover {{ background: {p['bg4']}; }}
QPushButton:pressed {{ background: {p['border2']}; }}
QPushButton#accent {{
    background: {p['accent']}; color: #ffffff;
    border: none; font-weight: bold;
}}
QPushButton#accent:hover {{ background: {p['accent2']}; }}
QPushButton#danger {{
    background: transparent; color: {p['danger']};
    border: 1px solid {p['danger']};
}}
QPushButton#danger:hover {{ background: rgba(240,82,82,0.12); }}
QPushButton#success {{
    background: {p['success']}; color: #0a2018;
    border: none; font-weight: bold; font-size: 15px; padding: 10px 24px;
}}
QPushButton#success:hover {{ opacity: 0.9; }}
QLineEdit, QComboBox {{
    background: {p['input']}; color: {p['fg']};
    border: 1px solid {p['border2']}; border-radius: 5px;
    padding: 5px 10px; font-size: 13px;
}}
QLineEdit:focus, QComboBox:focus {{ border-color: {p['accent']}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    background: {p['bg3']}; color: {p['fg']};
    selection-background-color: {p['sel_bg']};
    selection-color: {p['sel_fg']};
    border: 1px solid {p['border2']};
}}
QTreeWidget, QListWidget {{
    background: {p['input']}; color: {p['fg']};
    border: 1px solid {p['border2']}; border-radius: 5px;
    alternate-background-color: {p['bg3']};
    outline: none;
}}
QTreeWidget::item, QListWidget::item {{
    padding: 5px 8px;
}}
QTreeWidget::item:selected, QListWidget::item:selected {{
    background: {p['sel_bg']}; color: {p['sel_fg']};
}}
QTreeWidget::item:hover, QListWidget::item:hover {{
    background: {p['bg4']};
}}
QHeaderView::section {{
    background: {p['panel']}; color: {p['fg2']};
    border: none; border-bottom: 1px solid {p['border2']};
    padding: 5px 8px; font-weight: bold; font-size: 12px;
}}
QScrollBar:vertical {{
    background: {p['bg2']}; width: 8px; border: none;
}}
QScrollBar::handle:vertical {{
    background: {p['border2']}; border-radius: 4px; min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QProgressBar {{
    background: {p['panel']}; border: none; border-radius: 3px; height: 6px; text-align: center;
}}
QProgressBar::chunk {{
    background: {p['accent']}; border-radius: 3px;
}}
QCheckBox, QRadioButton {{ color: {p['fg2']}; spacing: 8px; font-size: 13px; }}
QCheckBox:hover, QRadioButton:hover {{ color: {p['fg']}; }}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 16px; height: 16px;
    border: 1px solid {p['border2']}; border-radius: 3px;
    background: {p['input']};
}}
QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background: {p['accent']}; border-color: {p['accent']};
}}
QRadioButton::indicator {{ border-radius: 8px; }}
QSlider::groove:horizontal {{
    background: {p['border2']}; height: 4px; border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {p['accent']}; width: 14px; height: 14px;
    border-radius: 7px; margin: -5px 0;
}}
QLabel#sectiontitle {{
    color: {p['fg']}; font-size: 16px; font-weight: bold;
}}
QLabel#sectionsubtitle {{
    color: {p['fg3']}; font-size: 12px;
}}
QLabel#seclabel {{
    color: {p['fg3']}; font-size: 11px; font-weight: bold;
    text-transform: uppercase; padding: 10px 14px 3px;
}}
QFrame#card {{
    background: {p['bg3']};
    border: 1px solid {p['border']};
    border-radius: 8px;
}}
QFrame#hline {{
    background: {p['border']}; max-height: 1px;
}}
QLabel#statusbar {{
    background: {p['bg2']}; color: {p['fg3']};
    border-top: 1px solid {p['border']}; padding: 3px 14px;
    font-size: 12px;
}}
QWidget#topbar {{
    background: {p['bg2']};
    border-bottom: 1px solid {p['border']};
}}
QPushButton#topbarbtn {{
    background: {p['panel']}; color: {p['fg2']};
    border: 1px solid {p['border2']}; border-radius: 4px;
    font-size: 12px; padding: 2px 10px;
}}
QPushButton#topbarbtn:hover {{
    background: {p['accent']}; color: #fff; border-color: {p['accent']};
}}
"""

# ── Worker thread ─────────────────────────────────────────────────────────────

class WorkerSignals(QObject):
    progress  = pyqtSignal(int, int, str)   # done, total, label
    log_msg   = pyqtSignal(str, str)        # msg, level
    finished  = pyqtSignal(list)            # results

class ProcessWorker(QThread):
    def __init__(self, files, credits, out_dir, fmt,
                 cover, mute, suffix_mode, custom_suffix, cancel_ev):
        super().__init__()
        self.signals = WorkerSignals()
        self.files = files; self.credits = credits
        self.out_dir = out_dir; self.fmt = fmt
        self.cover = cover; self.mute = mute
        self.suffix_mode = suffix_mode; self.custom_suffix = custom_suffix
        self.cancel = cancel_ev

    def run(self):
        proc = AudioProcessor(
            log_fn=lambda m,l="info": self.signals.log_msg.emit(m, l),
            progress_fn=lambda d,t,lbl: self.signals.progress.emit(d, t, lbl)
        )
        results = proc.process_batch(
            self.files, self.credits, self.out_dir, self.fmt,
            cover=self.cover, mute=self.mute,
            suffix_mode=self.suffix_mode, custom_suffix=self.custom_suffix,
            done_cb=None, cancel=self.cancel
        )
        self.signals.finished.emit(results)

# ══════════════════════════════════════════════════════════════════════════════
# CREDIT DIALOG
# ══════════════════════════════════════════════════════════════════════════════

class CreditDialog(QDialog):
    def __init__(self, parent, lang="he", existing=None):
        super().__init__(parent)
        self.lang = lang
        self.result_data = None
        ex = existing or {}
        rtl = lang == "he"

        self.setWindowTitle(T("cp_dialog_title", lang))
        self.setMinimumWidth(500)
        dir_ = Qt.LayoutDirection.RightToLeft if rtl else Qt.LayoutDirection.LeftToRight
        self.setLayoutDirection(dir_)

        layout = QVBoxLayout(self)
        layout.setSpacing(10); layout.setContentsMargins(20,16,20,16)
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft

        def lbl(key):
            l = QLabel(T(key, lang)); l.setAlignment(al); layout.addWidget(l)

        # ── Blend mode ───────────────────────────────────────────────────
        lbl("cp_mode_lbl")
        mode_w = QWidget(); mh = QHBoxLayout(mode_w); mh.setContentsMargins(0,0,0,4)
        self._rb_insert  = QRadioButton(T("cp_mode_insert",  lang))
        self._rb_overlay = QRadioButton(T("cp_mode_overlay", lang))
        self._mode_grp   = QButtonGroup()
        self._mode_grp.addButton(self._rb_insert); self._mode_grp.addButton(self._rb_overlay)
        mh.addWidget(self._rb_insert); mh.addWidget(self._rb_overlay); mh.addStretch()
        (self._rb_overlay if ex.get("mode","insert")=="overlay" else self._rb_insert).setChecked(True)
        layout.addWidget(mode_w)

        # ── Position (insert mode only) ────────────────────────────────────
        lbl("cp_pos_lbl")
        self._pos_w = QWidget(); ph = QHBoxLayout(self._pos_w); ph.setContentsMargins(0,0,0,4)
        self._rb_start = QRadioButton(T("pos_start", lang))
        self._rb_mid   = QRadioButton(T("pos_mid",   lang))
        self._rb_end   = QRadioButton(T("pos_end",   lang))
        self._pos_grp  = QButtonGroup()
        for rb in [self._rb_start, self._rb_mid, self._rb_end]:
            self._pos_grp.addButton(rb); ph.addWidget(rb)
        ph.addStretch()
        (self._rb_start if ex.get("position","mid")=="start" else
         self._rb_end   if ex.get("position","mid")=="end"   else
         self._rb_mid).setChecked(True)
        layout.addWidget(self._pos_w)

        # ── Time ──────────────────────────────────────────────────────────
        lbl("cp_time_lbl")
        self._time_e = QLineEdit(ex.get("time_str","00:00"))
        self._time_e.setMaximumWidth(130); layout.addWidget(self._time_e)

        # ── Repeat interval ───────────────────────────────────────────────
        lbl("cp_interval_lbl")
        iv_row = QWidget(); ivh = QHBoxLayout(iv_row); ivh.setContentsMargins(0,0,0,4)
        self._interval_e = QLineEdit(ex.get("interval_str","00:00"))
        self._interval_e.setMaximumWidth(100)
        iv_hint = QLabel(T("cp_interval_hint", lang))
        iv_hint.setStyleSheet("color:#505a72;font-size:11px;")
        ivh.addWidget(self._interval_e); ivh.addSpacing(8); ivh.addWidget(iv_hint); ivh.addStretch()
        layout.addWidget(iv_row)

        # ── Credit file ───────────────────────────────────────────────────
        lbl("cp_file_lbl")
        file_w = QWidget(); fh = QHBoxLayout(file_w); fh.setContentsMargins(0,0,0,4)
        self._file_e = QLineEdit(ex.get("file","")); self._file_e.setPlaceholderText("...")
        browse_btn = QPushButton(T("btn_browse", lang))
        browse_btn.setFixedWidth(40); browse_btn.clicked.connect(self._browse_file)
        fh.addWidget(self._file_e); fh.addWidget(browse_btn)
        layout.addWidget(file_w)

        # ── Volume ────────────────────────────────────────────────────────
        lbl("cp_vol_lbl")
        vol_w = QWidget(); vh = QHBoxLayout(vol_w); vh.setContentsMargins(0,0,0,4)
        self._vol_sl = QSlider(Qt.Orientation.Horizontal)
        self._vol_sl.setRange(0,100); self._vol_sl.setValue(int(ex.get("volume",1.0)*100))
        self._vol_lbl = QLabel(f"{self._vol_sl.value()}%"); self._vol_lbl.setFixedWidth(38)
        self._vol_sl.valueChanged.connect(lambda v: self._vol_lbl.setText(f"{v}%"))
        vh.addWidget(self._vol_sl); vh.addWidget(self._vol_lbl)
        layout.addWidget(vol_w)

        # ── Ducking ───────────────────────────────────────────────────────
        lbl("cp_duck_lbl")
        duck_w = QWidget(); dh = QHBoxLayout(duck_w); dh.setContentsMargins(0,0,0,4)
        self._duck_combo = QComboBox()
        duck_items = [
            (T("cp_duck_off",  lang),  0),
            (T("cp_duck_low",  lang), 10),
            (T("cp_duck_mid",  lang), 20),
            (T("cp_duck_high", lang), 30),
        ]
        for label, val in duck_items:
            self._duck_combo.addItem(label, val)
        saved_duck = ex.get("duck_db", 0)
        for i in range(self._duck_combo.count()):
            if self._duck_combo.itemData(i) == saved_duck:
                self._duck_combo.setCurrentIndex(i); break
        self._duck_combo.setMaximumWidth(180)
        dh.addWidget(self._duck_combo); dh.addStretch()
        layout.addWidget(duck_w)

        sep = QFrame(); sep.setObjectName("hline"); sep.setFixedHeight(1); layout.addWidget(sep)

        # ── Buttons ───────────────────────────────────────────────────────
        btns = QHBoxLayout()
        ok_btn = QPushButton(T("btn_ok", lang)); ok_btn.setObjectName("accent")
        ok_btn.clicked.connect(self._ok)
        ca_btn = QPushButton(T("btn_cancel_dlg", lang)); ca_btn.clicked.connect(self.reject)
        if rtl:
            btns.addWidget(ca_btn); btns.addStretch(); btns.addWidget(ok_btn)
        else:
            btns.addStretch(); btns.addWidget(ca_btn); btns.addWidget(ok_btn)
        layout.addLayout(btns)

        self._rb_start.toggled.connect(self._on_pos)
        self._rb_end.toggled.connect(self._on_pos)
        self._rb_insert.toggled.connect(self._on_mode)
        self._on_mode(); self._on_pos()

    def _on_mode(self):
        insert = self._rb_insert.isChecked()
        self._pos_w.setEnabled(insert)
        self._time_e.setEnabled(insert)

    def _on_pos(self):
        if not self._rb_insert.isChecked(): return
        if   self._rb_start.isChecked(): self._time_e.setText("00:00"); self._time_e.setEnabled(False)
        elif self._rb_end.isChecked():   self._time_e.setText("end");   self._time_e.setEnabled(False)
        else:                             self._time_e.setEnabled(True)

    def _browse_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "", "",
            "Audio Files (" + " ".join(f"*{e}" for e in SUPPORTED_FORMATS) + ")")
        if f: self._file_e.setText(f)

    def _ok(self):
        f = self._file_e.text().strip()
        if not f:   QMessageBox.warning(self,"",T("err_no_file",   self.lang)); return
        if not Path(f).exists():
                    QMessageBox.warning(self,"",T("err_file_missing",self.lang)); return
        mode = "overlay" if self._rb_overlay.isChecked() else "insert"
        pos  = ("start" if self._rb_start.isChecked() else
                "end"   if self._rb_end.isChecked()   else "mid")
        ts   = self._time_e.text().strip()
        ivs  = self._interval_e.text().strip()
        t_sec = "end" if pos=="end" else (0.0 if pos=="start" else parse_time(ts))
        iv_ms = int(parse_time(ivs)*1000) if ivs and ivs != "00:00" else 0
        self.result_data = {
            "file": f, "time_sec": t_sec, "time_str": ts,
            "volume": self._vol_sl.value()/100.0,
            "position": pos, "mode": mode,
            "interval_ms": iv_ms, "interval_str": ivs,
            "duck_db": self._duck_combo.currentData(),
        }
        self.accept()


# ══════════════════════════════════════════════════════════════════════════════
# DROP ZONE
# ══════════════════════════════════════════════════════════════════════════════

class DropZone(QLabel):
    files_dropped = pyqtSignal(list)

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("dropzone")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(100)
        self.setStyleSheet("""
            QLabel#dropzone {
                border: 2px dashed #334273;
                border-radius: 8px;
                color: #8b97b3;
                font-size: 13px;
                padding: 12px;
            }
            QLabel#dropzone:hover {
                border-color: #5b8cff;
                color: #e8ecf4;
            }
        """)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls(): e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        paths = [u.toLocalFile() for u in e.mimeData().urls()
                 if Path(u.toLocalFile()).suffix.lower() in SUPPORTED_FORMATS]
        if paths: self.files_dropped.emit(paths)

    def mousePressEvent(self, _): self.files_dropped.emit([])

# ══════════════════════════════════════════════════════════════════════════════
# MAIN WINDOW
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._settings  = load_settings()
        self._lang      = self._settings.get("lang", "he")
        self._theme     = self._settings.get("theme", "dark")
        self._files     = []
        self._credits   = []
        self._cancel_ev = threading.Event()
        self._worker    = None

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1100, 720)
        self._apply_theme()
        self._build_ui()
        self._refresh_files()
        self._refresh_credits()
        self._check_deps()

    # ── Theme ─────────────────────────────────────────────────────────────────
    def _apply_theme(self):
        p   = PALETTES[self._theme]
        rtl = self._lang == "he"
        self.setStyleSheet(_qss(p, rtl))
        # Do NOT set app-level LayoutDirection — we control sidebar side manually

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        rtl = self._lang == "he"
        p   = PALETTES[self._theme]

        container = QWidget()
        outer_v = QVBoxLayout(container)
        outer_v.setContentsMargins(0,0,0,0); outer_v.setSpacing(0)

        # ── Main row: sidebar + page stack ──
        root = QWidget()
        main_h = QHBoxLayout(root); main_h.setContentsMargins(0,0,0,0); main_h.setSpacing(0)

        # ── Sidebar ──
        sidebar = QFrame(); sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sb_v = QVBoxLayout(sidebar); sb_v.setContentsMargins(0,0,0,6); sb_v.setSpacing(0)

        # ── Logo / branding area ──
        logo_w = QWidget()
        logo_w.setObjectName("logoblock")
        logo_w.setStyleSheet(f"""
            QWidget#logoblock {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {p['accent']}, stop:1 {p['bg2']});
                border-bottom: 1px solid {p['border2']};
            }}
            QLabel {{ background: transparent; }}
        """)
        logo_v = QVBoxLayout(logo_w)
        logo_v.setContentsMargins(16, 18, 16, 16)
        logo_v.setSpacing(4)
        logo_al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft

        # Big emoji icon
        icon_lbl = QLabel("🎵")
        icon_lbl.setAlignment(logo_al)
        icon_lbl.setStyleSheet("font-size:40px; background:transparent; padding-bottom:4px;")
        logo_v.addWidget(icon_lbl)

        # Main title: Hebrew → show subtitle ("משלב הקרדיט") as big name
        #             English → show APP_NAME ("AudioCraft Pro")
        main_title = T("app_subtitle", self._lang) if rtl else APP_NAME
        app_lbl = QLabel(main_title)
        app_lbl.setAlignment(logo_al)
        app_lbl.setStyleSheet(
            "font-size:20px; font-weight:bold; color:#ffffff; background:transparent; letter-spacing:0.3px;")
        logo_v.addWidget(app_lbl)

        # Version directly below the title
        ver_lbl = QLabel(f"v{APP_VERSION}")
        ver_lbl.setAlignment(logo_al)
        ver_lbl.setStyleSheet("font-size:11px; color:rgba(255,255,255,0.5); background:transparent;")
        logo_v.addWidget(ver_lbl)

        # English only: small subtitle below version
        if not rtl:
            sub_lbl = QLabel("Credit Mixer")
            sub_lbl.setAlignment(logo_al)
            sub_lbl.setStyleSheet("font-size:11px; color:rgba(255,255,255,0.55); background:transparent;")
            logo_v.addWidget(sub_lbl)

        sb_v.addWidget(logo_w)

        # ── Nav items ──
        self._nav_btns = {}

        def _nav(key, page_id):
            btn = QPushButton(T(key, self._lang))
            btn.setObjectName("navbtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, p=page_id: self._show_page(p))
            sb_v.addWidget(btn)
            self._nav_btns[page_id] = btn

        def _sep():
            f = QFrame(); f.setObjectName("hline"); f.setFixedHeight(1)
            sb_v.addWidget(f)

        def _sec_lbl(text):
            l = QLabel(text)
            l.setObjectName("seclabel")
            sb_v.addWidget(l)

        _sep()
        _nav("nav_files",   "files")
        _nav("nav_credits", "credits")
        _nav("nav_export",  "export")
        _sep()
        _nav("nav_settings","settings")
        _nav("nav_about",   "about")

        sb_v.addStretch()
        _sep()

        self._status_sidebar = QLabel("")
        self._status_sidebar.setWordWrap(True)
        self._status_sidebar.setStyleSheet("color:#505a72;font-size:11px;padding:6px 14px;")
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft
        self._status_sidebar.setAlignment(al)
        sb_v.addWidget(self._status_sidebar)

        # ── Page stack ──
        self._stack = QStackedWidget()
        self._pages = {}
        for pid, builder in [
            ("files",    self._build_files_page),
            ("credits",  self._build_credits_page),
            ("export",   self._build_export_page),
            ("settings", self._build_settings_page),
            ("about",    self._build_about_page),
        ]:
            w = QWidget(); builder(w); self._stack.addWidget(w); self._pages[pid] = w

        # Sidebar RIGHT for Hebrew, LEFT for English
        if rtl:
            main_h.addWidget(self._stack)
            main_h.addWidget(sidebar)
        else:
            main_h.addWidget(sidebar)
            main_h.addWidget(self._stack)

        outer_v.addWidget(root)

        # ── Status bar (bottom) ──
        self._statusbar = QLabel(T("status_ready", self._lang))
        self._statusbar.setObjectName("statusbar")
        self._statusbar.setFixedHeight(26)
        outer_v.addWidget(self._statusbar)

        # ── Top bar: theme toggle ──
        topbar = QWidget()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(34)
        tb_h = QHBoxLayout(topbar)
        tb_h.setContentsMargins(12,0,12,0); tb_h.setSpacing(6)

        icon_dark  = "🌙  כהה"  if rtl else "🌙  Dark"
        icon_light = "☀  בהיר" if rtl else "☀  Light"
        toggle_lbl = icon_dark if self._theme == "light" else icon_light
        self._theme_toggle_btn = QPushButton(toggle_lbl)
        self._theme_toggle_btn.setObjectName("topbarbtn")
        self._theme_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_toggle_btn.setFixedHeight(24)
        self._theme_toggle_btn.clicked.connect(self._quick_toggle_theme)

        # Separator label
        sep_lbl = QLabel("|")
        sep_lbl.setStyleSheet("color:#505a72; font-size:13px;")

        status_lbl = QLabel(f"{APP_NAME}  v{APP_VERSION}")
        status_lbl.setStyleSheet("color:#8b97b3; font-size:11px;")

        if rtl:
            tb_h.addWidget(self._theme_toggle_btn)
            tb_h.addWidget(sep_lbl)
            tb_h.addStretch()
            tb_h.addWidget(status_lbl)
        else:
            tb_h.addWidget(status_lbl)
            tb_h.addStretch()
            tb_h.addWidget(sep_lbl)
            tb_h.addWidget(self._theme_toggle_btn)

        outer_v.insertWidget(0, topbar)

        self.setCentralWidget(container)
        self._show_page("files")

    def _show_page(self, page_id):
        if page_id not in self._pages: return
        self._stack.setCurrentWidget(self._pages[page_id])
        for pid, btn in self._nav_btns.items():
            btn.setProperty("active", pid == page_id)
            btn.style().unpolish(btn); btn.style().polish(btn)

    # ── PAGE: FILES ───────────────────────────────────────────────────────────
    def _build_files_page(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(24,20,24,20); layout.setSpacing(12)
        rtl = self._lang == "he"

        # Title row
        th = QHBoxLayout()
        title = QLabel(T("files_title", self._lang)); title.setObjectName("sectiontitle")
        sub   = QLabel(T("files_subtitle", self._lang)); sub.setObjectName("sectionsubtitle")
        if rtl:
            th.addStretch(); th.addWidget(sub); th.addSpacing(12); th.addWidget(title)
        else:
            th.addWidget(title); th.addSpacing(12); th.addWidget(sub); th.addStretch()
        layout.addLayout(th)

        # Buttons
        bh = QHBoxLayout(); bh.setSpacing(8)
        self._btn_add_f = QPushButton(T("btn_add_files", self._lang)); self._btn_add_f.setObjectName("accent")
        self._btn_add_d = QPushButton(T("btn_add_folder", self._lang))
        self._btn_rem   = QPushButton(T("btn_remove", self._lang))
        self._btn_clr   = QPushButton(T("btn_clear", self._lang)); self._btn_clr.setObjectName("danger")
        self._btn_add_f.clicked.connect(self._add_files)
        self._btn_add_d.clicked.connect(self._add_folder)
        self._btn_rem.clicked.connect(self._remove_file)
        self._btn_clr.clicked.connect(self._clear_files)
        if rtl:
            bh.addWidget(self._btn_clr); bh.addWidget(self._btn_rem)
            bh.addStretch()
            bh.addWidget(self._btn_add_d); bh.addWidget(self._btn_add_f)
        else:
            bh.addWidget(self._btn_add_f); bh.addWidget(self._btn_add_d)
            bh.addStretch()
            bh.addWidget(self._btn_rem); bh.addWidget(self._btn_clr)
        layout.addLayout(bh)

        # Drop zone
        self._drop_zone = DropZone(T("drop_hint", self._lang))
        self._drop_zone.files_dropped.connect(self._on_drop)
        layout.addWidget(self._drop_zone)

        # File count badge
        ch = QHBoxLayout()
        self._files_badge = QLabel(T("n_files", self._lang, n=0))
        self._files_badge.setStyleSheet(
            "background:#1e2332;color:#7fa8ff;border-radius:4px;padding:2px 10px;font-size:12px;")
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft
        self._files_badge.setAlignment(al)
        if rtl: ch.addStretch(); ch.addWidget(self._files_badge)
        else:   ch.addWidget(self._files_badge); ch.addStretch()
        layout.addLayout(ch)

        # Tree
        self._ftree = QTreeWidget()
        self._ftree.setAlternatingRowColors(True)
        self._ftree.setRootIsDecorated(False)
        hdrs = [T("col_type",self._lang), T("col_name",self._lang),
                T("col_dur",self._lang),  T("col_size",self._lang)]
        self._ftree.setHeaderLabels(hdrs)
        self._ftree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._ftree.setColumnWidth(0, 55); self._ftree.setColumnWidth(2, 80); self._ftree.setColumnWidth(3, 90)
        self._ftree.itemDoubleClicked.connect(lambda: self._remove_file())
        layout.addWidget(self._ftree)

    def _on_drop(self, paths):
        if not paths:
            self._add_files(); return
        added = 0
        for p in paths:
            if p not in self._files: self._files.append(p); added+=1
        self._refresh_files()

    def _add_files(self):
        exts = " ".join(f"*{e}" for e in SUPPORTED_FORMATS)
        files, _ = QFileDialog.getOpenFileNames(self, "", "", f"Audio Files ({exts})")
        added = 0
        for f in files:
            if f not in self._files: self._files.append(f); added+=1
        self._refresh_files()
        if added: self._set_status(f"+{added}")

    def _add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "")
        if not folder: return
        added = 0
        for ext in SUPPORTED_FORMATS:
            for f in Path(folder).glob(f"*{ext}"):
                if str(f) not in self._files: self._files.append(str(f)); added+=1
        self._refresh_files()
        if added: self._set_status(f"+{added}")

    def _remove_file(self):
        sel = self._ftree.selectedItems()
        if sel:
            idx = self._ftree.indexOfTopLevelItem(sel[0])
            if 0 <= idx < len(self._files):
                self._files.pop(idx); self._refresh_files()

    def _clear_files(self):
        if self._files:
            self._files.clear(); self._refresh_files()

    def _refresh_files(self):
        self._ftree.clear()
        for f in self._files:
            try:
                info = get_info(f)
                item = QTreeWidgetItem([info["ext"], info["name"],
                                        info["dur_str"], f"{info['sz']:.1f} MB"])
                item.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
                item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
                item.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
                self._ftree.addTopLevelItem(item)
            except: pass
        n = len(self._files)
        self._files_badge.setText(T("n_files", self._lang, n=n))
        self._status_sidebar.setText(T("n_files", self._lang, n=n))
        # Sync export list
        try: self._refresh_export_list()
        except: pass

    # ── PAGE: CREDITS ─────────────────────────────────────────────────────────
    def _build_credits_page(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(24,20,24,20); layout.setSpacing(12)
        rtl = self._lang == "he"

        title = QLabel(T("credits_title", self._lang)); title.setObjectName("sectiontitle")
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft
        title.setAlignment(al); layout.addWidget(title)

        # Buttons
        bh = QHBoxLayout(); bh.setSpacing(8)
        self._btn_add_cp  = QPushButton(T("btn_add_cp",  self._lang)); self._btn_add_cp.setObjectName("accent")
        self._btn_edit_cp = QPushButton(T("btn_edit_cp", self._lang))
        self._btn_del_cp  = QPushButton(T("btn_del_cp",  self._lang)); self._btn_del_cp.setObjectName("danger")
        self._btn_add_cp.clicked.connect(self._add_cp)
        self._btn_edit_cp.clicked.connect(self._edit_cp)
        self._btn_del_cp.clicked.connect(self._del_cp)
        if rtl:
            bh.addWidget(self._btn_del_cp); bh.addStretch()
            bh.addWidget(self._btn_edit_cp); bh.addWidget(self._btn_add_cp)
        else:
            bh.addWidget(self._btn_add_cp); bh.addWidget(self._btn_edit_cp)
            bh.addStretch(); bh.addWidget(self._btn_del_cp)
        layout.addLayout(bh)

        # Tree
        self._cptree = QTreeWidget()
        self._cptree.setAlternatingRowColors(True)
        self._cptree.setRootIsDecorated(False)
        hdrs = [T("col_pos",self._lang), T("col_time",self._lang),
                T("col_file",self._lang), T("col_vol",self._lang)]
        self._cptree.setHeaderLabels(hdrs)
        self._cptree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self._cptree.setColumnWidth(0, 110); self._cptree.setColumnWidth(1, 80); self._cptree.setColumnWidth(3, 70)
        self._cptree.itemDoubleClicked.connect(lambda: self._edit_cp())
        layout.addWidget(self._cptree)

    def _add_cp(self):
        d = CreditDialog(self, self._lang)
        if d.exec() and d.result_data:
            self._credits.append(d.result_data); self._refresh_credits()

    def _edit_cp(self):
        sel = self._cptree.selectedItems()
        if not sel: return
        idx = self._cptree.indexOfTopLevelItem(sel[0])
        d = CreditDialog(self, self._lang, existing=self._credits[idx])
        if d.exec() and d.result_data:
            self._credits[idx] = d.result_data; self._refresh_credits()

    def _del_cp(self):
        sel = self._cptree.selectedItems()
        if sel:
            idx = self._cptree.indexOfTopLevelItem(sel[0])
            self._credits.pop(idx); self._refresh_credits()

    def _refresh_credits(self):
        self._cptree.clear()
        pos_map = {
            "start": T("pos_start", self._lang),
            "mid":   T("pos_mid",   self._lang),
            "end":   T("pos_end",   self._lang),
        }
        for cp in self._credits:
            mode = cp.get("mode","insert")
            iv   = cp.get("interval_str","00:00")
            pos_str = pos_map.get(cp.get("position","mid"),"")
            if mode == "overlay":
                pos_str = "⬛ " + ("שכבה" if self._lang=="he" else "overlay")
            elif iv and iv not in ("00:00",""):
                pos_str = f"🔁 /{iv}"
            item = QTreeWidgetItem([
                pos_str,
                cp.get("time_str",""),
                Path(cp.get("file","")).name,
                f"{int(cp.get('volume',1.0)*100)}%"
            ])
            item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
            item.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
            self._cptree.addTopLevelItem(item)

    def _build_cover_page(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(24,20,24,20); layout.setSpacing(14)
        rtl = self._lang == "he"
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft

        title = QLabel(T("cover_title", self._lang)); title.setObjectName("sectiontitle")
        title.setAlignment(al); layout.addWidget(title)

        desc = QLabel(T("cover_desc", self._lang)); desc.setObjectName("sectionsubtitle")
        desc.setWordWrap(True); desc.setAlignment(al); layout.addWidget(desc)

        # Card
        card = QFrame(); card.setObjectName("card")
        cl = QVBoxLayout(card); cl.setContentsMargins(16,14,16,14); cl.setSpacing(10)

        path_lbl = QLabel(T("cover_path_lbl", self._lang)); path_lbl.setAlignment(al); cl.addWidget(path_lbl)
        ph = QHBoxLayout()
        self._cover_edit = QLineEdit(); self._cover_edit.setReadOnly(True)
        browse_btn = QPushButton(T("btn_browse_cover", self._lang))
        browse_btn.clicked.connect(self._browse_cover)
        if rtl:
            ph.addWidget(browse_btn); ph.addWidget(self._cover_edit)
        else:
            ph.addWidget(self._cover_edit); ph.addWidget(browse_btn)
        cl.addLayout(ph)

        self._embed_chk = QCheckBox(T("embed_cover_chk", self._lang))
        self._embed_chk.setChecked(True); cl.addWidget(self._embed_chk)

        # Preview
        self._cover_prev = QLabel()
        self._cover_prev.setFixedSize(160,160)
        self._cover_prev.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._cover_prev.setStyleSheet("border:1px solid #1e2538;border-radius:4px;background:#0f1219;color:#505a72;")
        self._cover_prev.setText("preview")
        prev_h = QHBoxLayout()
        prev_h.addStretch(); prev_h.addWidget(self._cover_prev); prev_h.addStretch()
        cl.addLayout(prev_h)
        layout.addWidget(card)
        layout.addStretch()

    def _browse_cover(self):
        f, _ = QFileDialog.getOpenFileName(self, "", "",
            "Images (*.jpg *.jpeg *.png *.bmp)")
        if f:
            self._cover_edit.setText(f)
            if PIL_OK:
                try:
                    from PIL import Image as _I
                    from PyQt6.QtGui import QPixmap
                    img = _I.open(f).resize((158,158))
                    import io; buf = io.BytesIO()
                    img.save(buf, "PNG"); buf.seek(0)
                    px = QPixmap()
                    px.loadFromData(buf.read())
                    self._cover_prev.setPixmap(px); self._cover_prev.setText("")
                except: pass

    # ── PAGE: EXPORT ───────────────────────────────────────────────────────────
    def _build_export_page(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(24,20,24,20); layout.setSpacing(14)
        rtl = self._lang == "he"
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft

        title = QLabel(T("export_title", self._lang)); title.setObjectName("sectiontitle")
        title.setAlignment(al); layout.addWidget(title)

        # Two-column split
        split = QHBoxLayout(); split.setSpacing(16)

        # ── Left card: settings ──
        lcard = QFrame(); lcard.setObjectName("card")
        ll = QVBoxLayout(lcard); ll.setContentsMargins(16,14,16,14); ll.setSpacing(10)

        # Output dir
        od_lbl = QLabel(T("outdir_lbl", self._lang)); od_lbl.setAlignment(al); ll.addWidget(od_lbl)
        od_h = QHBoxLayout()
        self._out_dir_edit = QLineEdit()
        self._out_dir_edit.setPlaceholderText(T("outdir_default", self._lang))
        saved_dir = self._settings.get("output_dir","")
        if saved_dir: self._out_dir_edit.setText(saved_dir)
        browse_dir_btn = QPushButton(T("btn_browse_dir", self._lang))
        browse_dir_btn.setFixedWidth(40)
        browse_dir_btn.clicked.connect(self._browse_outdir)
        if rtl:
            od_h.addWidget(browse_dir_btn); od_h.addWidget(self._out_dir_edit)
        else:
            od_h.addWidget(self._out_dir_edit); od_h.addWidget(browse_dir_btn)
        ll.addLayout(od_h)

        sep = QFrame(); sep.setObjectName("hline"); sep.setFixedHeight(1); ll.addWidget(sep)

        # Format
        fmt_lbl = QLabel(T("format_lbl", self._lang)); fmt_lbl.setAlignment(al); ll.addWidget(fmt_lbl)
        self._fmt_combo = QComboBox()
        fmt_keys  = ["source","mp3","wav","flac","aac"]
        fmt_labels= [T("fmt_source",self._lang), T("fmt_mp3",self._lang),
                     T("fmt_wav",self._lang),    T("fmt_flac",self._lang), T("fmt_aac",self._lang)]
        self._fmt_keys = fmt_keys
        for lbl in fmt_labels: self._fmt_combo.addItem(lbl)
        saved_fmt = self._settings.get("output_format","source")
        if saved_fmt in fmt_keys: self._fmt_combo.setCurrentIndex(fmt_keys.index(saved_fmt))
        ll.addWidget(self._fmt_combo)

        sep2 = QFrame(); sep2.setObjectName("hline"); sep2.setFixedHeight(1); ll.addWidget(sep2)

        # Suffix / naming
        suf_lbl = QLabel(T("suffix_lbl", self._lang)); suf_lbl.setAlignment(al); ll.addWidget(suf_lbl)
        self._suf_orig   = QRadioButton(T("suffix_original", self._lang))
        self._suf_credit = QRadioButton(T("suffix_credit",   self._lang))
        self._suf_custom = QRadioButton(T("suffix_custom",   self._lang))
        self._suf_grp = QButtonGroup(); 
        [self._suf_grp.addButton(r) for r in [self._suf_orig, self._suf_credit, self._suf_custom]]
        self._suf_input = QLineEdit(self._settings.get("output_suffix","קרדיט"))
        self._suf_input.setMaximumWidth(160)
        saved_mode = self._settings.get("output_mode","original")
        {"original": self._suf_orig, "add_credit": self._suf_credit,
         "custom": self._suf_custom}.get(saved_mode, self._suf_orig).setChecked(True)
        self._suf_input.setEnabled(saved_mode=="custom")
        self._suf_custom.toggled.connect(lambda c: self._suf_input.setEnabled(c))
        for rb in [self._suf_orig, self._suf_credit, self._suf_custom]: ll.addWidget(rb)
        cust_h = QHBoxLayout()
        if rtl: cust_h.addStretch(); cust_h.addWidget(self._suf_input)
        else:   cust_h.addWidget(QLabel("   ")); cust_h.addWidget(self._suf_input); cust_h.addStretch()
        ll.addLayout(cust_h)

        sep3 = QFrame(); sep3.setObjectName("hline"); sep3.setFixedHeight(1); ll.addWidget(sep3)

        # Cover in export
        cv_lbl = QLabel(T("cover_exp_lbl", self._lang)); cv_lbl.setAlignment(al); ll.addWidget(cv_lbl)
        cv_h = QHBoxLayout()
        self._exp_cover_edit = QLineEdit(); self._exp_cover_edit.setReadOnly(True)
        cv_browse = QPushButton(T("btn_browse", self._lang)); cv_browse.setFixedWidth(40)
        cv_browse.clicked.connect(self._browse_cover_exp)
        if rtl: cv_h.addWidget(cv_browse); cv_h.addWidget(self._exp_cover_edit)
        else:   cv_h.addWidget(self._exp_cover_edit); cv_h.addWidget(cv_browse)
        ll.addLayout(cv_h)
        self._embed_exp_chk = QCheckBox(T("embed_exp_chk", self._lang))
        self._embed_exp_chk.setChecked(True); ll.addWidget(self._embed_exp_chk)

        ll.addStretch()

        # Start / Cancel
        self._btn_start  = QPushButton(T("btn_start",  self._lang)); self._btn_start.setObjectName("success")
        self._btn_cancel_proc = QPushButton(T("btn_cancel", self._lang)); self._btn_cancel_proc.setObjectName("danger")
        self._btn_cancel_proc.setEnabled(False)
        self._btn_start.clicked.connect(self._start_processing)
        self._btn_cancel_proc.clicked.connect(self._cancel_processing)
        ll.addWidget(self._btn_start); ll.addWidget(self._btn_cancel_proc)

        # ── Right card: file list + progress ──
        rcard = QFrame(); rcard.setObjectName("card")
        rl = QVBoxLayout(rcard); rl.setContentsMargins(16,14,16,14); rl.setSpacing(10)

        fl_lbl = QLabel(T("export_files_lbl", self._lang)); fl_lbl.setAlignment(al); rl.addWidget(fl_lbl)
        self._exp_file_list = QListWidget()
        self._exp_file_list.setAlternatingRowColors(True)
        rl.addWidget(self._exp_file_list)

        self._prog_bar = QProgressBar(); self._prog_bar.setRange(0,100); self._prog_bar.setValue(0)
        rl.addWidget(self._prog_bar)

        self._prog_lbl = QLabel(""); self._prog_lbl.setAlignment(al)
        self._prog_lbl.setStyleSheet("font-size:12px;color:#8b97b3;"); rl.addWidget(self._prog_lbl)

        if rtl: split.addWidget(rcard); split.addWidget(lcard)
        else:   split.addWidget(lcard); split.addWidget(rcard)
        layout.addLayout(split)

    def _refresh_export_list(self):
        try:
            self._exp_file_list.clear()
            for f in self._files:
                item = QListWidgetItem(Path(f).name)
                self._exp_file_list.addItem(item)
        except: pass

    def _browse_outdir(self):
        d = QFileDialog.getExistingDirectory(self, "")
        if d:
            self._out_dir_edit.setText(d)
            self._settings["output_dir"] = d; save_settings(self._settings)

    def _browse_cover_exp(self):
        f, _ = QFileDialog.getOpenFileName(self, "", "", "Images (*.jpg *.jpeg *.png *.bmp)")
        if f: self._exp_cover_edit.setText(f)

    def _get_output_dir(self):
        d = self._out_dir_edit.text().strip()
        if d: return d
        out = _get_base() / "output"
        out.mkdir(exist_ok=True); return str(out)

    def _start_processing(self):
        if not self._files:
            QMessageBox.warning(self,"",T("msg_no_files",self._lang)); return
        if not self._credits:
            QMessageBox.warning(self,"",T("msg_no_credits",self._lang)); return
        if not PYDUB_OK:
            QMessageBox.critical(self,"",T("msg_no_pydub",self._lang)); return

        out_dir = self._get_output_dir()
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        fmt = self._fmt_keys[self._fmt_combo.currentIndex()]
        cover = self._exp_cover_edit.text().strip() if self._embed_exp_chk.isChecked() else None
        mute  = False  # duck is now per-credit-point (stored in each cp dict)
        mode  = ("add_credit" if self._suf_credit.isChecked() else
                 "custom"     if self._suf_custom.isChecked() else "original")
        cust  = self._suf_input.text().strip()

        # Save settings
        self._settings["output_format"] = fmt
        self._settings["output_mode"]   = mode
        self._settings["output_suffix"] = cust
        save_settings(self._settings)

        self._cancel_ev.clear()
        self._btn_start.setEnabled(False); self._btn_cancel_proc.setEnabled(True)
        self._prog_bar.setValue(0); self._set_status(T("status_processing",self._lang))

        self._worker = ProcessWorker(
            list(self._files), list(self._credits), out_dir, fmt,
            cover, mute, mode, cust, self._cancel_ev
        )
        self._worker.signals.progress.connect(self._on_progress)
        self._worker.signals.log_msg.connect(lambda m,l: log.info(f"[{l}] {m}"))
        self._worker.signals.finished.connect(self._on_done)
        self._worker.start()

    def _cancel_processing(self):
        self._cancel_ev.set()
        self._set_status(T("status_cancelled", self._lang))

    def _on_progress(self, done, total, label):
        pct = int(done/total*100) if total else 0
        self._prog_bar.setValue(pct)
        self._prog_lbl.setText(f"{label}  ({done}/{total})")
        al = Qt.AlignmentFlag.AlignRight if self._lang=="he" else Qt.AlignmentFlag.AlignLeft
        self._prog_lbl.setAlignment(al)

    def _on_done(self, results):
        ok   = sum(1 for r in results if r["ok"])
        fail = len(results) - ok
        self._btn_start.setEnabled(True); self._btn_cancel_proc.setEnabled(False)
        self._prog_bar.setValue(100)
        self._set_status(T("status_done", self._lang))
        QMessageBox.information(self, T("msg_done_title", self._lang),
                                T("msg_done", self._lang, ok=ok, fail=fail))

    # ── PAGE: SETTINGS ────────────────────────────────────────────────────────
    def _build_settings_page(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(24,20,24,20); layout.setSpacing(16)
        rtl = self._lang == "he"
        al  = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft
        # Set layout direction on this page so sub-widgets mirror correctly
        parent.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if rtl else Qt.LayoutDirection.LeftToRight)

        title = QLabel(T("settings_title", self._lang)); title.setObjectName("sectiontitle")
        title.setAlignment(al); layout.addWidget(title)

        # ── Card ──────────────────────────────────────────────────────────
        card = QFrame(); card.setObjectName("card")
        cl = QFormLayout(card)
        cl.setContentsMargins(18,14,18,14); cl.setSpacing(14)
        cl.setFormAlignment(Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft)
        cl.setLabelAlignment(Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft)
        cl.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)

        # Language
        self._lang_combo = QComboBox()
        self._lang_combo.addItem("עברית", "he")
        self._lang_combo.addItem("English", "en")
        self._lang_combo.setCurrentIndex(0 if self._lang == "he" else 1)
        self._lang_combo.setFixedWidth(160)
        cl.addRow(T("lang_lbl", self._lang), self._lang_combo)

        # Theme (permanent via Apply button)
        self._theme_combo = QComboBox()
        self._theme_combo.addItem(T("theme_dark",  self._lang), "dark")
        self._theme_combo.addItem(T("theme_light", self._lang), "light")
        saved_theme = self._settings.get("theme", "light")
        self._theme_combo.setCurrentIndex(0 if saved_theme == "dark" else 1)
        self._theme_combo.setFixedWidth(160)
        theme_note = QLabel("← " + ("ישמר לתמיד" if rtl else "saved permanently"))
        theme_note.setStyleSheet("color:#505a72;font-size:11px;")
        theme_row = QWidget(); tr_h = QHBoxLayout(theme_row); tr_h.setContentsMargins(0,0,0,0)
        tr_h.addWidget(self._theme_combo); tr_h.addWidget(theme_note); tr_h.addStretch()
        cl.addRow(T("theme_lbl", self._lang), theme_row)

        # FFmpeg
        self._ffmpeg_edit = QLineEdit(self._settings.get("ffmpeg_path",""))
        ff_row = QWidget(); ff_h = QHBoxLayout(ff_row); ff_h.setContentsMargins(0,0,0,0)
        ff_browse = QPushButton("📂"); ff_browse.setFixedWidth(40)
        ff_browse.clicked.connect(self._browse_ffmpeg)
        ff_save = QPushButton(T("btn_save_ffmpeg", self._lang)); ff_save.setObjectName("accent")
        ff_save.clicked.connect(self._save_ffmpeg)
        ff_h.addWidget(self._ffmpeg_edit); ff_h.addWidget(ff_browse); ff_h.addWidget(ff_save)
        cl.addRow(T("ffmpeg_lbl", self._lang), ff_row)

        # Apply
        apply_btn = QPushButton("✓  " + ("החל שינויים" if rtl else "Apply Changes"))
        apply_btn.setObjectName("accent")
        apply_btn.clicked.connect(self._apply_settings)
        cl.addRow("", apply_btn)

        layout.addWidget(card)

        # ── Deps status card ──────────────────────────────────────────────
        self._deps_card = QFrame(); self._deps_card.setObjectName("card")
        dl = QVBoxLayout(self._deps_card); dl.setContentsMargins(16,12,16,12); dl.setSpacing(6)
        layout.addWidget(self._deps_card)
        layout.addStretch()

    def _browse_ffmpeg(self):
        f, _ = QFileDialog.getOpenFileName(self, "", "", "ffmpeg.exe (ffmpeg.exe);;All Files (*)")
        if f:
            self._ffmpeg_edit.setText(str(Path(f).parent))

    def _save_ffmpeg(self):
        d = self._ffmpeg_edit.text().strip()
        if d:
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH","")
            if PYDUB_OK:
                AudioSegment.converter = str(Path(d)/"ffmpeg.exe")
                AudioSegment.ffprobe   = str(Path(d)/"ffprobe.exe")
            self._settings["ffmpeg_path"] = d; save_settings(self._settings)

    def _quick_toggle_theme(self):
        """Fast toggle from topbar — temporary (not saved to settings)."""
        self._theme = "light" if self._theme == "dark" else "dark"
        # Do NOT save to settings — this is a session-only change.
        # Only Settings page → Apply persists the theme.
        self._rebuild_ui()

    def _rebuild_ui(self):
        """Rebuild the entire UI (used after lang/theme change)."""
        self._apply_theme()
        old_central = self.centralWidget()
        if old_central: old_central.deleteLater()
        self._pages = {}; self._nav_btns = {}
        self._build_ui()
        self._refresh_files(); self._refresh_credits()

    def _apply_settings(self):
        new_lang  = self._lang_combo.currentData()
        new_theme = self._theme_combo.currentData()
        self._settings["lang"]  = new_lang
        self._settings["theme"] = new_theme
        save_settings(self._settings)   # persists permanently
        self._lang  = new_lang
        self._theme = new_theme
        self._rebuild_ui()

    # ── PAGE: ABOUT ───────────────────────────────────────────────────────────
    def _build_about_page(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(24,20,24,20); layout.setSpacing(14)
        rtl = self._lang == "he"
        al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft

        title = QLabel(T("about_title", self._lang)); title.setObjectName("sectiontitle")
        title.setAlignment(al); layout.addWidget(title)

        card = QFrame(); card.setObjectName("card")
        cl = QVBoxLayout(card); cl.setContentsMargins(20,16,20,16); cl.setSpacing(8)

        def sec(text, bold=False, color="#e8ecf4"):
            lbl = QLabel(text); lbl.setWordWrap(True); lbl.setAlignment(al)
            lbl.setStyleSheet(f"color:{color};font-size:{'14px' if bold else '13px'};"
                              f"font-weight:{'bold' if bold else 'normal'};")
            cl.addWidget(lbl)

        sec(f"{APP_NAME}  v{APP_VERSION}", bold=True)
        if rtl:
            sec("משלב הקרדיט — כלי לעיבוד קבצי שמע עם הטמעת קטעי קרדיט")
        else:
            sec("Credit Mixer — A tool for embedding credit audio clips into audio files")

        sep = QFrame(); sep.setObjectName("hline"); sep.setFixedHeight(1); cl.addWidget(sep)

        sec("Libraries / ספריות:", bold=True, color="#8b97b3")
        libs = [
            ("PyQt6",    "6.x",   "GNU GPL v3",      "https://www.riverbankcomputing.com/software/pyqt/"),
            ("pydub",    "0.25+", "MIT License",     "https://github.com/jiaaro/pydub"),
            ("mutagen",  "1.47+", "GPL v2",          "https://mutagen.readthedocs.io"),
            ("Pillow",   "10.x",  "HPND License",    "https://python-pillow.org"),
            ("FFmpeg",   "6.x+",  "LGPL / GPL v2+",  "https://ffmpeg.org"),
        ]
        for name, ver, lic, url in libs:
            sec(f"• {name} {ver}  —  {lic}  —  {url}", color="#8b97b3")

        sep2 = QFrame(); sep2.setObjectName("hline"); sep2.setFixedHeight(1); cl.addWidget(sep2)
        sec(f"Log file: {LOG_PATH}", color="#505a72")
        sec("Python " + sys.version.split()[0], color="#505a72")

        layout.addWidget(card); layout.addStretch()

    # ── Deps check ────────────────────────────────────────────────────────────
    def _check_deps(self):
        try:
            cl = self._deps_card.layout()
            rtl = self._lang == "he"
            al = Qt.AlignmentFlag.AlignRight if rtl else Qt.AlignmentFlag.AlignLeft
            for dep, ok in [("pydub",PYDUB_OK),("mutagen",MUTAGEN_OK),("Pillow",PIL_OK)]:
                lbl = QLabel(f"{'✓' if ok else '⚠'}  {dep}")
                lbl.setAlignment(al)
                lbl.setStyleSheet(f"color:{'#3ecf8e' if ok else '#f5a623'};font-size:13px;")
                cl.addWidget(lbl)
            try:
                subprocess.run(["ffmpeg","-version"], capture_output=True, timeout=3)
                ff_ok = True
            except: ff_ok = False
            lbl2 = QLabel(f"{'✓' if ff_ok else '⚠'}  FFmpeg")
            lbl2.setAlignment(al)
            lbl2.setStyleSheet(f"color:{'#3ecf8e' if ff_ok else '#f5a623'};font-size:13px;")
            cl.addWidget(lbl2)
        except: pass

    # ── Status bar ────────────────────────────────────────────────────────────
    def _set_status(self, msg):
        self._statusbar.setText(msg)

    def _quick_toggle_theme(self):
        self._theme = "light" if self._theme == "dark" else "dark"
        self._settings["theme"] = self._theme
        save_settings(self._settings)
        self._apply_theme()
        old_central = self.centralWidget()
        for w in self._pages.values():
            self._stack.removeWidget(w); w.deleteLater()
        self._pages.clear(); self._nav_btns.clear()
        if old_central: old_central.deleteLater()
        self._build_ui()
        self._refresh_files(); self._refresh_credits()

    def closeEvent(self, e):
        save_settings(self._settings); super().closeEvent(e)

# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
