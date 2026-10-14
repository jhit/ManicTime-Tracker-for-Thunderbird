# Thunderbird Tracker for ManicTime

[Deutsch](README.de.md)

Reports **From / To / Subject** of the focused Thunderbird window (reading or composing a mail) to the local **ManicTime** client, so it shows up on the Documents timeline. Optional: shorten the subject to a maximum number of characters (add-on settings). English and German UI.

## How it works
Same channel as ManicTime's own Chrome/Firefox extensions: WebSocket `ws://127.0.0.1:42870/manictime-document/` (ports 42870–42879), message `{ProcessName, Title, Url, IsPrivate}`. The `Title` is `From: …, To: …, Subject: …`; the `Url` is `https://<account>/<folder>/` when reading (e.g. `…/myAccount/INBOX/`) (or `…/<account>/virtual|unified|tag/<name>/` for search, unified and tag folders) or `https://<account>/compose/` when composing (account = name of the Thunderbird mail account).

## Privacy
Mail data is sent only to `127.0.0.1` (ManicTime on your own machine). The add-on has no network access beyond that and stores only the subject-length setting. Nothing is sent to the developer or any third party.

## Install
Install the signed `.xpi` via Thunderbird → Add-ons → ⚙ → Install Add-on From File. Unsigned builds need `xpinstall.signatures.required=false` or *Debug Add-ons → Load Temporary Add-on* (`extension/manifest.json`).

## Notes
- Tested on Linux (GNOME/Wayland with the ManicTime GNOME extension) and on Windows. Not tested on macOS. If your Thunderbird process has another name (Flatpak/Snap), edit `PROCESS_NAMES` in `extension/background.js`.
- Not affiliated with or endorsed by ManicTime / Finkit. The socket interface used is undocumented and may change.

## License
Copyright (C) 2026 Jürgen Hörmann. Licensed under the **GNU General Public License v3.0 or later** – see `LICENSE`.
