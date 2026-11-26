// ManicTime Tracker for Thunderbird - Copyright (C) 2026 Jürgen Hörmann
// SPDX-License-Identifier: GPL-3.0-or-later
// Polls the focused Thunderbird window and sends From/To/Subject as a
// "ManicTime/Email" document (the format the ManicTime Outlook plugin uses)
// to the local ManicTime client via its document-tracker WebSocket.
const FIRST_PORT = 42870;
const PORT_COUNT = 10;
const PROCESS_NAMES = ["thunderbird", "thunderbird-bin"]; // as seen by ManicTime
const POLL_MS = 2000;
const HEARTBEAT_MS = 5000;
const CONNECT_TIMEOUT_MS = 3000;
const RETRY_MIN_MS = 10000; // wait after a scan that found nothing, doubled ...
const RETRY_MAX_MS = 60000; // ... after each failed scan up to this limit

let socket = null; // the open connection to ManicTime, or null
let scanning = false;
let retryMs = RETRY_MIN_MS;
let retryTimer = null;
let lastMessages = null;
let lastKey = null;
let lastSent = 0;

// Resolves with the WebSocket once it is open, or with null if it fails.
function tryPort(port) {
  return new Promise((resolve) => {
    let ws;
    try {
      ws = new WebSocket("ws://127.0.0.1:" + port + "/manictime-document/");
    } catch (e) {
      resolve(null);
      return;
    }
    const timer = setTimeout(() => {
      ws.close();
      resolve(null);
    }, CONNECT_TIMEOUT_MS);
    ws.onopen = () => {
      clearTimeout(timer);
      resolve(ws);
    };
    ws.onerror = ws.onclose = () => {
      clearTimeout(timer);
      resolve(null);
    };
  });
}

// Tries the ports in order and keeps the first connection that opens. Scans
// again only when that connection closes; if no port answers, retries later.
async function scan() {
  if (scanning || socket) return;
  scanning = true;
  clearTimeout(retryTimer);
  for (let port = FIRST_PORT; port < FIRST_PORT + PORT_COUNT; port++) {
    const ws = await tryPort(port);
    if (!ws) continue;
    socket = ws;
    scanning = false;
    retryMs = RETRY_MIN_MS;
    ws.onerror = null;
    ws.onclose = () => {
      if (socket !== ws) return;
      socket = null;
      scan();
    };
    if (lastMessages) send(lastMessages);
    return;
  }
  scanning = false;
  retryTimer = setTimeout(scan, retryMs);
  retryMs = Math.min(retryMs * 2, RETRY_MAX_MS);
}

function send(messages) {
  lastMessages = messages;
  if (!socket || socket.readyState !== WebSocket.OPEN) return;
  try {
    messages.forEach((m) => socket.send(m));
  } catch (e) {}
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
  let msg = { Title: null, DocumentType: null, DocumentName: null, DocumentGroup: null };
  if (active) {
    const subject = shorten(info.subject);
    const name = `From: ${info.from}, To: ${info.to}`;
    const folder = info.mode === "compose" ? "compose" : info.folder || "unknown";
    msg = {
      Title: subject,
      DocumentType: "ManicTime/Email",
      DocumentName: name,
      DocumentGroup: `${info.account || "unknown"}/${folder}`,
    };
  }
  return PROCESS_NAMES.map((p) => JSON.stringify({ ProcessName: p, ...msg }));
}

function addrList(list) {
  return (list || []).join("; ");
}

const accountNames = new Map(); // accountId -> name (cleared when accounts change)
messenger.accounts.onCreated?.addListener(() => accountNames.clear());
messenger.accounts.onUpdated?.addListener(() => accountNames.clear());
messenger.accounts.onDeleted?.addListener(() => accountNames.clear());

async function accountName(accountId) {
  if (!accountId) return "";
  if (!accountNames.has(accountId)) {
    try {
      const a = await messenger.accounts.get(accountId);
      accountNames.set(accountId, (a && a.name) || "");
    } catch (e) {
      return "";
    }
  }
  return accountNames.get(accountId);
}

// Folder shown in the 3-pane tab if it is a search (virtual), unified or tag
// folder: "virtual/<name>", "unified/<name>" or "tag/<name>". Otherwise "".
async function specialFolder(tabId) {
  try {
    const f = (await messenger.mailTabs.get(tabId)).displayedFolder;
    if (!f) return "";
    const kind = f.isVirtual ? "virtual" : f.isUnified ? "unified" : f.isTag ? "tag" : "";
    return kind ? kind + "/" + (f.name || "") : "";
  } catch (e) {
    return ""; // not a mail tab (message tab/window)
  }
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
      account: await accountName(
        d.identityId ? (await messenger.identities.get(d.identityId))?.accountId : null
      ),
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
    account: await accountName(msg.folder && msg.folder.accountId),
    folder: (await specialFolder(tab.id)) || (msg.folder && msg.folder.path) || "",
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
    send(toMessages(info));
  }
}

loadOptions();
scan();
setInterval(tick, POLL_MS);
tick();
