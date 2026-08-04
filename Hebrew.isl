; Hebrew.isl — קובץ שפה עברית ל-Inno Setup 6
; מקם קובץ זה לצד AudioCraftPro_Setup.iss

[LangOptions]
LanguageName=Hebrew
LanguageID=$040D
LanguageCodePage=0
DialogFontName=Tahoma
DialogFontSize=8
WelcomeFontName=Tahoma
WelcomeFontSize=12
CopyrightFontName=Tahoma
CopyrightFontSize=8
RightToLeft=yes

[Messages]
; ── כפתורים ────────────────────────────────────────────────────────────────
ButtonBack=< &חזרה
ButtonNext=ה&בא >
ButtonInstall=&התקן
ButtonOK=אישור
ButtonCancel=ביטול
ButtonYes=&כן
ButtonYesToAll=כן ל&כולם
ButtonNo=&לא
ButtonNoToAll=לא ל&כולם
ButtonFinish=&סיום
ButtonBrowse=עי&ון...
ButtonWizardBrowse=עי&ון...
ButtonNewFolder=&צור תיקיה חדשה

; ── כותרות שלבי האשף ────────────────────────────────────────────────────
WelcomeLabel1=ברוכים הבאים לאשף ההתקנה של [name]
WelcomeLabel2=תוכנית זו תתקין את [name/ver] על המחשב שלך.%n%nמומלץ לסגור את כל היישומים הפתוחים לפני שממשיכים.%n%nלחץ 'הבא' כדי להמשיך.

LicenseLabel=אנא קרא את הסכם הרישיון לפני שתמשיך.
LicenseLabel3=קרא את הסכם הרישיון להלן. עליך לאשר את תנאי ההסכם לפני שתמשיך בהתקנה.
LicenseAccepted=אני &מסכים לתנאי הסכם הרישיון
LicenseNotAccepted=אני &אינו מסכים לתנאי הסכם הרישיון

InfoBeforeLabel=אנא קרא את המידע הבא לפני שתמשיך בהתקנה.
InfoBeforeClickLabel=כשתהיה מוכן להמשיך, לחץ 'הבא'.
InfoAfterLabel=אנא קרא את המידע הבא לפני שתסיים את ההתקנה.
InfoAfterClickLabel=כשתהיה מוכן להמשיך, לחץ 'הבא'.

WinVersionTooLowError=תוכנית זו מחייבת %1 גרסה %2 ומעלה.
WinVersionTooHighError=לא ניתן להתקין תוכנית זו על %1.
AdminPrivilegesRequired=עליך להיות מחובר כמנהל מערכת כדי להתקין תוכנית זו.
PowerUserPrivilegesRequired=עליך להיות מחובר כמנהל מערכת או כמשתמש מורשה כדי להתקין תוכנית זו.
SetupAppRunningError=המתקין זיהה כי %1 פועלת כעת.%n%nאנא סגור את כל המופעים של תוכנית זו, ולאחר מכן לחץ 'אישור' להמשך, או 'ביטול' ליציאה.
UninstallAppRunningError=מסיר ההתקנה זיהה כי %1 פועלת כעת.%n%nאנא סגור את כל המופעים של תוכנית זו, ולאחר מכן לחץ 'אישור' להמשך, או 'ביטול' ליציאה.

; ── בחירת תיקיית יעד ───────────────────────────────────────────────────
SelectDirDesc=לאן יש להתקין את [name]?
SelectDirLabel3=המתקין יתקין את [name] לתיקיה הבאה.
SelectDirBrowseLabel=לחץ 'הבא' כדי להמשיך. אם ברצונך לבחור תיקיה אחרת, לחץ 'עיון'.
DiskSpaceMBLabel=נדרש לפחות [mb] MB של שטח דיסק פנוי.
CannotInstallToNetworkDrive=לא ניתן להתקין לכונן רשת.
CannotInstallToUNCPath=לא ניתן להתקין לנתיב UNC.
InvalidPath=עליך להזין נתיב מלא עם אות כונן; לדוגמה:%n%nC:\APP
InvalidDrive=הכונן או מיקום השיתוף שבחרת אינו קיים או אינו נגיש. אנא בחר אחר.
DiskSpaceWarningInstall=למתקין אין מספיק שטח דיסק להתקנה. ניתן להמשיך למרות זאת, אך עלולות להיות בעיות בזמן ההתקנה.%n%nהאם להמשיך?
DirExistsWarning=התיקיה%n%n%1%n%nקיימת כבר. האם ברצונך להתקין לתיקיה זו בכל זאת?
DirDoesntExistConfirm=התיקיה%n%n%1%n%nאינה קיימת. האם ליצור אותה?

; ── בחירת קבוצת תפריט התחל ─────────────────────────────────────────────
SelectStartMenuFolderDesc=היכן ליצור קיצורי דרך בתפריט התחל?
SelectStartMenuFolderLabel3=המתקין ייצור קיצורי דרך בתיקיית תפריט התחל הבאה.
SelectStartMenuFolderBrowseLabel=לחץ 'הבא' כדי להמשיך. אם ברצונך לבחור תיקיה אחרת, לחץ 'עיון'.
MustEnterGroupName=עליך להזין שם קבוצה.
GroupNameTooLong=שם התיקיה או הנתיב ארוכים מדי.
InvalidGroupName=שם התיקיה אינו חוקי.
BadGroupName=שם הקבוצה אינו יכול לכלול את התווים הבאים:%n%n%1
NoProgramGroupCheck2=&אל תיצור תיקיה בתפריט התחל

; ── בחירת משימות נוספות ─────────────────────────────────────────────────
WizardSelectTasks=בחר משימות נוספות
SelectTasksDesc=אילו משימות נוספות יש לבצע?
SelectTasksLabel2=בחר את המשימות הנוספות שברצונך שהמתקין יבצע בזמן התקנת [name], ולאחר מכן לחץ 'הבא'.

; ── מוכן להתקין ─────────────────────────────────────────────────────────
WizardReady=מוכן להתקין
ReadyLabel1=המתקין מוכן להתקין את [name] על המחשב שלך.
ReadyLabel2a=לחץ 'התקן' כדי להתחיל, או לחץ 'חזרה' כדי לסקור או לשנות הגדרות.
ReadyLabel2b=לחץ 'התקן' כדי להתחיל.
ReadyMemoUserInfo=פרטי משתמש:
ReadyMemoDir=תיקיית יעד:
ReadyMemoType=סוג התקנה:
ReadyMemoComponents=רכיבים שנבחרו:
ReadyMemoGroup=תיקיית תפריט התחל:
ReadyMemoTasks=משימות נוספות:

; ── מתקין ───────────────────────────────────────────────────────────────
WizardInstalling=מתקין
InstallingLabel=אנא המתן בזמן שהמתקין מתקין את [name] על המחשב שלך.

; ── סיום ────────────────────────────────────────────────────────────────
FinishedHeadingLabel=השלמת את אשף ההתקנה של [name]
FinishedLabelNoIcons=ההתקנה של [name] הושלמה בהצלחה.
FinishedLabel=ההתקנה של [name] הושלמה בהצלחה. ניתן להפעיל את התוכנה על ידי לחיצה על הסמל שנוצר.
ClickFinish=לחץ 'סיום' כדי לסיים את ההתקנה.

; ── הודעות מגוונות ──────────────────────────────────────────────────────
SetupAborted=ההתקנה לא הושלמה.%n%nאנא תקן את הבעיה והפעל שוב את המתקין.
AbortRetryIgnoreSelectAction=בחר פעולה
AbortRetryIgnoreRetry=נסה שוב
AbortRetryIgnoreIgnore=&התעלם מהשגיאה והמשך
AbortRetryIgnoreCancel=בטל התקנה

StatusClosingApplications=סוגר יישומים...
StatusCreateDirs=יוצר תיקיות...
StatusExtractFiles=מחלץ קבצים...
StatusCreateIcons=יוצר קיצורי דרך...
StatusCreateIniEntries=יוצר ערכי INI...
StatusCreateRegistryEntries=יוצר ערכי רג'יסטרי...
StatusRegisterFiles=רושם קבצים...
StatusSavingUninstall=שומר מידע להסרת התקנה...
StatusRunProgram=מסיים התקנה...
StatusRestartingApplications=מפעיל מחדש יישומים...
StatusRollback=מבטל שינויים...

ErrorInternal2=שגיאה פנימית: %1
ErrorFunctionFailedNoCode=%1 נכשל
ErrorFunctionFailed=%1 נכשל; קוד %2
ErrorFunctionFailedWithMessage=%1 נכשל; קוד %2.%n%3
ErrorExecutingProgram=לא ניתן להפעיל את הקובץ:%n%1

RegSvr32Failed=RegSvr32 נכשל עם קוד שגיאה %1.
RegServerFailedCommon=לא ניתן לרשום את השרת. וודא שהקובץ נמצא ביעד, שיש לך הרשאות כתיבה, ושה-COM+/MTS מותקן.

FileNotInDir2=הקובץ "%1" לא נמצא ב-"%2". אנא הכנס את הדיסק הנכון, או בחר תיקיה חלופית.
SelectDirectoryForFile=בחר תיקיה עבור "%1"

SetupFileCorrupted=קובצי ההתקנה פגומים. אנא השג עותק חדש של התוכנה.
SetupFileCorruptedOrWrongVer=קובצי ההתקנה פגומים, או שאינם תואמים לגרסה זו של המתקין. אנא תקן את הבעיה או השג עותק חדש.
InvalidParameter=פרמטר שגוי הועבר לשורת הפקודה:%n%n%1
SetupAlreadyRunning=המתקין כבר פועל.

WindowsVersionNotSupported=תוכנית זו אינה תומכת בגרסת Windows שמותקנת על המחשב שלך.
WindowsServicePackRequired=תוכנית זו מחייבת %1 עם Service Pack %2 ומעלה.
NotOnThisPlatform=תוכנית זו לא תפעל על %1.
OnlyOnThisPlatform=תוכנית זו חייבת לפעול על %1.
OnlyOnTheseArchitectures=תוכנית זו ניתנת להתקנה רק על גרסאות Windows שתומכות בארכיטקטורות המעבד הבאות:%n%n%1
WinVersionTooLowError=תוכנית זו מחייבת %1 גרסה %2 ומעלה.
WinVersionTooHighError=לא ניתן להתקין תוכנית זו על %1.
MissingWOW64APIs=גרסת Windows שבה אתה משתמש אינה כוללת פונקציונליות הנדרשת על ידי המתקין לביצוע התקנה 64-ביט.
WinFuncError=שגיאה %1.
UninstallMayNotCompleteLabel1=לפני שתסיר את ההתקנה של %1 מהמחשב, ייתכן שיהיה עליך לסגור כמה יישומים.

; ── הסרת התקנה ──────────────────────────────────────────────────────────
UninstallNotFound=הקובץ "%1" לא קיים. לא ניתן להסיר את ההתקנה.
UninstallOpenError=לא ניתן לפתוח את הקובץ "%1". לא ניתן להסיר את ההתקנה.
UninstallUnsupportedVer=קובץ יומן ההסרה "%1" אינו מוכר על ידי גרסה זו של מסיר ההתקנה.
UninstallUnknownEntry=נתקלנו בערך לא מוכר "%1" ביומן ההסרה
ConfirmUninstall=האם אתה בטוח שברצונך להסיר לחלוטין את %1 וכל הרכיבים שלו?
UninstallOnlyOnWin64=ניתן להסיר את ההתקנה של תוכנית זו רק על Windows 64-ביט.
OnlyAdminCanUninstall=ניתן להסיר את ההתקנה של תוכנית זו רק על ידי משתמש עם הרשאות מנהל מערכת.
UninstallStatusLabel=אנא המתן בזמן ש-%1 מוסרת מהמחשב שלך.
UninstalledAll=%1 הוסרה בהצלחה מהמחשב שלך.
UninstalledMost=הסרת ההתקנה של %1 הושלמה.%n%nחלק מהפריטים לא ניתנו להסרה. ניתן להסירם ידנית.
UninstalledAndNeedsRestart=כדי להשלים את הסרת ההתקנה של %1, יש להפעיל מחדש את המחשב.%n%nהאם להפעיל מחדש עכשיו?
UninstallDataCorrupted=הקובץ "%1" פגום. לא ניתן להסיר את ההתקנה.

; ── הפעלה מחדש ──────────────────────────────────────────────────────────
FinishedRestartLabel=כדי להשלים את ההתקנה של [name], יש להפעיל מחדש את המחשב.%n%nהאם להפעיל מחדש עכשיו?
ShowReadmeCheck=כן, ברצוני לצפות בקובץ README
YesRadio=&כן, הפעל מחדש את המחשב עכשיו
NoRadio=&לא, אפעיל מחדש את המחשב מאוחר יותר
ErrorCreatingShortcut=לא ניתן ליצור קיצור דרך: %1
ErrorCreatingIcon=לא ניתן ליצור סמל: %1
ErrorChangingAttr=לא ניתן לשנות את תכונות הקובץ: %1
ErrorCreatingConfig=לא ניתן ליצור קובץ תצורה: %1
ErrorReadingSetupFile=אירעה שגיאה בעת קריאת קובץ ההתקנה.
ErrorLineIsEmpty=שורה %1 בקובץ ההתקנה ריקה.
ErrorFileMissing=קובץ ההתקנה חסר: %1
ErrorDataEntry=שגיאה בנתוני ההתקנה: %1
ErrorUnsupportedSetup=הגדרה לא נתמכת ב-%1.
ErrorRestartReplace=RestartReplace נכשל: %1
ErrorRenamingTemp=אירעה שגיאה בעת שינוי שם קובץ זמני:%n%1
ErrorRegisterServer=לא ניתן לרשום את ה-DLL/OCX: %1
ErrorRegSvr32Failed=RegSvr32 נכשל עם קוד שגיאה %1
ErrorRegisterTypeLib=לא ניתן לרשום את ספריית הטיפוסים: %1

; ── שונות ────────────────────────────────────────────────────────────────
ExitSetupTitle=יציאה מהמתקין
ExitSetupMessage=ההתקנה לא הושלמה. אם תצא עכשיו, [name] לא יותקן.%n%nתוכל להפעיל את המתקין שוב כדי להשלים את ההתקנה.%n%nהאם לצאת?
AboutSetupMenuItem=&אודות המתקין...
AboutSetupTitle=אודות המתקין
AboutSetupMessage=%1 גרסה %2%n%nדף הבית של %1:%n%3
AboutSetupNote=
TranslatorNote=
