# 🎵 AudioCraft Pro — מדריך מלא

> עורך קרדיטים לקבצי שמע | גרסה **0.4**

---

## 📋 תוכן עניינים

1. [מה זה AudioCraft Pro](#מה-זה)
2. [דרישות מערכת](#דרישות-מערכת)
3. [הוראות התקנה שלב אחר שלב](#התקנה)
4. [מבנה הקבצים](#מבנה-קבצים)
5. [הפעלה ראשונה](#הפעלה-ראשונה)
6. [מדריך שימוש מלא](#שימוש)
7. [קמפול ל-EXE עצמאי](#קמפול)
8. [שאלות נפוצות ופתרון בעיות](#בעיות)

---

<a name="מה-זה"></a>
## 🎯 מה זה AudioCraft Pro?

**AudioCraft Pro** היא תוכנת שולחן עבודה (Windows) המאפשרת לשלב קטעי קרדיט (Credit/Bumper) בתוך קבצי שמע בצורה אוטומטית ומקצועית.

### יכולות עיקריות:
- ✅ שילוב קרדיט בהתחלה, בסוף, או בנקודות זמן מוגדרות
- ✅ עיבוד מרובה קבצים בבת אחת (Batch Processing)
- ✅ תמיכה ב-MP3, WAV, FLAC, AAC, OGG, M4A, WMA, OPUS
- ✅ ייצוא בכל פורמט ללא איבוד איכות
- ✅ הטמעת תמונת כיסוי (Cover Art) בכל קובץ
- ✅ יבוא עיצוב מ-HTML חיצוני (`theme.html`)
- ✅ ממשק עברי מלא, מותאם RTL

---

<a name="דרישות-מערכת"></a>
## 💻 דרישות מערכת

| דרישה | גרסה מינימלית |
|-------|--------------|
| מערכת הפעלה | Windows 10 / Windows 11 (64-bit) |
| Python | 3.9 ומעלה (לא נדרש בגרסת EXE) |
| RAM | 4 GB (מינימום) |
| אחסון | 200 MB פנויים |

---

<a name="התקנה"></a>
## 🛠️ הוראות התקנה שלב אחר שלב

### שלב 1 — התקן Python

1. לך לכתובת: **https://www.python.org/downloads/**
2. לחץ **"Download Python 3.x.x"**
3. ⚠️ **חשוב:** סמן **"Add Python to PATH"** לפני ההתקנה
4. לחץ **"Install Now"**

**לאימות:**
```
python --version
```

---

### שלב 2 — התקן FFmpeg

1. לך לאתר: **https://ffmpeg.org/download.html** → Windows → gyan.dev
2. הורד **ffmpeg-release-essentials.zip**
3. חלץ לתיקיה, לדוגמה: `C:\ffmpeg`

**הוספה אוטומטית ל-PATH:**
הרץ את `add_ffmpeg_to_path.bat` **כ-Administrator** — הקובץ ישאל את הנתיב ויוסיף אוטומטית.

**הוספה ידנית:**
`Win+R` → `sysdm.cpl` → Advanced → Environment Variables → Path → New → `C:\ffmpeg\bin`

**לאימות:**
```
ffmpeg -version
```

---

### שלב 3 — התקן ספריות Python

**מקובץ requirements.txt (מומלץ):**
```
pip install -r requirements.txt
```

**ידנית:**
```
pip install pydub pygame mutagen Pillow
```

| ספריה | תפקיד |
|-------|--------|
| `pydub` | עיבוד קבצי שמע |
| `pygame` | נגן שמע |
| `mutagen` | הטמעת תגיות ותמונה |
| `Pillow` | עיבוד תמונות |

---

### שלב 4 — מקם את קבצי התוכנה

```
C:\AudioCraftPro\
├── audio_craft_pro.py      ← קובץ התוכנה הראשי
├── theme.html              ← קובץ העיצוב (חייב להיות כאן!)
├── requirements.txt        ← רשימת ספריות
└── add_ffmpeg_to_path.bat  ← הגדרת FFmpeg
```

### שלב 5 — הפעלה

```
cd C:\AudioCraftPro
python audio_craft_pro.py
```

---

<a name="מבנה-קבצים"></a>
## 📁 מבנה קבצים

```
C:\AudioCraftPro\
├── audio_craft_pro.py
├── theme.html
├── requirements.txt
├── add_ffmpeg_to_path.bat
└── README.md
```

---

<a name="הפעלה-ראשונה"></a>
## 🚀 הפעלה ראשונה

יומן הפעולות יציג:
- `✓ pydub / pygame / mutagen / Pillow` — הכל תקין
- `⚠ ספריה חסרה` — הרץ `pip install -r requirements.txt`
- `✓ FFmpeg` — FFmpeg מוכן
- `⚠ FFmpeg לא נמצא` — הרץ `add_ffmpeg_to_path.bat` או הגדר ידנית בהגדרות

---

<a name="שימוש"></a>
## 📖 מדריך שימוש מלא

### שלב א — קבצי שמע
לחץ **"📂 הוסף קבצים"** או **"📁 הוסף תיקיה"**, או לחץ על אזור הגרירה.

### שלב ב — קרדיטים
לשונית **קרדיטים** → **➕ הוסף** → הגדר מיקום, זמן, קובץ ועוצמה.

| מיקום | תיאור |
|-------|--------|
| 🟢 התחלה | יוכנס בתחילת הקובץ |
| 🔵 אמצע | יוכנס בזמן שתגדיר |
| 🔴 סוף | יוכנס בסיום הקובץ |

### שלב ג — ייצוא
לשונית **ייצוא** → בחר תיקייה ופורמט → לחץ **"🚀 התחל עיבוד"**.

---

<a name="קמפול"></a>
## 📦 קמפול ל-EXE עצמאי (Windows)

קמפול מאפשר להפיץ את התוכנה **ללא התקנת Python** אצל המשתמש הסופי.

### הכנה
```
pip install pyinstaller
```

---

### סוג א' — קובץ EXE יחיד (Single File)

קובץ אחד בלבד, קל להפצה. הפעלה ראשונה איטית מעט (מחלץ זמנית לדיסק).

```
pyinstaller --onefile --windowed --name "AudioCraftPro" audio_craft_pro.py
```

הקובץ ייצא ל: `dist\AudioCraftPro.exe`

⚠️ לאחר הקמפול, העתק את `theme.html` לתיקיית `dist\` לצד ה-EXE.

---

### סוג ב' — תיקיית קבצים (Folder Mode)

תיקייה עם EXE + קבצי עזר. הפעלה מהירה יותר, עדכון קל יותר.

```
pyinstaller --onedir --windowed --name "AudioCraftPro" audio_craft_pro.py
```

התוצאה: `dist\AudioCraftPro\AudioCraftPro.exe`

העתק את `theme.html` לתוך `dist\AudioCraftPro\`.

---

### האם נדרש FFmpeg בגרסת EXE?

**כן** — FFmpeg הוא תוכנה חיצונית ואינה נכללת בקמפול הרגיל.

**אפשרות 1:** המשתמש מתקין FFmpeg בנפרד ומריץ `add_ffmpeg_to_path.bat`.

**אפשרות 2 (מומלצת להפצה):** כלול FFmpeg בתוך חבילת הקמפול:

```
pyinstaller --onefile --windowed --name "AudioCraftPro" ^
  --add-binary "C:\ffmpeg\bin\ffmpeg.exe;." ^
  --add-binary "C:\ffmpeg\bin\ffprobe.exe;." ^
  audio_craft_pro.py
```

כך המשתמש **לא צריך להתקין FFmpeg בנפרד**.

---

### פקודות קמפול מומלצות — סיכום

**קובץ יחיד (ללא FFmpeg מובנה):**
```
pyinstaller --onefile --windowed --name "AudioCraftPro" audio_craft_pro.py
```

**קובץ יחיד (עם FFmpeg מובנה — מומלץ להפצה):**
```
pyinstaller --onefile --windowed --name "AudioCraftPro" ^
  --add-binary "C:\ffmpeg\bin\ffmpeg.exe;." ^
  --add-binary "C:\ffmpeg\bin\ffprobe.exe;." ^
  audio_craft_pro.py
```

**תיקיית קבצים (עם FFmpeg מובנה — מומלץ לפיתוח):**
```
pyinstaller --onedir --windowed --name "AudioCraftPro" ^
  --add-binary "C:\ffmpeg\bin\ffmpeg.exe;." ^
  --add-binary "C:\ffmpeg\bin\ffprobe.exe;." ^
  audio_craft_pro.py
```

> 💡 **המלצה:** `--onedir` — הפעלה מהירה יותר ועדכונים קלים; `--onefile` — הפצה נוחה יותר למשתמשים.

---

---

<a name="ffmpeg-local"></a>
## 🔧 FFmpeg — שימוש בגרסת EXE ללא התקנה ב-PATH

**החל מגרסה 0.4**, התוכנה מזהה אוטומטית `ffmpeg.exe` אם הוא מונח **לצד קובץ ה-EXE** — ללא צורך להוסיף ל-PATH של Windows.

### איך זה עובד

בהפעלה, התוכנה מחפשת `ffmpeg.exe` בתיקיית ה-EXE (או תיקיית ה-`.py` בהרצת מקור). אם נמצא — הוא בשימוש אוטומטית. אם לא נמצא — התוכנה תנסה למצוא ffmpeg ב-PATH של המערכת כגיבוי.

### מה לכלול בהפצה

```
AudioCraftPro\
├── AudioCraftPro.exe    ← קובץ ה-EXE (מ-PyInstaller)
├── ffmpeg.exe           ← מתוך ffmpeg-release-essentials.zip\bin\
├── ffprobe.exe          ← מתוך ffmpeg-release-essentials.zip\bin\
├── theme.html           ← קובץ העיצוב
└── (קבצי _internal\* אם השתמשת ב--onedir)
```

> ✅ **כן** — מספיק ש-`ffmpeg.exe` יהיה לצד ה-EXE. אין צורך ב-PATH, אין צורך בהתקנה נפרדת.
> ✅ **כן** — זה עובד גם ב-`--onefile` וגם ב-`--onedir`.
> ❌ **לא** — אם `ffmpeg.exe` לא נמצא בשום מקום, עיבוד קבצי M4A/AAC ייכשל.

---

<a name="inno-setup"></a>
## 📦 יצירת מעטפת התקנה עם Inno Setup

Inno Setup מאפשר ליצור קובץ `.exe` אחד שמתקין את התוכנה כמו כל תוכנה מקצועית — עם אשף התקנה, קיצורי דרך, והסרת התקנה נוחה.

### הורדת Inno Setup

**https://jrsoftware.org/isinfo.php** → Download → הורד את הגרסה האחרונה (**Inno Setup 6.x**)

---

### קבצים שיש להכין לפני הקמפול

#### שלב א' — קמפל את Python ל-EXE

```
pyinstaller --onedir --windowed --name "AudioCraftPro" audio_craft_pro.py
```

#### שלב ב' — סדר את התיקייה כך:

```
project\
├── AudioCraftPro_Setup.iss    ← קובץ Inno Setup (מצורף)
├── theme.html
├── README.md
├── ffmpeg\
│   └── bin\
│       ├── ffmpeg.exe         ← מתוך ffmpeg-release-essentials.zip
│       └── ffprobe.exe
└── dist\
    └── AudioCraftPro\        ← תוצאת PyInstaller
        ├── AudioCraftPro.exe
        ├── _internal\
        └── ...
```

**מאיפה מורידים FFmpeg:**
1. לך ל-**https://www.gyan.dev/ffmpeg/builds/**
2. הורד **ffmpeg-release-essentials.zip**
3. חלץ — תמצא תיקיית `bin` עם `ffmpeg.exe` ו-`ffprobe.exe`

---

### שלב ג' — ערוך את קובץ ה-ISS

פתח את `AudioCraftPro_Setup.iss` בעורך טקסט או ב-Inno Setup IDE ובדוק שהנתיבים נכונים:

```pascal
; קובצי PyInstaller
Source: "dist\AudioCraftPro\*"; DestDir: "{app}"; ...

; FFmpeg (שנה את הנתיב אם חילצת למקום אחר)
Source: "ffmpeg\bin\ffmpeg.exe";  DestDir: "{app}"; ...
Source: "ffmpeg\bin\ffprobe.exe"; DestDir: "{app}"; ...

; theme.html
Source: "theme.html"; DestDir: "{app}"; ...
```

---

### שלב ד' — בנה את ה-Installer

1. פתח את Inno Setup Compiler
2. `File` → `Open` → בחר `AudioCraftPro_Setup.iss`
3. לחץ `Build` → `Compile` (או `Ctrl+F9`)
4. הקובץ ייצא ל: `installer_output\AudioCraftPro_v0.4_Setup.exe`

---

### מה מקבל המשתמש הסופי

הקובץ `AudioCraftPro_v0.4_Setup.exe` כולל **הכל**:
- ✅ `AudioCraftPro.exe` + כל קבצי הספריות
- ✅ `ffmpeg.exe` + `ffprobe.exe` (לצד ה-EXE — ללא צורך ב-PATH)
- ✅ `theme.html`
- ✅ קיצור דרך בתפריט התחל (ואופציונלית על שולחן העבודה)
- ✅ הסרת התקנה נוחה מ"הוסף/הסר תוכניות"

> **לא נדרש** Python, לא נדרש pip, לא נדרש FFmpeg בנפרד, לא נדרש PATH.
> המשתמש מריץ `Setup.exe` → לוחץ הבא → סיום.

---

### תיקון שגיאות נפוצות ב-Inno Setup

| שגיאה | פתרון |
|-------|--------|
| `Source file not found: dist\AudioCraftPro\*` | הרץ PyInstaller תחילה |
| `Source file not found: ffmpeg\bin\ffmpeg.exe` | עדכן את הנתיב ל-ffmpeg שלך |
| `Cannot open file: theme.html` | ודא ש-theme.html נמצא לצד ה-.iss |
| `[ISPP] Error` | ודא שמשתמשים ב-Inno Setup 6.x |


<a name="בעיות"></a>
## ❓ שאלות נפוצות ופתרון בעיות

### "pydub לא מותקן"
```
pip install pydub
```

### "FFmpeg לא נמצא"
הרץ `add_ffmpeg_to_path.bat` כ-Administrator, או הגדר ידנית בלשונית **הגדרות**.

### קובץ M4A / AAC לא נטען
M4A דורש FFmpeg. ודא שהוא מותקן ומוגדר.

### התמונה לא מוטמעת
ודא ש-`mutagen` מותקן: `pip install mutagen`
תמיכה: MP3, FLAC, M4A. WAV אינו תומך בתמונות.

### הממשק לא נראה נכון / ערכת עיצוב
ודא ש-`theme.html` נמצא **באותה תיקיה** כמו `audio_craft_pro.py` (או לצד `AudioCraftPro.exe`).

### בגרסת EXE התוכנה לא מוצאת את theme.html
`theme.html` חייב להיות **לצד** ה-EXE — לא בתת-תיקייה.

---

## 📦 פקודות מהירות

```bash
# התקנת ספריות
pip install -r requirements.txt

# הרצת התוכנה
python audio_craft_pro.py

# עדכון ספריות
pip install --upgrade pydub pygame mutagen Pillow
```

---

*AudioCraft Pro v0.4 | Python 3.9+ | Windows 10/11*


# תמונות 
<img width="1098" height="749" alt="משלב קרדיט" src="https://github.com/user-attachments/assets/407fa8e2-6f07-406b-af27-8c2c306b4748" />
