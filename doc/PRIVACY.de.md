Datenschutzerklärung – ManicTime-Tracker für Thunderbird

Dieser Text ist dafür gedacht, unverändert in das Feld für die Datenschutzerklärung auf addons.thunderbird.net eingefügt zu werden. Englische Fassung: PRIVACY.md.

---

ManicTime-Tracker für Thunderbird meldet die Mail, an der Sie in Thunderbird arbeiten, an den Zeiterfassungs-Client ManicTime auf Ihrem eigenen Rechner. Diese Erklärung beschreibt, was das Add-on mit Ihren Daten macht.

Welche Daten gesendet werden
Solange ein Thunderbird-Fenster aktiv ist und Sie eine Mail lesen oder verfassen, sendet das Add-on folgende Daten zu dieser Mail:
- Absender (From)
- Empfänger (To)
- Betreff (gekürzt, wenn Sie in den Add-on-Einstellungen eine maximale Länge festgelegt haben)
- Name des Thunderbird-Mailkontos
- Ordner, in dem die Mail angezeigt wird (bzw. „compose“ beim Verfassen)
Außerdem sendet es den festen Programmnamen „thunderbird“, damit ManicTime die Daten Thunderbird zuordnen kann. Die Daten werden gesendet, wenn sie sich ändern, und alle 5 Sekunden. Wird keine Mail gelesen oder verfasst, werden leere Werte gesendet. Text und Anhänge einer Mail liest und sendet das Add-on nie.

Wohin die Daten gehen
Die Daten werden nur an 127.0.0.1, Ports 42870–42879, gesendet. Das ist die lokale WebSocket-Schnittstelle des ManicTime-Clients auf demselben Rechner. Die Daten verlassen Ihren Rechner nicht, und das Add-on baut keine anderen Netzwerkverbindungen auf. Es wird nichts an den Entwickler des Add-ons oder an Dritte gesendet. Das Add-on enthält keine Analyse-, Tracking- oder Werbefunktionen.
Die Verbindung ist nicht verschlüsselt (ws://), weil die lokale Schnittstelle von ManicTime keine Verschlüsselung unterstützt. Die Daten laufen nur über die interne Loopback-Schnittstelle des Rechners, die aus dem Netzwerk nicht erreichbar ist.

Was mit den Daten in ManicTime geschieht
ManicTime speichert die empfangenen Daten in seiner eigenen Datenbank, um sie auf Ihren Zeitleisten anzuzeigen. Wie ManicTime diese Daten speichert, synchronisiert oder weitergibt, hängt von Ihren ManicTime-Einstellungen ab, zum Beispiel von einem eingerichteten ManicTime Server. Dafür gilt die Datenschutzerklärung von ManicTime, nicht die dieses Add-ons.

Was das Add-on speichert
Das Add-on speichert nur eine Einstellung, die maximale Betreff-Länge, im lokalen Add-on-Speicher von Thunderbird. Mail-Daten speichert es nicht.

Websites
Das Add-on interagiert nicht mit Websites, und Websites können es nicht erkennen.

Ihre Kontrolle
In den Add-on-Einstellungen können Sie Betreffzeilen kürzen. Um die Übertragung zu beenden, deaktivieren oder entfernen Sie das Add-on in Thunderbird unter Add-ons und Themes.

Kontakt
Fragen und Probleme: https://github.com/jhit/ManicTime-Tracker-for-Thunderbird/issues
