# ManicTime-Tracker für Thunderbird

[English](README.md)

Meldet **Absender / Empfänger / Betreff** des aktiven Thunderbird-Fensters (Mail lesen oder verfassen) an den lokalen **ManicTime**-Client, sodass sie auf der Dokumente-Zeitleiste erscheinen. Optional kann der Betreff in den Add-on-Einstellungen auf eine maximale Zeichenzahl gekürzt werden. Oberfläche auf Deutsch und Englisch.

## Bedienung
1. Den **ManicTime**-Client auf demselben Rechner installieren und starten. In Thunderbird ist nichts einzurichten.
2. Das Add-on installieren. Es hat keinen Symbolleisten-Knopf und keinen Menüeintrag: Es arbeitet im Hintergrund, solange Thunderbird läuft.
3. Eine Mail auswählen oder öffnen oder eine neue schreiben. Nach wenigen Sekunden zeigt ManicTime sie auf der Zeitleiste **Dokumente** als `From: <Absender>, To: <Empfänger>` an, gruppiert nach Konto und Ordner. Der Betreff erscheint als Fenstertitel auf der Zeitleiste **Anwendungen**.
4. Optionale Einstellungen: *Extras → Add-ons und Themes → ManicTime-Tracker für Thunderbird → ⋯ → Einstellungen*. Dort lässt sich die maximale Betreff-Länge festlegen (0 = keine Begrenzung). Änderungen werden sofort gespeichert.

Erscheint in ManicTime nichts, prüfen, ob der ManicTime-Client läuft; das Add-on verbindet sich automatisch neu.

## Funktionsweise
Das Add-on meldet jede Mail als E-Mail-Dokument an ManicTime, im selben Format wie das ManicTime-Outlook-Plugin: `DocumentType` = `ManicTime/Email`. Es sendet die Nachricht `{ProcessName, Title, DocumentType, DocumentName, DocumentGroup}` an den lokalen Dokument-Tracker-WebSocket von ManicTime, `ws://127.0.0.1:42870/manictime-document/` (Ports 42870–42879). Bis 1.14 nutzte es stattdessen das Format der Browser-Erweiterungen (`{ProcessName, Title, Url, IsPrivate}` mit einer fiktiven Web-URL).

- `Title` ist der Betreff. Er ist der Fenstertitel auf der Anwendungen-Zeitleiste.
- `DocumentName` lautet `From: <Absender>, To: <Empfänger>`. Das ist der Eintrag auf der Dokumente-Zeitleiste.
- `DocumentGroup` ist `<Konto>/<Ordner>`, z. B. `myAccount/INBOX` (Konto = Name des Thunderbird-Mailkontos). Danach werden die Einträge auf der Dokumente-Zeitleiste gruppiert.
  - Beim Verfassen: `<Konto>/compose`.
  - Mail in einem Suchordner, vereinigten Ordner oder Schlagwort-Ordner: `<Konto>/virtual/<Name>`, `<Konto>/unified/<Name>` bzw. `<Konto>/tag/<Name>`.

Wird keine Mail gelesen oder verfasst, werden alle Felder als `null` gesendet.

## Datenschutz
Mail-Daten werden nur an `127.0.0.1` gesendet (ManicTime auf dem eigenen Rechner). Das Add-on hat darüber hinaus keinen Netzwerkzugriff und speichert nur die Einstellung für die Betreff-Länge. Es wird nichts an den Entwickler oder Dritte übertragen.

## Installation
Die signierte `.xpi` in Thunderbird installieren: Add-ons → ⚙ → Add-on aus Datei installieren. Unsignierte Builds brauchen `xpinstall.signatures.required=false` oder *Add-ons debuggen → Temporäres Add-on laden* (`src/manifest.json`).

## Hinweise
- Getestet unter Linux (GNOME/Wayland mit der ManicTime-GNOME-Erweiterung) unter Windows und unter macOS (15.8.3 auf einem Mac mini 2018). Hat der Thunderbird-Prozess einen anderen Namen (Flatpak/Snap), `PROCESS_NAMES` in `src/background.js` anpassen.
- Unabhängig von ManicTime / Finkit entwickelt. Name und Icon von ManicTime werden mit Erlaubnis des ManicTime-Entwicklers verwendet. Die verwendete Socket-Schnittstelle ist nicht dokumentiert und kann sich ändern.

## Lizenz
Copyright (C) 2026 Jürgen Hörmann. Lizenziert unter der **GNU General Public License v3.0 oder später** – siehe `LICENSE`.
