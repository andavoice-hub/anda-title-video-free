Unicode true
RequestExecutionLevel user
Name "安達免費字卡影片"
OutFile "release\安達免費字卡影片-Setup.exe"
InstallDir "$LOCALAPPDATA\Programs\安達免費字卡影片"
ShowInstDetails show
ShowUninstDetails show
SetCompressor lzma

Function .onInit
  CreateDirectory "$TEMP\安達AI\安裝紀錄"
  FileOpen $0 "$TEMP\安達AI\安裝紀錄\免費字卡影片.log" a
  FileWrite $0 "開始安裝：$INSTDIR$\r$\n"
  FileClose $0
FunctionEnd

Section "安裝"
  SetOutPath "$INSTDIR"
  File /r "stage\*.*"
  CreateDirectory "$SMPROGRAMS\安達AI"
  CreateShortcut "$SMPROGRAMS\安達AI\安達免費字卡影片.lnk" "$INSTDIR\AndaTitleVideoFree.exe"
  CreateShortcut "$DESKTOP\安達免費字卡影片.lnk" "$INSTDIR\AndaTitleVideoFree.exe"
  WriteUninstaller "$INSTDIR\解除安裝.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AndaTitleVideoFree" "DisplayName" "安達免費字卡影片"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AndaTitleVideoFree" "UninstallString" '"$INSTDIR\解除安裝.exe"'
  FileOpen $0 "$TEMP\安達AI\安裝紀錄\免費字卡影片.log" a
  FileWrite $0 "安裝完成：$INSTDIR$\r$\n"
  FileClose $0
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\安達免費字卡影片.lnk"
  Delete "$SMPROGRAMS\安達AI\安達免費字卡影片.lnk"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AndaTitleVideoFree"
  RMDir /r "$INSTDIR"
  ; 成品由使用者自行指定位置，不在安裝目錄中。
SectionEnd

Function .onInstFailed
  FileOpen $0 "$TEMP\安達AI\安裝紀錄\免費字卡影片.log" a
  FileWrite $0 "安裝失敗：$INSTDIR；請檢查磁碟空間與安裝位置。$\r$\n"
  FileClose $0
  MessageBox MB_ICONSTOP "安裝失敗。請檢查安裝位置及磁碟空間；紀錄在暫存資料夾的安達AI\安裝紀錄。"
FunctionEnd
