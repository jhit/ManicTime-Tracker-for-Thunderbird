Privacy Policy – ManicTime Tracker for Thunderbird

This text is meant to be pasted as-is into the privacy policy field on addons.thunderbird.net. German version: PRIVACY.de.md.

---

ManicTime Tracker for Thunderbird reports the mail you are working on in Thunderbird to the ManicTime time-tracking client on your own computer. This policy describes what the add-on does with your data.

What data is sent
While a Thunderbird window is focused and you are reading or composing a mail, the add-on sends the following data about that mail:
- sender (From)
- recipients (To)
- subject (shortened if you set a maximum length in the add-on options)
- name of the Thunderbird mail account
- folder in which the mail is shown (or "compose" when writing a mail)
It also sends the fixed program name "thunderbird", so that ManicTime can assign the data to Thunderbird. The data is sent when it changes and every 5 seconds. When no mail is being read or composed, empty values are sent. The add-on never reads or sends the body or the attachments of a mail.

Where the data goes
The data is sent only to 127.0.0.1, ports 42870–42879. This is the local WebSocket interface of the ManicTime client on the same computer. The data never leaves your computer, and the add-on makes no other network connections. Nothing is sent to the developer of the add-on or to any third party. The add-on contains no analytics, tracking or advertising.
The connection is not encrypted (ws://), because ManicTime's local interface does not support encryption. The data travels only over the computer's internal loopback interface, which is not reachable from the network.

What happens with the data in ManicTime
ManicTime stores the received data in its own database to show it on your timelines. How ManicTime stores, syncs or shares this data depends on your ManicTime settings, for example a ManicTime Server you have configured. That is governed by ManicTime's own privacy policy, not by this add-on.

What the add-on stores
The add-on stores only one setting, the maximum subject length, in Thunderbird's local storage for add-ons. It does not store any mail data.

Websites
The add-on does not interact with websites, and websites cannot detect it.

Your control
You can shorten subjects in the add-on options. To stop the transmission, disable or remove the add-on in Thunderbird under Add-ons and Themes.

Contact
Questions and issues: https://github.com/jhit/ManicTime-Tracker-for-Thunderbird/issues
