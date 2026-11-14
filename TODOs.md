
# TODOs

Milestone 2 is done, so the next gate is Milestone 3: installer plus a run on a machine that has never seen Python. Everything you just verified was on your dev box, which already has WebView2, the CRT, and .NET. That's the assumption most likely to break.

**1. Clean-machine test before anything else.** Zip `dist\TagStore\` (the whole folder, `_internal` included), drop it into Windows Sandbox or a VM, and rerun your table. No installer needed yet — this isolates "does the bundle work" from "does the installer work". Watch specifically for: WebView2 absent, first-launch SmartScreen, and whether the Recycle Bin path still works without pywin32 (your warn file shows `send2trash.win.modern` unresolved, so you're on the ctypes legacy path — it should hold, but confirm).

**2. Fail loudly when the window can't open.** Right now a windowed build has no console, so `DatabaseLoadError` from a corrupt `.tagstore.json`, a missing WebView2, or a failed bind all exit silently. The only trace is a log the user can't find. And `open_browser_fallback` blocks on `threading.Event().wait()` forever with no way out except Task Manager. A `MessageBoxW`/`tkinter.messagebox` with the exception and the log path, before `return 1`, is a few lines and turns your worst support case into a readable one.

**3. Confirm add-tag by hand — and fix the expectation.** It wasn't confirmed, and it's the one action with an irreversible side effect: `_apply_tag_edit` calls `_append_tags_to_filenames` when `op == "add"` and `override` is false. A hand-typed tag *cannot* stay separate from the filename; `spot` typed into the box renames `red cat.png` to `red cat spot.png` on every copy of that hash. So the assertion is "the file got renamed and the tag survived a rescan", not "a tag independent of the filename". Click a tile first (`addDetailTag` returns early when `selectedHashes` is empty), then click into the input and press Enter. While you're there, decide whether a Ctrl+arrow range of 200 images silently renaming 200 files needs a confirmation.

**4. One realistic library, inside the exe.** Three images tells you nothing about `/api/search`, which builds `result_entries` for every match and returns the full `hashes` list on each page request, or about `save()`, which rewrites the whole indented JSON on every single tag edit. Point it at 10k–50k files and time a search, a page flip, and one tag add. If that's slow, it's the thing users will call broken.

Then the `.iss`: `PrivilegesRequired=lowest`, `{localappdata}\Programs\TagStore`, ship the whole onedir, stamp version/icon on the exe first. Add a second Start Menu entry "TagStore (choose folder)" wired to a `--pick` flag — cheap, and it removes the dead end where the only way to change folder is deleting `config.json`.

**Defer:** code signing, GitHub Actions, macOS/Linux, trimming `opentelemetry`/`pydantic.v1`. Don't exclude `setuptools` — `clr_loader.ffi` → `cffi.api` → `_shimmed_dist_utils` imports it at runtime, so pywebview dies without it.

Also: commit your table as `packaging/TESTS.md` so step 1 is a rerun, not a rewrite.