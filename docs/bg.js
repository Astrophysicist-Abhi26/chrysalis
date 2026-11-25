/* Chrysalis background and flyers.
   #bg (behind the content): a faint garden of muscle cells, vesicles, mitochondria, leaves,
   flowers and fun facts, weighted by the ranking profile's interests.
   #flyers (over the content, click-through): tiny butterflies by day and fireflies by night that
   wander slowly across the whole page. Both switch with the theme, and the flyers are not drawn at
   all when the reader prefers reduced motion. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const DAY = ["#ffc83d", "#ff6fae", "#9b7bff", "#3fd6a6", "#4fb8ff", "#ff9f43"];
  const BUTTERFLIES = 9, FIREFLIES = 46;
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
  const FLY_CSS = `<style>
    #flyers .w{position:absolute;left:0;top:0;will-change:transform;animation:cw var(--d) ease-in-out infinite alternate;animation-delay:var(--dl)}
    @keyframes cw{0%{transform:translate(var(--x0),var(--y0))}25%{transform:translate(var(--x1),var(--y1))}
      50%{transform:translate(var(--x2),var(--y2))}75%{transform:translate(var(--x3),var(--y3))}100%{transform:translate(var(--x4),var(--y4))}}
    #flyers .bob{animation:cbob 1.7s ease-in-out infinite alternate}
    @keyframes cbob{to{transform:translateY(-7px) rotate(9deg)}}
    #flyers .wl,#flyers .wr{transform-box:fill-box;animation:cflap .26s ease-in-out infinite alternate}
    #flyers .wl{transform-origin:right center}#flyers .wr{transform-origin:left center}
    @keyframes cflap{to{transform:scaleX(.3)}}
    #flyers .ff{display:block;width:11px;height:11px;border-radius:50%;
      background:radial-gradient(circle,#fbffd0 0 16%,rgba(198,255,90,.8) 30%,rgba(198,255,90,0) 70%);
      animation:cblink var(--b) ease-in-out infinite;animation-delay:var(--bd)}
    @keyframes cblink{0%,100%{opacity:.05}45%,60%{opacity:.95}}
  </style>`;
  function butterflySvg(c1, c2, w) {
    return `<svg width="${w}" height="${(w * 0.8).toFixed(0)}" viewBox="-17 -14 34 27" aria-hidden="true">` +
      `<g class="wl"><path d="M0 0C-6-12-16-12-15-4C-14 2-6 3 0 0Z" fill="${c1}"/><path d="M0 1C-5 8-11 10-11 5C-11 2-5 1 0 1Z" fill="${c2}"/></g>` +
      `<g class="wr"><path d="M0 0C6-12 16-12 15-4C14 2 6 3 0 0Z" fill="${c1}"/><path d="M0 1C5 8 11 10 11 5C11 2 5 1 0 1Z" fill="${c2}"/></g>` +
      `<rect x="-1" y="-6" width="2" height="12" rx="1" fill="#4a3a30"/></svg>`;
  }
  // a route of five waypoints spread over the whole window (vw/vh), so each flyer crosses the page
  function route() {
    let s = "";
    for (let k = 0; k < 5; k++) s += `--x${k}:${rnd(1, 97).toFixed(1)}vw;--y${k}:${rnd(4, 94).toFixed(1)}vh;`;
    return s;
  }
  function drawFlyers(dark, still) {
    let host = document.getElementById("flyers");
    if (!host) {
      host = document.createElement("div");
      host.id = "flyers";
      host.setAttribute("aria-hidden", "true");
      host.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:45;overflow:hidden";
      document.body.appendChild(host);
    }
    if (still) { host.innerHTML = ""; host.dataset.count = "0"; return; }
    let out = FLY_CSS;
    if (dark) {
      for (let i = 0; i < FIREFLIES; i++) {
        out += `<div class="w" style="${route()}--d:${rnd(50, 110).toFixed(0)}s;--dl:-${rnd(0, 60).toFixed(0)}s">` +
          `<i class="ff" style="--b:${rnd(2.2, 5).toFixed(1)}s;--bd:${rnd(0, 5).toFixed(1)}s"></i></div>`;
      }
    } else {
      for (let i = 0; i < BUTTERFLIES; i++) {
        out += `<div class="w bf" style="${route()}--d:${rnd(45, 80).toFixed(0)}s;--dl:-${rnd(0, 40).toFixed(0)}s"><div class="bob">` +
          butterflySvg(DAY[i % DAY.length], DAY[(i + 2) % DAY.length], Math.round(rnd(16, 24))) + `</div></div>`;
      }
    }
    host.innerHTML = out;
    host.dataset.count = String(dark ? FIREFLIES : BUTTERFLIES);
    host.dataset.mode = dark ? "fireflies" : "butterflies";
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
    let out = `<style>
      .dr{animation:dr var(--d) ease-in-out infinite alternate}@keyframes dr{to{transform:translate(var(--x),var(--y)) rotate(var(--r))}}
      .ft{font:600 14px Lexend,system-ui,sans-serif;fill:currentColor;opacity:${dark ? ".22" : ".28"}}
      ${still ? "*{animation:none!important}" : ""}</style>`;
    for (let i = 0; i < 22; i++) {
      const m = pick(), c = DAY[(Math.random() * DAY.length) | 0];
      out += `<g transform="translate(${rnd(30, W - 30).toFixed(0)} ${rnd(30, H - 30).toFixed(0)}) scale(${rnd(.8, 1.7).toFixed(2)}) rotate(${rnd(-40, 40).toFixed(0)})" opacity="${dark ? ".35" : ".5"}">` +
        `<g class="dr" style="--d:${rnd(8, 16).toFixed(1)}s;--x:${rnd(-30, 30).toFixed(0)}px;--y:${rnd(-30, 30).toFixed(0)}px;--r:${rnd(-20, 20).toFixed(0)}deg">${MOTIFS[m](c)}</g></g>`;
    }
    FACTS.slice().sort(() => Math.random() - .5).slice(0, 3).forEach((f, i) => {
      out += `<text class="ft" x="${rnd(60, W - 520).toFixed(0)}" y="${(240 + i * 280 + rnd(-40, 40)).toFixed(0)}">${dark ? "✦" : "🦋"} ${f}</text>`;
    });
    if (!svg) { svg = document.createElementNS(NS, "svg"); svg.setAttribute("preserveAspectRatio", "xMidYMid slice"); host.appendChild(svg); }
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.innerHTML = out;
    host.dataset.motifs = String(svg.querySelectorAll(".dr").length);
    host.dataset.mode = dark ? "fireflies" : "butterflies";
    drawFlyers(dark, still);
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
