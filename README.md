# ManicTime Tracker for Thunderbird

[Deutsch](README.de.md)

Reports **From / To / Subject** of the focused Thunderbird window (reading or composing a mail) to the local **ManicTime** client, so it shows up on the Documents timeline. Optional: shorten the subject to a maximum number of characters (add-on settings). English and German UI.

## Usage
1. Install and run the **ManicTime** client on the same computer. Thunderbird itself needs no setup.
2. Install the add-on. It has no toolbar button and no menu entry: it works in the background as long as Thunderbird is running.
3. Select or open a mail, or write a new one. Within a few seconds ManicTime shows it on the **Documents** timeline as `From: <sender>, To: <receiver>`, grouped by account and folder. The subject appears as the window title on the **Applications** timeline.
4. Optional settings: *Tools → Add-ons and Themes → ManicTime Tracker for Thunderbird → ⋯ → Options*. There you can set the maximum subject length (0 = no limit). Changes are saved immediately.

If nothing shows up in ManicTime, make sure the ManicTime client is running; the add-on reconnects automatically.

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
Install the signed `.xpi` via Thunderbird → Add-ons → ⚙ → Install Add-on From File. Unsigned builds need `xpinstall.signatures.required=false` or *Debug Add-ons → Load Temporary Add-on* (`src/manifest.json`).

## Notes
- Tested on Linux (GNOME/Wayland with the ManicTime GNOME extension) on Windows and on macOS (15.8.3 on a Mac mini 2018). If your Thunderbird process has another name (Flatpak/Snap), edit `PROCESS_NAMES` in `src/background.js`.
- Developed independently of ManicTime / Finkit. The ManicTime name and icon are used with permission of the ManicTime developer. The socket interface used is undocumented and may change.

## License
Copyright (C) 2026 Jürgen Hörmann. Licensed under the **GNU General Public License v3.0 or later** – see `LICENSE`.
