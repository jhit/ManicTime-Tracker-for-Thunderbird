# Thunderbird Tracker für ManicTime

[English](README.md)

Meldet **Absender / Empfänger / Betreff** des aktiven Thunderbird-Fensters (Mail lesen oder verfassen) an den lokalen **ManicTime**-Client, sodass sie auf der Dokumente-Zeitleiste erscheinen. Optional kann der Betreff in den Add-on-Einstellungen auf eine maximale Zeichenzahl gekürzt werden. Oberfläche auf Deutsch und Englisch.

## Funktionsweise
Das Add-on nutzt denselben Kanal wie die Chrome-/Firefox-Erweiterungen von ManicTime: WebSocket `ws://127.0.0.1:42870/manictime-document/` (Ports 42870–42879), Nachricht `{ProcessName, Title, Url, IsPrivate}`. Der `Title` lautet `From: …, To: …, Subject: …`; die `Url` lautet `https://<Konto>/<Ordner>/` beim Lesen (z. B. `…/myAccount/INBOX/`) (bzw. `…/<Konto>/virtual|unified|tag/<Name>/` bei Suchordnern, vereinigten Ordnern und Schlagwort-Ordnern) bzw. `https://<Konto>/compose/` beim Verfassen (Konto = Name des Thunderbird-Mailkontos).

## Datenschutz
Mail-Daten werden nur an `127.0.0.1` gesendet (ManicTime auf dem eigenen Rechner). Das Add-on hat darüber hinaus keinen Netzwerkzugriff und speichert nur die Einstellung für die Betreff-Länge. Es wird nichts an den Entwickler oder Dritte übertragen.

## Installation
Die signierte `.xpi` in Thunderbird installieren: Add-ons → ⚙ → Add-on aus Datei installieren. Unsignierte Builds brauchen `xpinstall.signatures.required=false` oder *Add-ons debuggen → Temporäres Add-on laden* (`extension/manifest.json`).

## Hinweise
- Getestet unter Linux (GNOME/Wayland mit der ManicTime-GNOME-Erweiterung) und unter Windows. Nicht getestet unter macOS. Hat der Thunderbird-Prozess einen anderen Namen (Flatpak/Snap), `PROCESS_NAMES` in `extension/background.js` anpassen.
- Nicht mit ManicTime / Finkit verbunden oder von ihnen unterstützt. Die verwendete Socket-Schnittstelle ist nicht dokumentiert und kann sich ändern.

## Lizenz
Copyright (C) 2026 Jürgen Hörmann. Lizenziert unter der **GNU General Public License v3.0 oder später** – siehe `LICENSE`.
