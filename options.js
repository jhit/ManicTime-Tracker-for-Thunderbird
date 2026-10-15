// ManicTime Tracker for Thunderbird - Copyright (C) 2026 Jürgen Hörmann
// SPDX-License-Identifier: GPL-3.0-or-later
for (const el of document.querySelectorAll("[data-i18n]")) {
  el.textContent = messenger.i18n.getMessage(el.dataset.i18n);
}
document.documentElement.lang = messenger.i18n.getUILanguage();

const input = document.getElementById("max");
const saved = document.getElementById("saved");
let timer;

messenger.storage.local.get({ maxSubject: 0 }).then((o) => (input.value = o.maxSubject));

input.addEventListener("input", async () => {
  const n = Math.max(0, parseInt(input.value, 10) || 0);
  await messenger.storage.local.set({ maxSubject: n });
  saved.hidden = false;
  clearTimeout(timer);
  timer = setTimeout(() => (saved.hidden = true), 1500);
});
