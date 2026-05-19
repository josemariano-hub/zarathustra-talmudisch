// =====================================================================
// Zarathustra · Talmudische Ausgabe — interactive renderer
// =====================================================================
// Reads the same PreTeXt XML source the `pretext build` toolchain reads
// (../source/ch_vorrede.ptx) plus a JSON commentary sidecar, and renders
// a Talmud-style page:  inner margin · center (Urtext + mother tongue) ·
// outer margin · bottom strata.  Dynamic behaviour: active verse +
// associated commentary highlight, others dim; scroll, ↑/↓ and click all
// drive selection; SVG threads draw between active center text and its
// commentary notes.
// =====================================================================

const params = new URLSearchParams(location.search);
const LANG  = ["en","fr","es"].includes(params.get("lang")) ? params.get("lang") : "en";
// Chapter identifier: either the legacy "vorrede" (hand-tuned with rich
// commentary) or one of the auto-generated chapter ids (e.g. "ch-p1-01").
const CHAPTER_ID = params.get("ch") || "vorrede";

// Source base path — works both locally (served from /web/...) and
// when deployed flat (served from /...). The reader and source/ live as
// siblings in both layouts; we detect which we're under and route.
const SRC_BASE = (location.pathname.includes("/web/") ? "../source" : "source") + "/";

function chapterUrl(navEntry, id) {
  if (id === "vorrede") return SRC_BASE + "ch_vorrede.ptx";
  if (navEntry) return SRC_BASE + navEntry.file;
  return null;
}

const NAV_URL  = SRC_BASE + "chapter-nav.json";
const JSON_URL = SRC_BASE + "commentary.json";

// stream colour map — mirrors style.css (kept here for inline use)
const STREAM_COLORS = {
  philology: "#8b5e3c", lampert: "#7a3b3b", higgins: "#3b5a7a",
  rosen: "#5a3b7a", "gooding-williams": "#7a5a3b",
  klossowski: "#a04a55", deleuze: "#c46a3a",
  "sanchez-pascual": "#d4a23a", "sanchez-meca": "#3a8a8a",
  "sanchez-pascual-notes": "#d4a23a", "sp-introduction": "#b58a3a",
  "new-cambridge": "#3a6a3a",
  crossref: "#3b7a5a", loeb: "#5a7a3b"
};

// Short verse label for note tags: "ch-p3-12-v07" → "v.7"; "v05" → "v.5"
function shortVerseLabel(target) {
  if (!target) return "";
  const m = target.match(/v(\d+)$/);
  if (!m) return target;
  return "v." + parseInt(m[1], 10);
}

// Strict text-only HTML emitter: keep <em>, escape everything else.
// Prevents stored-XSS from any commentary text that ever embeds markup.
function safeHTML(s) {
  if (s == null) return "";
  const esc = String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
  // restore <em>…</em> only
  return esc.replace(/&lt;em&gt;(.*?)&lt;\/em&gt;/g, "<em>$1</em>");
}

// Strip page references ("p. 132", "pp 200-204") and turn known chapter
// titles into clickable links. Operates on already-escaped HTML so
// inserted <a> tags stay safe.
function enrichNote(html, lang) {
  if (!html) return "";
  // 1. drop page refs (Spanish "p.", English "p.", French "p.")
  html = html.replace(/,?\s*\bpp?\.?\s*\d{1,4}(?:[\-–—]\d{1,4})?(\s*y\s*ss?\.?)?/gi, "");
  html = html.replace(/\s+([\.,;])/g, "$1");           // collapse spaces before punctuation
  // 2. link chapter title references (longest-first, case-insensitive,
  //    word-boundary anchored). state.titleIndex is built once in main().
  const idx = state.titleIndex?.[lang];
  if (idx) {
    for (const { title, xml_id, escaped } of idx) {
      const re = new RegExp("(^|[\\s\"'«(>])(" + escaped + ")(?=[\\s\\.,;:!\\?»)<]|$)", "g");
      const target = xml_id === "ch-p0-00" ? "vorrede" : xml_id;
      html = html.replace(re,
        `$1<a class="xref" href="?lang=${lang}&ch=${target}">$2</a>`);
    }
  }
  return html;
}

function buildTitleIndex(nav) {
  const out = { en: [], fr: [], es: [] };
  for (const lang of ["en", "fr", "es"]) {
    const items = [];
    for (const e of nav) {
      const t = e[lang];
      if (!t || t.length < 4) continue;
      // Strip trailing punctuation from titles when matching
      const cleanTitle = t.replace(/[\.,;:!\?]+$/, "").trim();
      items.push({
        title: cleanTitle,
        xml_id: e.xml_id,
        escaped: cleanTitle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
      });
    }
    // longest first so "El más feo de los hombres" beats "El más"
    items.sort((a, b) => b.title.length - a.title.length);
    out[lang] = items;
  }
  return out;
}

const FLAGS = { fr: "🇫🇷", es: "🇪🇸", en: "🇬🇧", de: "🇩🇪" };

// ---------- bootstrap ---------------------------------------------------
fetch(NAV_URL).then(r => r.json()).then(nav => {
  state.nav = nav;
  state.titleIndex = buildTitleIndex(nav);
  const entry = nav.find(c => c.xml_id === CHAPTER_ID || (CHAPTER_ID === "vorrede" && c.xml_id === "ch-p0-00"));
  state.navEntry = entry;
  state.chapterId = CHAPTER_ID;

  const ptxUrl = chapterUrl(entry, CHAPTER_ID);
  return Promise.all([
    fetch(ptxUrl).then(r => r.text()).then(parsePTX),
    fetch(JSON_URL).then(r => r.json())
  ]);
}).then(([chapter, commentary]) => {
  state.chapter = chapter;
  state.commentary = commentary;
  renderBreadcrumb();
  renderLangToggle();
  renderCenter();
  $("#loading")?.remove();
  // Always render margins/strata; per-stream `notes` lists filter naturally
  // by target verse id, so chapters without applicable notes simply show
  // empty margins.
  renderMargins();
  renderStrata();
  installScrollSpy();
  // Restore active verse from URL hash if it points to a valid verse.
  const initialId = (location.hash || "").slice(1);
  const startVerse = state.chapter.verses.find(v => v.id === initialId)?.id
                  || state.chapter.verses[0].id;
  setActiveVerse(startVerse, /*scroll*/ initialId !== "");
  ["scroll","keydown","click"].forEach(ev =>
    window.addEventListener(ev, () => $("#zoom-hint")?.remove(), { once:true }));
  installChapterNav();
}).catch(err => {
  document.body.innerHTML = `<pre style="padding:2rem;color:#a00">${err}\n${err.stack}</pre>`;
});

// Localized UI strings (per current state.lang)
const UI = {
  en: { prologue: "Prologue", part: ["Prologue","First Part","Second Part","Third Part","Fourth and Last Part"],
        chap: "Ch.", back: "← Back", next: "Next →", start: "← Start", end: "End →" },
  fr: { prologue: "Prologue", part: ["Prologue","Première Partie","Deuxième Partie","Troisième Partie","Quatrième et Dernière Partie"],
        chap: "Ch.", back: "← Retour", next: "Suivant →", start: "← Début", end: "Fin →" },
  es: { prologue: "Prólogo", part: ["Prólogo","Primera parte","Segunda parte","Tercera parte","Cuarta y última parte"],
        chap: "Cap.", back: "← Atrás", next: "Siguiente →", start: "← Inicio", end: "Fin →" },
  de: { prologue: "Vorrede", part: ["Vorrede","Erster Theil","Zweiter Theil","Dritter Theil","Vierter und letzter Theil"],
        chap: "Kap.", back: "← Zurück", next: "Weiter →", start: "← Anfang", end: "Ende →" },
};
function ui() { return UI[state.lang] || UI.de; }

function renderBreadcrumb() {
  // Update the top crumbs with the current chapter
  const head = $(".page-head");
  if (!head) return;
  const entry = state.navEntry;
  if (!entry) return;
  const u = ui();
  const partLabel = u.part[entry.part] || u.part[0];
  // Replace existing crumbs (first 3 spans)
  const crumbs = head.querySelectorAll(".crumb");
  if (crumbs[0]) crumbs[0].textContent = partLabel;
  if (crumbs[1]) crumbs[1].textContent = entry.idx === 0 ? u.prologue : `${u.chap} ${entry.idx}`;
  if (crumbs[2]) crumbs[2].textContent = entry[state.lang] || entry.de;
}

function installChapterNav() {
  if (!state.nav) return;
  const idx = state.nav.findIndex(c => c.xml_id === state.navEntry?.xml_id);
  const prev = idx > 0 ? state.nav[idx-1] : null;
  const next = idx >= 0 && idx < state.nav.length - 1 ? state.nav[idx+1] : null;
  const goto = (entry) => {
    if (!entry) return;
    const target = (entry.xml_id === "ch-p0-00") ? "vorrede" : entry.xml_id;
    location.search = `?lang=${state.lang}&ch=${target}`;
  };
  window.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") goto(next);
    if (e.key === "ArrowLeft")  goto(prev);
  });

  // Append a prev/next footer to the centre column so users can move
  // between chapters without keyboard or breadcrumb.
  const center = $("#center");
  if (center) {
    const foot = el("nav", { className: "chapter-foot" });
    const mkLink = (entry, dir) => {
      const a = el("a", { className: `chapter-foot-link ${dir}` });
      if (entry) {
        const target = (entry.xml_id === "ch-p0-00") ? "vorrede" : entry.xml_id;
        a.href = `?lang=${state.lang}&ch=${target}`;
        const u = ui();
        a.append(
          el("span", { className: "dir", textContent: dir === "prev" ? u.back : u.next }),
          el("span", { className: "title", textContent: entry[state.lang] || entry.de })
        );
      } else {
        a.classList.add("disabled");
        const u = ui();
        a.append(el("span", { className: "dir", textContent: dir === "prev" ? u.start : u.end }));
      }
      return a;
    };
    foot.append(mkLink(prev, "prev"), mkLink(next, "next"));
    center.append(foot);
  }

  // table of contents drawer
  const toc = $("#toc");
  const body = $("#toc-body");
  body.innerHTML = "";
  const PART_LABEL = ui().part;
  let curPart = -1;
  for (const entry of state.nav) {
    if (entry.part !== curPart) {
      curPart = entry.part;
      const h = el("h3", { className: "toc-part", textContent: PART_LABEL[entry.part] });
      body.append(h);
    }
    const target = (entry.xml_id === "ch-p0-00") ? "vorrede" : entry.xml_id;
    const a = el("a", { className: "toc-item", href: `?lang=${state.lang}&ch=${target}` });
    if (entry.xml_id === state.navEntry?.xml_id) a.classList.add("active");
    a.append(
      el("span", { className: "toc-no", textContent: entry.part === 0 ? "—" : String(entry.idx) }),
      el("span", { className: "toc-name", textContent: entry[state.lang] || entry.de })
    );
    body.append(a);
  }
  const open  = () => { toc.hidden = false;  requestAnimationFrame(() => toc.classList.add("open")); };
  const close = () => { toc.classList.remove("open"); setTimeout(() => toc.hidden = true, 300); };
  $("#toc-toggle").addEventListener("click", () => toc.hidden ? open() : close());
  $("#toc-close").addEventListener("click", close);
  window.addEventListener("keydown", e => {
    if (e.key === "Escape") close();
  });
}

// ---------- state -------------------------------------------------------
const state = {
  lang: LANG, chapter: null, commentary: null, activeVerse: null,
  spySuspended: false        // pause IntersectionObserver during programmatic scroll
};

// ---------- helpers -----------------------------------------------------
const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const el = (tag, props = {}, ...children) => {
  const e = Object.assign(document.createElement(tag), props);
  for (const c of children) {
    if (c == null) continue;
    e.append(c.nodeType ? c : document.createTextNode(c));
  }
  return e;
};

// ---------- PreTeXt parser ---------------------------------------------
// Pulls out the chapter title, section title, and an ordered list of
// verses; for each verse, collects all <p xml:id="vNN-XX"> across all
// languages.  Preserves <em> markup.
function parsePTX(text) {
  const xml = new DOMParser().parseFromString(text, "application/xml");
  const err = xml.querySelector("parsererror");
  if (err) throw new Error("PreTeXt parse error: " + err.textContent);

  const chapter = xml.querySelector("chapter");
  const section = chapter.querySelector("section");

  const verses = $$(":scope > paragraphs", section).map(node => {
    const id = node.getAttribute("xml:id");
    const title = node.querySelector(":scope > title")?.textContent.trim() || id;
    const byLang = {};
    $$(":scope > p", node).forEach(p => {
      const lang = p.getAttribute("xml:lang") || "de";
      byLang[lang] = stripPreserveEm(p);
    });
    return { id, title, byLang };
  });

  return {
    chapterTitle: chapter.querySelector(":scope > title")?.textContent.trim(),
    sectionTitle: section.querySelector(":scope > title")?.textContent.trim(),
    intro:        section.querySelector(":scope > introduction > p")?.textContent.trim() || "",
    verses
  };
}

function stripPreserveEm(node) {
  // Convert the <p> children into HTML with <em> preserved, other tags
  // stripped.  Collapses whitespace.
  const out = [];
  const walk = (n) => {
    if (n.nodeType === 3) { out.push(n.textContent); return; }
    const name = (n.localName || n.nodeName || "").toLowerCase();
    if (name === "em") {
      const inner = (n.textContent || "").replace(/\s+/g, " ").trim();
      if (inner) out.push(`<em>${inner}</em>`);
    } else {
      n.childNodes.forEach(walk);
    }
  };
  walk(node);
  return out.join("").replace(/\s+/g, " ").trim();
}

// ---------- rendering --------------------------------------------------
function renderLangToggle() {
  const target = $("#lang-toggle");
  target.innerHTML = "";
  const langs = [["en","EN"],["fr","FR"],["es","ES"]];
  const chParam = state.chapterId ? `&ch=${state.chapterId}` : "";
  for (const [code,label] of langs) {
    const a = el("a", { href: `?lang=${code}${chParam}`, textContent: label });
    if (code === state.lang) a.className = "active";
    target.append(a);
  }
}

function renderCenter() {
  const center = $("#center");
  const { verses } = state.chapter;
  for (const v of verses) {
    const node = el("article", { id: v.id, className: "verse", tabIndex: 0 },
      el("span", { className: "verse-mark", textContent: v.title })
    );
    const de = v.byLang.de ?? "";
    const tr = v.byLang[state.lang] ?? v.byLang.en ?? "";
    const pDe = el("p", { className: "de" }); pDe.innerHTML = safeHTML(de);
    const pTr = el("p", { className: "tr" }); pTr.innerHTML = safeHTML(tr);
    node.append(pDe, pTr);
    // Mobile-only inline commentary: shown when viewport is too narrow
    // for the radial Talmudic margins. Hidden by CSS on desktop.
    const inline = el("div", { className: "mobile-notes" });
    inline.dataset.target = v.id;
    node.append(inline);
    node.addEventListener("click", e => {
      if (window.getSelection().toString().length > 0) return;
      setActiveVerse(v.id, /*scroll*/ true);
    });
    node.addEventListener("focus", () => setActiveVerse(v.id, /*scroll*/ true));
    center.append(node);
  }
  // Populate the inline mobile notes from commentary streams
  fillMobileNotes();
}

function fillMobileNotes() {
  const verseIds = new Set(state.chapter.verses.map(v => v.id));
  // Group notes by target verse
  const byVerse = {};
  for (const [key, stream] of Object.entries(state.commentary.streams)) {
    if (stream._disabled || key.startsWith("_")) continue;
    for (const n of stream.notes) {
      if (!verseIds.has(n.target)) continue;
      const body = n[state.lang];
      if (!body) continue;
      (byVerse[n.target] ||= []).push({ key, stream, note: n, body });
    }
  }
  for (const [vid, items] of Object.entries(byVerse)) {
    const host = document.querySelector(`.verse[id="${CSS.escape(vid)}"] .mobile-notes`);
    if (!host) continue;
    for (const { key, stream, note, body } of items) {
      const card = el("div", { className: "mobile-note" });
      card.style.setProperty("--stream", stream.color);
      const head = el("span", { className: "mobile-note-stream",
        textContent: stream.label[state.lang] || key });
      if (stream.bibliographic) head.title = stream.bibliographic;
      if (stream._origin && stream._origin !== state.lang) {
        head.append(el("span", { className: "origin-badge",
          textContent: ` ${FLAGS[stream._origin]||""} ${stream._origin.toUpperCase()}` }));
      }
      if (note._audit_flag === "weak") card.classList.add("weak");
      const text = el("span", { className: "mobile-note-body" });
      text.innerHTML = enrichNote(safeHTML(body.replace(/\n/g," ")), state.lang);
      card.append(head, text);
      host.append(card);
    }
  }
}

function renderMargins() {
  const inner = $("#margin-inner"), outer = $("#margin-outer");
  // Verse ids visible on the current page (so we can filter streams)
  const verseIds = new Set(state.chapter.verses.map(v => v.id));
  for (const [key, stream] of Object.entries(state.commentary.streams)) {
    if (stream._disabled || key.startsWith("_")) continue;
    if (stream.side === "bottom") continue;
    const relevantStream = filterStreamForChapter(stream, verseIds);
    if (relevantStream.notes.length === 0) continue;
    const container = stream.side === "inner" ? inner : outer;
    container.append(renderStream(key, relevantStream));
  }
}

function filterStreamForChapter(stream, verseIds) {
  return {
    ...stream,
    notes: stream.notes.filter(n => verseIds.has(n.target))
  };
}

function renderStrata() {
  const strata = $("#strata");
  const verseIds = new Set(state.chapter.verses.map(v => v.id));
  for (const [key, stream0] of Object.entries(state.commentary.streams)) {
    if (stream0._disabled || key.startsWith("_")) continue;
    if (stream0.side !== "bottom") continue;
    const stream = filterStreamForChapter(stream0, verseIds);
    if (stream.notes.length === 0) continue;
    const div = el("div", { className: "stratum" });
    div.style.setProperty("--stream", stream.color);
    const stratumLabel = el("span", { className: "stratum-label", textContent: stream.label[state.lang] || key });
    if (stream.bibliographic) stratumLabel.title = stream.bibliographic;
    if (stream._origin && stream._origin !== state.lang) {
      const badge = el("span", { className: "origin-badge",
        textContent: ` ${FLAGS[stream._origin]||""} ${stream._origin.toUpperCase()}` });
      badge.title = "Auto-translated from " + stream._origin.toUpperCase() +
                    " via Gemini 2.5 Flash.";
      stratumLabel.append(badge);
    }
    div.append(stratumLabel);
    for (const n of stream.notes) {
      const bodyText = n[state.lang];
      if (!bodyText) continue;
      const note = el("div", { className: "note" });
      note.dataset.target = n.target;
      note.dataset.stream = key;
      const tag = el("span", { className: "target-tag", textContent: shortVerseLabel(n.target) });
      if (n.note_n != null) {
        const nn = el("span", { className: "note-n", textContent: `№${n.note_n}` });
        nn.title = "Original footnote number in Sánchez Pascual (Alianza, 1972).";
        tag.append(" ", nn);
      }
      const body = el("span", { className: "body" });
      body.innerHTML = enrichNote(safeHTML(bodyText.replace(/\n/g," ")), state.lang);
      note.append(tag, body);
      if (n._audit_flag === "weak") {
        note.classList.add("weak");
        note.title = "Weak attribution (?). The LLM audit was unsure this note " +
                     "engages this specific verse; the source is otherwise " +
                     "relevant to the chapter. Treat as a starting point." +
                     (n._audit_reason ? "\n\nAudit note: " + n._audit_reason : "");
      }
      note.addEventListener("click", () => setActiveVerse(n.target));
      div.append(note);
    }
    strata.append(div);
  }
}

function renderStream(key, stream) {
  const wrap = el("div", { className: "stream" });
  wrap.style.setProperty("--stream", stream.color);
  const label = el("span", { className: "stream-label", textContent: stream.label[state.lang] || key });
  if (stream.bibliographic) label.title = stream.bibliographic;
  if (stream._origin && stream._origin !== state.lang) {
    const badge = el("span", { className: "origin-badge", textContent: ` ${FLAGS[stream._origin]||""} ${stream._origin.toUpperCase()}` });
    badge.title = "Auto-translated from " + stream._origin.toUpperCase() +
                  " via Gemini 2.5 Flash. Original wording in this badge’s language.";
    label.append(badge);
  }
  wrap.append(label);
  for (const n of stream.notes) {
    const note = el("div", { className: "note" });
    note.dataset.target = n.target;
    note.dataset.stream = key;
    const tag = el("span", { className: "target-tag", textContent: n.target });
    const bodyText = n[state.lang];
    if (!bodyText) continue;   // no English fallback for non-EN readers
    if (n.term) {
      const termText = (typeof n.term === "object") ? (n.term[state.lang] || "") : n.term;
      if (termText) {
        const term = el("span", { className: "term", textContent: termText + " — " });
        note.append(tag, term);
      } else {
        note.append(tag);
      }
    } else {
      note.append(tag);
    }
    const body = el("span", { className: "body" });
    body.innerHTML = enrichNote(safeHTML(bodyText.replace(/\n/g," ")), state.lang);
    note.append(body);
    if (n._audit_flag === "weak") {
      note.classList.add("weak");
      note.title = "Weak attribution: " + (n._audit_reason || "");
    }
    note.addEventListener("click", () => setActiveVerse(n.target));
    wrap.append(note);
  }
  return wrap;
}

// ---------- dynamics ---------------------------------------------------
function setActiveVerse(id, scroll = true) {
  if (id === state.activeVerse && !scroll) return;
  state.activeVerse = id;
  // Reflect active verse in URL hash (no history pollution).
  try { history.replaceState(null, "", "#" + id); } catch {}
  const verses = state.chapter.verses;
  const idx = verses.findIndex(v => v.id === id);

  // dim/brighten verses
  $$(".verse").forEach((v, i) => {
    v.classList.toggle("is-active", v.id === id);
    v.classList.toggle("is-neighbor", Math.abs(i - idx) === 1);
  });

  // dim/brighten margin + strata notes
  $$(".margin .note, .strata .note").forEach(n => {
    n.classList.toggle("is-active", n.dataset.target === id);
  });

  // scroll target verse into view — the spy will then keep the active
  // state in sync as the smooth scroll rolls through intermediate verses.
  if (scroll) {
    const verseEl = $("#" + CSS.escape(id));
    verseEl?.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  // centre the active notes inside their own scroll containers
  $$(".margin .note.is-active, .strata .note.is-active").forEach(n => {
    const container = n.closest(".margin, .stratum");
    if (!container) return;
    const cRect = container.getBoundingClientRect();
    const nRect = n.getBoundingClientRect();
    const offset = (nRect.top - cRect.top) - (cRect.height - nRect.height) / 2;
    container.scrollBy({ top: offset, behavior: "smooth" });
  });

  // active section title (top crumb): the hand-tuned Vorrede file (12 verses)
  // is §1 of the Vorrede, so prefix with "§ 1"; for the auto-parsed chapters
  // (the rest of the book) there is no further subdivision, just the verse id.
  const vTitle = state.chapter.verses[idx]?.title || "";
  $("#active-section").textContent =
    state.chapterId === "vorrede" ? `§ 1 · ${vTitle}` : vTitle;

  requestAnimationFrame(drawThreads);
}

function installScrollSpy() {
  // Active verse = whichever is closest to the vertical centre of the
  // scroll container. On desktop the container is `.center`; on phone the
  // whole window scrolls and the center column has no overflow.
  const center = $("#center");
  const verses = $$(".verse");
  const isMobile = () => window.matchMedia("(max-width: 700px)").matches;

  const updateActive = () => {
    const cRect = isMobile()
      ? { top: 0, height: window.innerHeight }
      : center.getBoundingClientRect();
    const targetY = cRect.top + cRect.height / 2;
    let bestId = null, bestDist = Infinity;
    for (const v of verses) {
      const vR = v.getBoundingClientRect();
      const mid = (vR.top + vR.bottom) / 2;
      const d = Math.abs(mid - targetY);
      if (d < bestDist) { bestDist = d; bestId = v.id; }
    }
    if (bestId && bestId !== state.activeVerse) {
      setActiveVerse(bestId, /*scroll*/ false);
    } else {
      drawThreads();
    }
  };

  let raf = 0;
  const sched = () => {
    if (!raf) raf = requestAnimationFrame(() => { raf = 0; updateActive(); });
  };
  // Desktop: center column scrolls. Mobile: window scrolls.
  center.addEventListener("scroll", sched, { passive: true });
  window.addEventListener("scroll", sched, { passive: true });
  $$(".margin, .stratum").forEach(c => c.addEventListener("scroll", () => {
    if (!raf) raf = requestAnimationFrame(() => { raf = 0; drawThreads(); });
  }, { passive: true }));
  window.addEventListener("resize", sched);

  // keyboard navigation — drives a smooth scroll to the next verse; the
  // scroll-spy then updates the active state as the page moves.
  window.addEventListener("keydown", e => {
    const i = verses.findIndex(v => v.id === state.activeVerse);
    if (e.key === "ArrowDown" || e.key === "j") {
      e.preventDefault();
      const next = verses[Math.min(verses.length - 1, i + 1)];
      next && setActiveVerse(next.id, /*scroll*/ true);
    } else if (e.key === "ArrowUp" || e.key === "k") {
      e.preventDefault();
      const prev = verses[Math.max(0, i - 1)];
      prev && setActiveVerse(prev.id, /*scroll*/ true);
    }
  });
}

// ---------- threads (SVG lines from active verse to active notes) -----
//
// Geometry rules:
//   • Endpoints are clamped to within the visible page bounds; if either
//     side is fully off-page, the thread is skipped entirely (no curves
//     trailing off the screen).
//   • The verse-side endpoint is anchored on the inner edge of the centre
//     column (left or right depending on which margin the note lives in),
//     not the geometric centre of the verse, so the curve doesn't cross
//     the central text.
function drawThreads() {
  const svg = $("#threads");
  if (!svg) return;
  const page = $("#page");
  const center = $("#center");
  const r = page.getBoundingClientRect();
  const cR = center.getBoundingClientRect();
  svg.setAttribute("viewBox", `0 0 ${r.width} ${r.height}`);
  svg.innerHTML = "";

  const verseEl = state.activeVerse && $("#" + CSS.escape(state.activeVerse));
  if (!verseEl) return;
  const vR = verseEl.getBoundingClientRect();
  // skip entirely if the active verse is fully off-page
  if (vR.bottom < r.top + 4 || vR.top > r.bottom - 4) return;

  // verse-side Y, clamped to visible page (with a small inset)
  const PAD = 24;
  const vYRaw = (vR.top + vR.bottom) / 2 - r.top;
  const vy = Math.max(PAD, Math.min(r.height - PAD, vYRaw));
  // Anchor the verse end *inside* the centre column so threads visibly
  // terminate at the text, not at the column edge. The inset is wider than
  // the column padding so the dot lands on the actual paragraph margin.
  const INSET = 28;
  const xLeft  = cR.left  - r.left + INSET;
  const xRight = cR.right - r.left - INSET;

  $$(".margin .note.is-active, .strata .note.is-active").forEach(n => {
    const nR = n.getBoundingClientRect();
    // skip notes that are fully off-page
    if (nR.bottom < r.top + 4 || nR.top > r.bottom - 4) return;

    const inInner = !!n.closest(".margin-inner");
    const inOuter = !!n.closest(".margin-outer");
    const inStrata = !!n.closest(".stratum");

    // note-side anchor point + verse-side anchor point
    let fromX, fromY, toX, toY;
    if (inInner) {
      fromX = nR.right - r.left;   // inner-margin right edge
      fromY = (nR.top + nR.bottom) / 2 - r.top;
      toX = xLeft;                 // centre column's left edge
      toY = vy;
    } else if (inOuter) {
      fromX = nR.left - r.left;    // outer-margin left edge
      fromY = (nR.top + nR.bottom) / 2 - r.top;
      toX = xRight;                // centre column's right edge
      toY = vy;
    } else { // strata at bottom
      fromX = (nR.left + nR.right) / 2 - r.left;
      fromY = nR.top - r.top;      // top edge of stratum note
      // route to the bottom of the verse on the side closest to the note
      const toLeft = fromX < (cR.left + cR.right) / 2 - r.left;
      toX = toLeft ? xLeft : xRight;
      toY = vy;
    }

    // clamp every coordinate to the visible page rectangle
    fromX = Math.max(PAD, Math.min(r.width - PAD, fromX));
    fromY = Math.max(PAD, Math.min(r.height - PAD, fromY));
    toX   = Math.max(PAD, Math.min(r.width - PAD, toX));
    toY   = Math.max(PAD, Math.min(r.height - PAD, toY));

    // gentle horizontal bezier (calligraphic, not aggressive)
    const dx = toX - fromX;
    const cx1 = fromX + dx * 0.45;
    const cx2 = toX   - dx * 0.45;
    const color = STREAM_COLORS[n.dataset.stream] || "#999";
    const NS = "http://www.w3.org/2000/svg";

    const path = document.createElementNS(NS,"path");
    path.setAttribute("d", `M ${fromX} ${fromY} C ${cx1} ${fromY}, ${cx2} ${toY}, ${toX} ${toY}`);
    path.setAttribute("stroke", color);
    path.setAttribute("class", "is-active");
    svg.appendChild(path);

    // terminal dot at the verse side — makes the destination unambiguous
    const dot = document.createElementNS(NS,"circle");
    dot.setAttribute("cx", toX);
    dot.setAttribute("cy", toY);
    dot.setAttribute("r", 3.2);
    dot.setAttribute("fill", color);
    dot.setAttribute("class", "is-active");
    svg.appendChild(dot);

    // smaller origin dot at the note side
    const odot = document.createElementNS(NS,"circle");
    odot.setAttribute("cx", fromX);
    odot.setAttribute("cy", fromY);
    odot.setAttribute("r", 2);
    odot.setAttribute("fill", color);
    odot.setAttribute("class", "is-active");
    svg.appendChild(odot);
  });
}
