Checked the repo (default branch is `master`, one commit, Nov 14). Here's the honest position.

## Status against your own milestones

| Milestone | State | Evidence |
|---|---|---|
| 1 — launcher from source | Done | `run_tagstore.py`, verified by your checklist |
| 2 — `TagStore.exe` on your machine | Done | your table, all six rows pass |
| 3 — installer, proven on clean Windows | **Written, not proven** | `packaging/{build.ps1, installer.iss, tagstore.spec}` exist; no test record |
| 4 — first public release | Not started | 0 releases, 0 tags |

So the *code* for 0.1.0 is essentially finished. `installer.iss` already has the things people get wrong: `PrivilegesRequired=lowest`, `{localappdata}\Programs\TagStore`, `recursesubdirs` on the whole onedir, a fixed `AppId`, and an uninstaller that leaves `.tagstore.json` and `%APPDATA%\TagStore` alone. What's left is not features — it's proof and about 50 lines of hardening.

**Next milestone: the Milestone 3 acceptance test, not more code.** Build the setup, install it in Windows Sandbox, rerun your six-row table plus uninstall. That single run is the gate between "works on Omar's PC" and "installable by a stranger".

## Release gate, in order

1. **Clean install → checklist → uninstall.** Also install twice: `installer.iss` has no `CloseApplications`/`AppMutex`, so upgrading with TagStore open will hit a locked `TagStore.exe`. You'll meet this the moment you ship 0.1.1.
2. **Loud failure.** Still the biggest support risk: windowed build, no console, `DatabaseLoadError` exits silently, and `open_browser_fallback` waits forever. One `MessageBoxW` with the exception + log path.
3. **Add-tag by hand.** Unconfirmed, and it renames files (`_append_tags_to_filenames`). Assert the rename, not an independent tag.
4. **One 10k–50k file library.** `/api/search` builds every entry and returns all hashes per request; `save()` rewrites the full indented JSON per tag edit.
5. **Cosmetics that aren't cosmetic.** No `icon=`/`version=` in the spec and no `SetupIconFile` — an unversioned, iconless exe is worse for SmartScreen and AV heuristics. And the repo has no LICENSE, which for a public repo shipping bundled third-party binaries is worth fixing before the release, not after.

## Two small things I noticed reading the scripts

- `build.ps1`: the "ISCC not found" branch calls `Write-Error` but doesn't `exit`, then falls through to `& $iscc` with `$iscc` null. Add `exit 1` — you'll hit this on any machine without Inno Setup.
- `DESIGN-DOC.md` §4 still lists the window variant and config location as *open* decisions, and §2 mentions a `cli.py` that isn't in the repo. Now that this is the public front door, record what you actually chose (variant B, `%APPDATA%`).

**Still defer:** signing, GitHub Actions, dependency trimming. Add `packaging/TESTS.md` with your table so step 1 is a rerun.

Rough estimate: one afternoon of verification plus the hardening above, and 0.1.0 is publishable.