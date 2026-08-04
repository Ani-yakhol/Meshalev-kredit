; ============================================================
;  AudioCraft Pro v0.4 — Inno Setup Script
;  ממשק התקנה בעברית מלאה
;  דורש: Inno Setup 6.x   https://jrsoftware.org/isinfo.php
; ============================================================

#define AppName      "AudioCraft Pro"
#define AppVersion   "0.7"
#define AppPublisher "AudioCraft"
#define AppExeName   "AudioCraftPro.exe"
#define AppURL       ""

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
OutputDir=.\installer_output
OutputBaseFilename=AudioCraftPro_v{#AppVersion}_Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
DisableWelcomePage=no
; Require Windows 10 or later
MinVersion=10.0

; Request admin rights (needed to write to Program Files)
PrivilegesRequired=admin

; Icon (uncomment and set path if you have an icon file)
; SetupIconFile=icon.ico
; UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
; Hebrew.isl — קובץ שפה עברית מלאה (חייב להיות באותה תיקיה כמו ה-.iss)
Name: "hebrew"; MessagesFile: "Hebrew.isl"

[CustomMessages]
hebrew.CreateDesktopIcon=צור &קיצור דרך על שולחן העבודה
hebrew.LaunchAfterInstall=הפעל את {#AppName} לאחר סיום ההתקנה

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "קיצורי דרך:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "צור קיצור דרך ב&שורת המשימות"; GroupDescription: "קיצורי דרך:"; Flags: unchecked; OnlyBelowVersion: 6.1

[Dirs]
; Create the ffmpeg subfolder inside the install dir
Name: "{app}\ffmpeg"

[Files]
; ── Main application ──────────────────────────────────────────────────────
; Replace the source paths below with the actual paths on your machine.
; All paths are relative to the location of this .iss file unless absolute.

; PyInstaller --onedir output (recommended)
; Copy the entire dist\AudioCraftPro\ folder contents here:
Source: "dist\AudioCraftPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs


; ── FFmpeg binaries ───────────────────────────────────────────────────────
; Download ffmpeg-release-essentials.zip from https://www.gyan.dev/ffmpeg/builds/
; Extract and point to the bin folder:
Source: "ffmpeg\bin\ffmpeg.exe";  DestDir: "{app}"; Flags: ignoreversion
Source: "ffmpeg\bin\ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion

; ── Extra files ───────────────────────────────────────────────────────────
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
; Start Menu shortcut
Name: "{group}\{#AppName}";            Filename: "{app}\{#AppExeName}";    WorkingDir: "{app}"
Name: "{group}\הסר התקנה";             Filename: "{uninstallexe}"
; Desktop shortcut (only if task selected)
Name: "{autodesktop}\{#AppName}";      Filename: "{app}\{#AppExeName}";    WorkingDir: "{app}"; Tasks: desktopicon
; Quick Launch (Windows XP/Vista)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon

[Run]
; Offer to launch the app after installation
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchAfterInstall}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any generated temp files
Type: filesandordirs; Name: "{app}\__pycache__"
Type: filesandordirs; Name: "{app}\_internal"

; ── Registry: Add app to "Add/Remove Programs" with Hebrew display name ──
[Registry]
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#AppName}"; \
    ValueType: string; ValueName: "DisplayName"; ValueData: "{#AppName} {#AppVersion}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#AppName}"; \
    ValueType: string; ValueName: "Publisher"; ValueData: "{#AppPublisher}"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#AppName}"; \
    ValueType: string; ValueName: "DisplayVersion"; ValueData: "{#AppVersion}"

; ── Code section: show a Hebrew info page during install ─────────────────

