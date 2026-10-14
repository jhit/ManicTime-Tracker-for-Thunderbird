// Thunderbird Tracker for ManicTime - Copyright (C) 2026 Jürgen Hörmann
// SPDX-License-Identifier: GPL-3.0-or-later
// Polls the focused Thunderbird window and sends From/To/Subject to the local
// ManicTime client via its document-tracker WebSocket (the same one the
// ManicTime Chrome/Firefox extension uses).
const FIRST_PORT = 42870;
const PORT_COUNT = 10;
const PROCESS_NAMES = ["thunderbird", "thunderbird-bin"]; // as seen by ManicTime
const POLL_MS = 2000;
const HEARTBEAT_MS = 5000;

const sockets = new Map(); // port -> WebSocket (open or connecting)
let lastMessages = null;
let lastKey = null;
let lastSent = 0;

function connect(onlyFirst) {
  const last = onlyFirst ? FIRST_PORT + 1 : FIRST_PORT + PORT_COUNT;
  for (let port = FIRST_PORT; port < last; port++) {
    if (sockets.has(port)) continue;
    let ws;
    try {
      ws = new WebSocket("ws://127.0.0.1:" + port + "/manictime-document/");
    } catch (e) {
      continue;
    }
    sockets.set(port, ws);
    ws.onopen = () => {
      if (lastMessages) lastMessages.forEach((m) => ws.send(m));
    };
    ws.onclose = ws.onerror = () => sockets.delete(port);
  }
}

function broadcast(messages) {
  lastMessages = messages;
  for (const ws of sockets.values()) {
    if (ws.readyState !== WebSocket.OPEN) continue;
    try {
      messages.forEach((m) => ws.send(m));
    } catch (e) {}
  }
}

let maxSubject = 0; // 0 = do not shorten

async function loadOptions() {
  const o = await messenger.storage.local.get({ maxSubject: 0 });
  maxSubject = Math.max(0, parseInt(o.maxSubject, 10) || 0);
  lastKey = null; // resend with the new setting
}
messenger.storage.onChanged.addListener(loadOptions);

function shorten(subject) {
  const chars = Array.from(subject);
  return maxSubject > 0 && chars.length > maxSubject
    ? chars.slice(0, maxSubject).join("").trimEnd() + "…"
    : subject;
}

function toMessages(info) {
  const active = info.mode === "read" || info.mode === "compose";
  const title = active
    ? `From: ${info.from}, To: ${info.to}, Subject: ${shorten(info.subject)}`
    : null;
  // ManicTime treats the document like a web page: host = group name.
  const url = active ? `https://thunderbird/${info.mode === "compose" ? "compose" : "read"}` : null;
  return PROCESS_NAMES.map((p) =>
    JSON.stringify({ ProcessName: p, Title: title, Url: url, IsPrivate: active ? false : null })
  );
}

function addrList(list) {
  return (list || []).join("; ");
}

async function currentInfo() {
  const win = await messenger.windows.getLastFocused({ populate: true });
  if (!win || !win.focused) return { mode: "none" };
  const tab = (win.tabs || []).find((t) => t.active);
  if (!tab) return { mode: "none" };

  if (win.type === "messageCompose") {
    const d = await messenger.compose.getComposeDetails(tab.id);
    return {
      mode: "compose",
      from: d.from || "",
      to: addrList((d.to || []).map((r) => (typeof r === "string" ? r : r.id || ""))),
      subject: d.subject || "",
    };
  }

  // 3-pane window (selected mail) or message tab/window
  let msg = null;
  try {
    msg = await messenger.messageDisplay.getDisplayedMessage(tab.id);
  } catch (e) {}
  if (!msg) return { mode: "none" };
  return {
    mode: "read",
    from: msg.author || "",
    to: addrList(msg.recipients),
    subject: msg.subject || "",
  };
}

async function tick() {
  let info;
  try {
    info = await currentInfo();
  } catch (e) {
    info = { mode: "none" };
  }
  const key = JSON.stringify(info);
  const now = Date.now();
  if (key !== lastKey || now - lastSent >= HEARTBEAT_MS) {
    lastKey = key;
    lastSent = now;
    broadcast(toMessages(info));
  }
}

loadOptions();
connect();
setInterval(() => connect(true), 10000); // main port
setInterval(() => connect(false), 60000); // fallback ports
setInterval(tick, POLL_MS);
tick();
