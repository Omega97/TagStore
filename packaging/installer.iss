; Per-user TagStore installer. No admin rights. Does not remove image-folder
; .tagstore.json files or %APPDATA%\TagStore on uninstall.

#define AppName "TagStore"
#define AppVersion "0.1.0"
#define AppExeName "TagStore.exe"

[Setup]
AppId={{8F3C2A1E-6B47-4D19-9C5A-2E7B0D4F1A88}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppName}
DefaultDirName={localappdata}\Programs\TagStore
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
AppMutex=TagStore-8F3C2A1E-6B47-4D19-9C5A-2E7B0D4F1A88
CloseApplications=yes
SetupIconFile=tagstore.ico
OutputDir=..\dist
OutputBaseFilename=TagStore-Setup-{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Files]
Source: "..\dist\TagStore\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
