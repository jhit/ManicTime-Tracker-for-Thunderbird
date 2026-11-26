# ManicTime Tracker for Thunderbird

[Deutsch](README.de.md)

Reports **From / To / Subject** of the focused Thunderbird window (reading or composing a mail) to the local **ManicTime** client, so it shows up on the Documents timeline. Optional: shorten the subject to a maximum number of characters (add-on settings). English and German UI.

## How it works
The add-on reports each mail to ManicTime as an email document, in the same format as the ManicTime Outlook plugin: `DocumentType` = `ManicTime/Email`. It sends the message `{ProcessName, Title, DocumentType, DocumentName, DocumentGroup}` to ManicTime's local document-tracker WebSocket `ws://127.0.0.1:42870/manictime-document/` (ports 42870–42879). Up to 1.14 it used the browser-extension format instead (`{ProcessName, Title, Url, IsPrivate}` with a fake web URL).

- `Title` is the subject. It is the window title on the Applications timeline.
- `DocumentName` is `From: <sender>, To: <receiver>`. It is the entry on the Documents timeline.
- `DocumentGroup` is `<account>/<folder>`, e.g. `myAccount/INBOX` (account = name of the Thunderbird mail account). It groups the entries on the Documents timeline.
  - Composing: `<account>/compose`.
  - Mail viewed in a search, unified or tag folder: `<account>/virtual/<name>`, `<account>/unified/<name>` or `<account>/tag/<name>`.

If no mail is being read or composed, all fields are sent as `null`.

## Privacy
Mail data is sent only to `127.0.0.1` (ManicTime on your own machine). The add-on has no network access beyond that and stores only the subject-length setting. Nothing is sent to the developer or any third party.

## Install
Install the signed `.xpi` via Thunderbird → Add-ons → ⚙ → Install Add-on From File. Unsigned builds need `xpinstall.signatures.required=false` or *Debug Add-ons → Load Temporary Add-on* (`extension/manifest.json`).

## Notes
- Tested on Linux (GNOME/Wayland with the ManicTime GNOME extension) on Windows and on macOS (15.8.3 on a Mac mini 2018). If your Thunderbird process has another name (Flatpak/Snap), edit `PROCESS_NAMES` in `extension/background.js`.
- Not affiliated with or endorsed by ManicTime / Finkit. The socket interface used is undocumented and may change.

## License
Copyright (C) 2026 Jürgen Hörmann. Licensed under the **GNU General Public License v3.0 or later** – see `LICENSE`.
