#!/usr/bin/env python3
# ManicTime Tracker for Thunderbird - Copyright (C) 2026 Jürgen Hörmann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Stand-in for ManicTime's local document-tracker WebSocket, for testing the
add-on without ManicTime. Python 3 standard library only.

    python3 test/manictime-mock.py [--port 42870] [--redact]

Listens on ws://127.0.0.1:<port>/manictime-document/ and prints every message
the add-on sends, one JSON object per line. The add-on connects to port 42870
at start and retries it every 10 s; ports 42871-42879 are retried every 60 s
(use one of them if ManicTime itself already occupies 42870).
--redact replaces mail data (subject, addresses, folder) by its length.
"""
import argparse
import base64
import hashlib
import json
import socketserver
import struct
import sys

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
PATH = "/manictime-document/"


def redact(text):
    try:
        msg = json.loads(text)
    except ValueError:
        return text
    for k in ("Title", "DocumentName", "DocumentGroup"):
        if isinstance(msg.get(k), str):
            msg[k] = "<%d chars>" % len(msg[k])
    return json.dumps(msg, ensure_ascii=False)


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        request = self.rfile.readline().decode("latin-1").split()
        headers = {}
        while True:
            line = self.rfile.readline().decode("latin-1").strip()
            if not line:
                break
            k, _, v = line.partition(":")
            headers[k.strip().lower()] = v.strip()
        key = headers.get("sec-websocket-key")
        if len(request) < 2 or request[1] != PATH or not key:
            self.wfile.write(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n")
            return
        accept = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
        self.wfile.write(("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                          "Connection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n" % accept).encode())
        log("connected " + self.client_address[0])
        try:
            while self.read_frame():
                pass
        except (ConnectionError, struct.error):
            pass
        log("disconnected")

    def read_frame(self):
        head = self.rfile.read(2)
        if len(head) < 2:
            return False
        opcode = head[0] & 0x0F
        length = head[1] & 0x7F
        if length == 126:
            length = struct.unpack(">H", self.rfile.read(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self.rfile.read(8))[0]
        mask = self.rfile.read(4) if head[1] & 0x80 else b"\0\0\0\0"
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(self.rfile.read(length)))
        if opcode == 0x8:  # close
            self.wfile.write(b"\x88\x00")
            return False
        if opcode == 0x9:  # ping -> pong
            self.wfile.write(bytes([0x8A, len(data)]) + data)
        elif opcode == 0x1:  # text (the add-on sends small unfragmented frames)
            text = data.decode("utf-8")
            print(redact(text) if ARGS.redact else text, flush=True)
        return True


def log(text):
    print("# " + text, file=sys.stderr, flush=True)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--port", type=int, default=42870)
    p.add_argument("--redact", action="store_true", help="hide mail data in the output")
    ARGS = p.parse_args()
    with Server(("127.0.0.1", ARGS.port), Handler) as srv:
        log("listening on ws://127.0.0.1:%d%s" % (ARGS.port, PATH))
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
