# TagStore

<img src="icon.png" width="150" style="float: right; margin-left: 15px;"> 
<p>TagStore tags the images in a folder on your computer. The index is a `.tagstore.json` file in that folder. The app talks only to `127.0.0.1`. Nothing is uploaded. </p>

## Windows installer

Install the packages in `requirements-dev.txt`, then:

```
powershell -ExecutionPolicy Bypass -File packaging\build.ps1
```

That writes `dist\TagStore\TagStore.exe` and `dist\TagStore-Setup-0.1.0.exe`. The installer step needs [Inno Setup 6](https://jrsoftware.org/isdl.php).

`DESIGN-DOC.md` is the packaging design. `TODOs.md` is the remaining work.

## Run from source

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m tagstore.web --root C:\path\to\images
```

Then open http://127.0.0.1:8000.

`python run_tagstore.py` does the same thing in a desktop window. It asks for the image folder on the first launch and reopens that folder later. Pass `--root` to choose a folder for that run.

