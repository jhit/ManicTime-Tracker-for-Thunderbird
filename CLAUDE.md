# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Thunderbird MailExtension (Manifest V2, Thunderbird ≥ 115) that reports the focused mail (reading or composing) to the local ManicTime client as an email document. No npm/bundler, no runtime dependencies, no tests — the plain JS/HTML files in `src/` are the add-on; `src/` becomes the root of the `.xpi`. Building needs only `bash`, `zip` and `python3`.

## Commands

- Build the `.xpi`: `./build.sh` → `dist/manictime-tracker-<version>.xpi` (version read from `src/manifest.json`). It first regenerates `doc/README.html`, then zips the files listed in `build.sh` from inside `src/` and adds the root `LICENSE`. New files in `src/` must be added to that `zip` list, or they are not shipped.
- Regenerate the AMO description only: `python3 doc/readme2html.py`
- Lint (optional, `WEBEXT-LINTER-CACHE/` is gitignored): `npx web-ext lint --source-dir src`
- Manual test: Thunderbird → Debug Add-ons → Load Temporary Add-on → select `src/manifest.json`.
- Test steps (for users and AMO reviewers) are in `test/TESTING.md`; keep them in sync with behavior changes.
- Test without ManicTime: `python3 test/manictime-mock.py [--port 4287x] [--redact]` (stdlib only) imitates ManicTime's socket and prints every message the add-on sends. If ManicTime already holds 42870, use 42871–42879; the add-on retries those only every 60 s. Use `--redact` whenever the output ends up in a conversation or log — the messages contain real subjects and addresses.

## Architecture

`src/background.js` does everything:
- **Polling, not events:** every `POLL_MS` (2 s) `currentInfo()` inspects the last-focused window — compose window via `compose.getComposeDetails`, otherwise `messageDisplay.getDisplayedMessage` for 3-pane/message tabs. A message is sent when the info changes or every `HEARTBEAT_MS` (5 s).
- **Protocol:** JSON `{ProcessName, Title, DocumentType: "ManicTime/Email", DocumentName, DocumentGroup}` (same format as ManicTime's Outlook plugin) sent over WebSocket to `ws://127.0.0.1:42870–42879/manictime-document/`. One message per entry in `PROCESS_NAMES`, because the process name ManicTime sees differs by platform. When nothing is focused/displayed, all fields except `ProcessName` are `null`. This interface is undocumented by ManicTime.
  - `Title` = subject (optionally shortened to `maxSubject` chars), `DocumentName` = `From: …, To: …`, `DocumentGroup` = `<account>/<folder>` (`compose`, or `virtual|unified|tag/<name>` for special folders via `mailTabs.get`).
- **Connections:** sockets are kept in a map per port; port 42870 is retried every 10 s, the fallback ports every 60 s. The last messages are replayed on `onopen`.
- **Settings:** only `maxSubject` in `storage.local`, edited by `src/options.html/js`; changing it resets `lastKey` to force a resend.

UI strings live in `src/_locales/{en,de}/messages.json` (must stay next to `manifest.json`) and are applied via `data-i18n` attributes in `options.html`.

## Conventions

- `doc/README.html` is the template for the add-on description on addons.thunderbird.net, generated from `README.md` by `python3 doc/readme2html.py` (also run by `build.sh`). Regenerate it after every change to `README.md`. AMO allows only `<a href title> <abbr title> <acronym title> <b> <blockquote> <code> <em> <i> <li> <ol> <strong> <ul>` — no headings, no `<p>`/`<br>` (newlines become breaks), so the converter drops the H1 (AMO shows the name), turns other headings into `<b>`, writes each list on one line and rewrites relative links to `https://github.com/jhit/ManicTime-Tracker-for-Thunderbird/blob/main/…`. It supports only the Markdown the README uses (headings, paragraphs, `-`/`1.` lists with 2-space nesting, `>` quotes, code, bold, italic, links); extend `doc/readme2html.py` before using other syntax, and check the output contains only allowed tags.
- Releases: bump `version` in `src/manifest.json` and add a `CHANGELOG.md` entry; behavior/format changes are documented in both `README.md` and `README.de.md` (keep them in sync).
- What is sent and where is stated in three places that must stay in sync with `src/background.js`: the README Privacy section, `doc/PRIVACY.md`/`doc/PRIVACY.de.md` (text for the ATN privacy policy field), and the `optionsData` string on the options page.
- The ManicTime name and icon are used with permission of the ManicTime developer.
- New Thunderbird APIs need the matching permission in `manifest.json`; the privacy promise in the README (data only goes to `127.0.0.1`, only the subject-length setting is stored) must stay true.
- Source files carry the GPL-3.0-or-later SPDX header.
