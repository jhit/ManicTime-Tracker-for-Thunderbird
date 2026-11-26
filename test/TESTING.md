# Testing ManicTime Tracker for Thunderbird

The add-on has no UI of its own. It runs in the background and sends the mail in the focused Thunderbird window to ManicTime's local WebSocket `ws://127.0.0.1:42870/manictime-document/` (ports 42870–42879). You can test it with ManicTime (option A), or without it by using the mock server in this folder (option B).

Requirements: Thunderbird 115 or newer with the add-on installed. To load it unsigned, use *Tools → Developer Tools → Debug Add-ons → Load Temporary Add-on* and select `src/manifest.json`.

## Option A – with ManicTime

1. Install the ManicTime desktop client from <https://www.manictime.com> and start it. It runs on Windows, macOS and Linux.
2. Start Thunderbird with the add-on.
3. Select a mail in the message list, or open one in a tab or window. Then open a new compose window and enter a recipient and a subject.
4. In ManicTime, open today's day view. Within a few seconds:
   - The **Documents** timeline shows entries such as `From: <sender>, To: <receiver>`, grouped as `<account>/INBOX` (when reading) or `<account>/compose` (when composing).
   - The **Applications** timeline shows the subject as the Thunderbird window title.
5. Optional: under *Tools → Add-ons and Themes → ManicTime Tracker for Thunderbird → ⋯ → Options*, set "Maximum subject length" to `10`. New entries in ManicTime then show the subject shortened to 10 characters, ending with `…`.

## Option B – without ManicTime (mock server)

`manictime-mock.py` imitates ManicTime's local socket and prints every message the add-on sends. It uses only the Python 3 standard library.

1. Run the mock server:
   ```
   python3 manictime-mock.py
   ```
   It listens on `ws://127.0.0.1:42870/manictime-document/`.
2. Start Thunderbird with the add-on. The add-on connects within 10 seconds, and the server prints `# connected 127.0.0.1`.
3. Select or compose a mail. The terminal prints one line per process name (`thunderbird` and `thunderbird-bin`). It prints them whenever the mail changes, and again every 5 seconds:
   ```
   {"ProcessName": "thunderbird", "Title": "<subject>", "DocumentType": "ManicTime/Email", "DocumentName": "From: <sender>, To: <receiver>", "DocumentGroup": "<account>/INBOX"}
   ```
4. Click on something that is not a mail, for example a folder with no message selected. `Title`, `DocumentType`, `DocumentName` and `DocumentGroup` then become `null`.
5. Optional: set "Maximum subject length" as in option A, step 5. `Title` is then shortened.

### Options

- `--port <n>`: listen on another port. Use this if ManicTime is already running and holds port 42870. Pick a port from 42871–42879: the add-on tries those ports when it starts and then every 60 seconds, so the connection can take up to a minute.
- `--redact`: print only the length of the subject, addresses and folder, not their text. Use it when the output is shared, for example in logs or bug reports.
