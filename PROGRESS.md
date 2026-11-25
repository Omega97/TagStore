# Progress

Checked items are in the repo and have been exercised on this PC. Open items are the remaining milestones and the checks still to run.

## Achievements

- [x] Tag images in a local folder. The index is `.tagstore.json` in that folder, with `synonyms.txt` and `banned.txt` beside it. The server binds to `127.0.0.1` only.
- [x] Web UI to scan, search, rename, reveal a file in Explorer, and delete it to the Recycle Bin.
- [x] Desktop launcher (`run_tagstore.py`): folder picker, last folder saved in `%APPDATA%\TagStore\config.json`, free local port, native window. Closing the window ends the process.
- [x] Windowed `TagStore.exe` (PyInstaller `--onedir`) and per-user installer `TagStore-Setup-0.1.0.exe` (no administrator prompt, leaves image data and `%APPDATA%\TagStore` on uninstall).
- [x] Interactive pass of `TagStore.exe` on this PC: folder dialog, native window, scan, rename, reveal, delete, and close.
- [x] Startup failures show a dialog with the log path, then exit. A corrupt database is reported before the server thread starts.
- [x] Installer can see a running copy (`AppMutex`, `CloseApplications`). The exe has version 0.1.0 and an icon (a multi-size `.ico` generated from `icon.png`).
- [x] `packaging/build.ps1` exits with code 1 when Inno Setup (ISCC) is not found, instead of falling through and crashing.
- [x] MIT `LICENSE`. Design notes record the native window and the `%APPDATA%\TagStore` config.
- [x] First git commit on `master`.
- [x] Timed a 10,000-file library: first scan 121.6 s, search 0.08 s, one tag edit 0.06 s. The tag edit renamed the file. Search and the full JSON rewrite were left as they are.

## Milestones and checks still to run

- [ ] Install `dist\TagStore-Setup-0.1.0.exe` on a Windows machine that does not have Python or this repo. This PC is Windows 10 Home, so Windows Sandbox is not available. Checklist is in `packaging/TESTS.md`.
- [ ] On that install: cancel the folder dialog, then choose a throwaway folder, scan three images, rename, reveal, delete to the Recycle Bin, and close the window so the process and the port are gone.
- [ ] Add one tag from the window. The file should be renamed to include that tag, and the tag should still be there after a rescan.
- [ ] Uninstall from Settings. Program files and shortcuts go away. `.tagstore.json` and `%APPDATA%\TagStore` stay.
- [ ] Run the installer again while TagStore is open. It should close the running app or wait, then leave a working `TagStore.exe`.
- [ ] Publish the first release (tag and a downloadable setup). No remote and no release yet.
- [ ] Code signing, so SmartScreen is not the first thing a new user sees.
- [ ] Build the installer with GitHub Actions on a Windows runner.
- [ ] Trim what the package ships (the onedir build is about 41 MB).
- [ ] Let the user pick a different image folder without hunting down `config.json`.
- [ ] Decide whether `synonyms.txt` and `banned.txt` should move to `%APPDATA%\TagStore`.
- [ ] See whether a real photo library of tens of thousands of files needs a faster first scan. The 10k run above used tiny fake files.
