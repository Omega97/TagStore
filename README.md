# TagStore

<img src="icon.png" width="150" style="float: right; margin-left: 15px;">

[Download here](https://github.com/Omega97/TagStore/releases/latest)
TagStore tags the pictures in a folder on your computer. The tags come from the words in each file's name. Everything stays on your computer — the app talks only to `127.0.0.1`, and nothing is uploaded.

## Install

1. Download `TagStore-Setup-0.1.0.exe` from the [releases page](https://github.com/Omega97/TagStore/releases). You only need that one file.
2. Open it. If Windows shows "Windows protected your PC", click **More info** → **Run anyway**. That warning appears because TagStore is not code-signed yet.
3. Follow the installer. It does not ask for an administrator password.
4. Open **TagStore** from the desktop icon or Start menu. Choose the folder with your pictures, then click **Scan database** in the app.

To remove it: **Settings** → **Apps** → **TagStore** → **Uninstall**. Your pictures and their tags stay where they are.

See `HOW-TO-INSTALL.md` for a longer step-by-step guide.

## Build from source (developers)

Install the packages in `requirements-dev.txt`, then:

```
powershell -ExecutionPolicy Bypass -File packaging\build.ps1
```

That writes `dist\TagStore\TagStore.exe` and `dist\TagStore-Setup-0.1.0.exe`. The installer step needs [Inno Setup 6](https://jrsoftware.org/isdl.php).

To run without building:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m tagstore.web --root C:\path\to\images
```

Then open http://127.0.0.1:8000. `python run_tagstore.py` runs the same app in a desktop window.

`DESIGN-DOC.md` is the packaging design. `TODOs.md` is the remaining work.
