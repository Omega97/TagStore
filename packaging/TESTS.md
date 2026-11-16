# TagStore installer checks

Run these on a Windows install that does not have this repo or a Python environment. Windows Sandbox is the intended machine. Use a throwaway folder of three small images, for example `red cat.png`, `blue cat.png`, and `red dog.png`.

The build under test is `dist\TagStore-Setup-0.1.0.exe`, produced by `packaging\build.ps1`.

## Install

The setup finishes without an administrator prompt. Start menu and, if chosen, the desktop shortcut point at `{localappdata}\Programs\TagStore\TagStore.exe`.

## Application

1. **Launch.** The process name is `TagStore`. The log line `starting TagStore` appears only after a folder is chosen.
2. **Folder dialog.** Cancel once: the process exits and does not write `%APPDATA%\TagStore\config.json`. Choose the throwaway folder: `last_root` is that folder, and the server binds `127.0.0.1` on a free port.
3. **Native window.** The window shows the scan control. The log does not contain `native window failed`.
4. **Scan and tags.** Scan from the window. All three files appear. Tags inferred from the file names are visible.
5. **Rename, reveal, delete.** Rename leaves the new name on disk and removes the old one. Reveal opens Explorer on that file. Delete asks for confirmation, removes the file from the folder, and puts it in the Recycle Bin. The other files remain.
6. **Close.** The window close button ends the `TagStore` process and nothing keeps listening on its port.
7. **Add a tag by hand.** Adding a tag renames the file so the new name contains that tag. After a rescan the tag is still present. A tag stored separately from the filename is not the expected result.

## Uninstall

Uninstall from Settings. Program files, the Start menu entry, and the desktop shortcut are gone. `.tagstore.json` in the image folder and `%APPDATA%\TagStore` remain.

## Upgrade while running

Install, launch TagStore, and run the installer again. The installer closes the running app or refuses to continue while it is open, then leaves a working `TagStore.exe`.

## Large library

On a development machine, time one folder of about 10,000 small files: one scan, one `/api/search`, and one tag edit that rewrites `.tagstore.json`. Record the numbers below. Do not change the search or save implementation for this check unless the run fails outright.

## Results

Recorded 2026-11-15. The build is `dist\TagStore-Setup-0.1.0.exe` (20,294,015 bytes) from `packaging\build.ps1`. `TagStore.exe` reports FileVersion 0.1.0.0, ProductVersion 0.1.0, ProductName TagStore.

### Clean install

Not run. This PC is Windows 10 Home, and `WindowsSandbox.exe` is not present. Windows Sandbox cannot be turned on for that edition. The check needs another machine or a virtual machine.

### Large library

Run on this PC with the source server (`python` / uvicorn, same `create_app` the exe uses), then the folder was deleted. 10,000 unique non-image `.png` files:

| Step | Time | Evidence |
|---|---|---|
| First scan | 121.56 s | summary `assets=10000`, `hashed=10000`, `errors=[]` |
| `GET /api/search?page_size=28` | 0.08 s | `total=10000`, 28 page rows, 10,000 hashes in the response |
| Add tag `bench` on one file | 0.06 s | file renamed to `f00000 bench.png`; `.tagstore.json` is 4,510,217 bytes |

Search and the full-file rewrite are fine at this size. The first scan is the slow step. No code change.
