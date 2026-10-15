# Changelog

## 1.14
- Renamed to "ManicTime Tracker for Thunderbird" (German: "ManicTime-Tracker für Thunderbird") to comply with the Mozilla trademark policy.

## 1.13
- The URL now starts with the account name instead of "thunderbird": `https://<account>/<folder>/`. Characters not allowed in a host name (spaces, `@`, …) in the account name are replaced by `-`.

## 1.12
- Search (virtual), unified and tag folders are used in the URL when the mail is viewed in one: `https://thunderbird/<account>/virtual|unified|tag/<name>/`. Otherwise the real folder is used.

## 1.11
- The mail folder is part of the URL when reading: `https://thunderbird/<account>/<folder>/` (e.g. `…/myAccount/INBOX/`). Composing uses `https://thunderbird/<account>/compose/`.

## 1.10
- The mail account name is part of the URL sent to ManicTime: `https://thunderbird/<account>/read|compose`. Needs the `accountsRead` permission again.

## 1.9
- Added the ManicTime icon.

## 1.8
- Removed the unused `accountsRead` permission.

## 1.7
- Copyright holder set to Jürgen Hörmann.

## 1.6
- New add-on ID: `manictime-tracker@jhit.org`.

## 1.5
- Renamed to "Thunderbird Tracker for ManicTime" (German: "Thunderbird Tracker für ManicTime").

## 1.4
- Licensed under GPL-3.0-or-later; added `LICENSE`.

## 1.3
- Settings page styled like native Thunderbird (light and dark).
- English and German translation.

## 1.2
- Fewer connection attempts to unused ManicTime ports: 42870 every 10 s, 42871–42879 every 60 s.

## 1.1
- Settings page opens in its own tab.

## 1.0
- First version: sends From, To and Subject of the focused Thunderbird window (reading and composing) to the local ManicTime client via its document-tracker WebSocket.
- Option to shorten the subject to a maximum number of characters.
