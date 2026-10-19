# 第三方元件與授權

查證日期：2026-10-18。

| 元件 | 本候選使用方式 | 授權與來源 |
| --- | --- | --- |
| FFmpeg n8.1.3-18-g46d899d7a0-20261017 | BtbN 的 `win64-lgpl-shared` 建置，與安達程式以獨立執行檔通訊；安裝包內附 `ffmpeg.exe`、同包的 `ffprobe.exe`／`ffplay.exe` 與 DLL，沒有重新授權給 PolyForm | LGPL v3；[建置來源](https://github.com/BtbN/FFmpeg-Builds)、[FFmpeg 授權說明](https://ffmpeg.org/legal.html)、[對應原始碼](https://github.com/FFmpeg/FFmpeg/commit/46d899d7a0)。下載包 SHA-256：`3057CDE77A053756D36E10A86D85E2B9A312DA8A989D801F9C5CBB1C06EFF16F`。安裝包內含其 `LICENSE.txt`。建置參數可用 `ffmpeg -version` 查閱。 |
| Pillow | Python 程式的圖片繪製函式庫 | [HPND 類型授權](https://pillow.readthedocs.io/en/stable/about.html#license)；實際封裝版本請見建置紀錄。 |
| Python | PyInstaller 封裝的執行環境 | [Python Software Foundation License](https://docs.python.org/3/license.html)。 |
| PyInstaller | Windows 執行檔封裝器 | [GPL 與 bootloader 例外](https://pyinstaller.org/en/stable/license.html)。 |
| 微軟正黑體／微軟雅黑／新細明體 | 在使用者 Windows 上讀取既有字型，不複製字型檔到安裝包 | 依 Windows 及字型既有授權使用；安裝包不散布字型。 |

此處選用 LGPL shared 建置，避免把本機既有的 GPL FFmpeg full build 封入非商用套件。發行前仍應由授權審查人確認實際打包二進位、附帶聲明及來源提供方式。
