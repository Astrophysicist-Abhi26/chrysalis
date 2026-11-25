/* Chrysalis background: a garden that changes with the theme.
   By day, tiny butterflies drift between faint muscle cells, vesicles, mitochondria, leaves and
   flowers; by night the same garden is lit by tiny blinking fireflies. Everything sits behind the
   content (it never covers text), is weighted by the ranking profile's interests, and stays still
   when the reader prefers reduced motion. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const DAY = ["#ffc83d", "#ff6fae", "#9b7bff", "#3fd6a6", "#4fb8ff", "#ff9f43"];
  const rnd = (a, b) => a + Math.random() * (b - a);
  let svg = null, last = null;
  const isDark = () => {
    const t = document.documentElement.dataset.theme;
    if (t === "dark") return true;
    if (t === "light") return false;
    return !!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
  };
  const MOTIFS = {
    myotube: (c) => `<rect x="-36" y="-8" width="72" height="16" rx="8" fill="${c}" opacity=".45"/>` +
      [-22, -7, 8, 23].map((x) => `<ellipse cx="${x}" rx="4.5" ry="3" fill="#7b4fd6" opacity=".6"/>`).join(""),
    vesicle: (c) => `<circle r="10" fill="${c}" fill-opacity=".14" stroke="${c}" stroke-width="2"/><circle r="6" fill="none" stroke="${c}" stroke-width="1.2"/>`,
    cell: (c) => `<circle r="20" fill="${c}" opacity=".16" stroke="${c}" stroke-width="2"/><circle cx="3" cy="-2" r="7" fill="${c}" opacity=".55"/>` +
      `<circle cx="22" cy="-14" r="3.5" fill="none" stroke="${c}" stroke-width="1.4"/><circle cx="28" cy="-22" r="2.5" fill="none" stroke="${c}" stroke-width="1.2"/>`,
    mito: (c) => `<ellipse rx="20" ry="10" fill="none" stroke="${c}" stroke-width="2.6"/><path d="M-13 0q4-7 8 0t8 0 8 0" stroke="${c}" stroke-width="1.8" fill="none"/>`,
    leaf: (c) => `<path d="M0 18C-14 4-10-14 0-20C10-14 14 4 0 18Z" fill="${c}" opacity=".45"/><path d="M0 18V-16" stroke="${c}" stroke-width="1.4"/>`,
    flower: (c) => [0, 72, 144, 216, 288].map((a) => `<ellipse cy="-8" rx="4" ry="7" fill="${c}" opacity=".55" transform="rotate(${a})"/>`).join("") + `<circle r="3.5" fill="#ffc83d"/>`,
    dna: (c) => `<path d="M-8-20C10-10-10 10 8 20M8-20C-10-10 10 10-8 20" stroke="${c}" stroke-width="2.4" fill="none"/>`,
  };
  const FACTS = ["A muscle fibre can hold hundreds of nuclei", "Exosomes are only about 30–150 nm across",
    "Fireflies glow with luciferase — the enzyme in reporter assays", "Butterflies taste with their feet",
    "A chrysalis is where a caterpillar rebuilds itself", "Cells talk by mailing tiny vesicles"];
  function butterfly(c1, c2) {
    return `<g class="wl"><path d="M0 0C-6-12-16-12-15-4C-14 2-6 3 0 0Z" fill="${c1}"/><path d="M0 1C-5 8-11 10-11 5C-11 2-5 1 0 1Z" fill="${c2}"/></g>` +
      `<g class="wr"><path d="M0 0C6-12 16-12 15-4C14 2 6 3 0 0Z" fill="${c1}"/><path d="M0 1C5 8 11 10 11 5C11 2 5 1 0 1Z" fill="${c2}"/></g>` +
      `<rect x="-1" y="-6" width="2" height="12" rx="1" fill="#4a3a30"/>`;
  }
  function render(opts) {
    if (opts) last = opts;
    const host = document.getElementById("bg");
    if (!host) return;
    const weight = (last && last.weight) || (() => 50);
    const dark = isDark();
    const still = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    const W = 1600, H = 1000, mol = weight("molbio") || 40;
    const pool = [["myotube", 10 + mol / 8], ["vesicle", 12 + mol / 8], ["cell", 8 + mol / 10], ["mito", 6 + mol / 12], ["dna", 4],
      ["leaf", 10], ["flower", 9]];
    const pick = () => { let r = Math.random() * pool.reduce((s, [, w]) => s + w, 0); for (const [k, w] of pool) if ((r -= w) <= 0) return k; return "vesicle"; };
    let out = `<defs><radialGradient id="ffg"><stop offset="0" stop-color="#f6ff9e" stop-opacity="1"/><stop offset=".35" stop-color="#c6ff5a" stop-opacity=".7"/>` +
      `<stop offset="1" stop-color="#c6ff5a" stop-opacity="0"/></radialGradient></defs><style>
      .dr{animation:dr var(--d) ease-in-out infinite alternate}@keyframes dr{to{transform:translate(var(--x),var(--y)) rotate(var(--r))}}
      .fly{animation:fly var(--d) ease-in-out infinite alternate}
      @keyframes fly{25%{transform:translate(var(--x1),var(--y1))}50%{transform:translate(var(--x2),var(--y2))}75%{transform:translate(var(--x3),var(--y3))}100%{transform:translate(var(--x4),var(--y4))}}
      .wl,.wr{transform-box:fill-box;animation:flap .28s ease-in-out infinite alternate}.wl{transform-origin:right center}.wr{transform-origin:left center}
      @keyframes flap{to{transform:scaleX(.3)}}
      .ff{animation:ffd var(--d) ease-in-out infinite alternate,blink var(--b) ease-in-out infinite}
      @keyframes ffd{to{transform:translate(var(--x),var(--y))}}@keyframes blink{0%,100%{opacity:.05}45%,60%{opacity:1}}
      .ft{font:600 14px Lexend,system-ui,sans-serif;fill:currentColor;opacity:${dark ? ".22" : ".28"}}
      ${still ? "*{animation:none!important}" : ""}</style>`;
    // faint garden of cells (both themes)
    for (let i = 0; i < 22; i++) {
      const m = pick(), c = DAY[(Math.random() * DAY.length) | 0];
      out += `<g transform="translate(${rnd(30, W - 30).toFixed(0)} ${rnd(30, H - 30).toFixed(0)}) scale(${rnd(.8, 1.7).toFixed(2)}) rotate(${rnd(-40, 40).toFixed(0)})" opacity="${dark ? ".35" : ".5"}">` +
        `<g class="dr" style="--d:${rnd(8, 16).toFixed(1)}s;--x:${rnd(-30, 30).toFixed(0)}px;--y:${rnd(-30, 30).toFixed(0)}px;--r:${rnd(-20, 20).toFixed(0)}deg">${MOTIFS[m](c)}</g></g>`;
    }
    if (dark) {
      // tiny fireflies: a dot of light with a soft halo, blinking out of step
      for (let i = 0; i < 46; i++) {
        out += `<g transform="translate(${rnd(0, W).toFixed(0)} ${rnd(0, H).toFixed(0)})"><g class="ff" style="--d:${rnd(6, 14).toFixed(1)}s;--b:${rnd(2.2, 5).toFixed(1)}s;` +
          `--x:${rnd(-60, 60).toFixed(0)}px;--y:${rnd(-50, 50).toFixed(0)}px;animation-delay:0s,${rnd(0, 5).toFixed(1)}s">` +
          `<circle r="${rnd(5, 8).toFixed(1)}" fill="url(#ffg)"/><circle r="1.4" fill="#fbffd0"/></g></g>`;
      }
    } else {
      // tiny butterflies wandering across the page
      for (let i = 0; i < 9; i++) {
        const c1 = DAY[i % DAY.length], c2 = DAY[(i + 2) % DAY.length], v = () => `${rnd(-220, 220).toFixed(0)}px`;
        out += `<g transform="translate(${rnd(60, W - 60).toFixed(0)} ${rnd(60, H - 60).toFixed(0)}) scale(${rnd(.55, .85).toFixed(2)})">` +
          `<g class="fly" style="--d:${rnd(14, 26).toFixed(0)}s;--x1:${v()};--y1:${v()};--x2:${v()};--y2:${v()};--x3:${v()};--y3:${v()};--x4:${v()};--y4:${v()}">` +
          butterfly(c1, c2) + `</g></g>`;
      }
    }
    FACTS.slice().sort(() => Math.random() - .5).slice(0, 3).forEach((f, i) => {
      out += `<text class="ft" x="${rnd(60, W - 520).toFixed(0)}" y="${(240 + i * 280 + rnd(-40, 40)).toFixed(0)}">${dark ? "✦" : "🦋"} ${f}</text>`;
    });
    if (!svg) { svg = document.createElementNS(NS, "svg"); svg.setAttribute("preserveAspectRatio", "xMidYMid slice"); host.appendChild(svg); }
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.innerHTML = out;
    host.dataset.motifs = String(svg.querySelectorAll(".dr").length);
    host.dataset.mode = dark ? "fireflies" : "butterflies";
  }
  if (typeof MutationObserver !== "undefined") {
    new MutationObserver(() => render()).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  }
  if (window.matchMedia) {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq && mq.addEventListener) mq.addEventListener("change", () => render());
  }
  window.PPBackground = { render };
})();
