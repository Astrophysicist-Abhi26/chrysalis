"""
Redraws Chrysalis's artwork: Megha's avatar (docs/megha.svg), the app icon
(docs/icon.svg + PNGs) and the Android launcher layers.
Needs:  pip install resvg-py        Run from the repository root:  python tools/make_art.py
"""
import math, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
random.seed(11)

# ── palette taken from her photo ──────────────────────────────────────────────
SKIN_HI, SKIN, SKIN_MID, SKIN_SH = "#F1C6A4", "#E0AC88", "#CB9370", "#AC7255"
HAIR_HI, HAIR = "#4B3B40", "#130D11"
DRESS_HI, DRESS, DRESS_SH = "#FFD84D", "#F2B705", "#D18F00"

def butterfly(x, y, s, c1, c2, cls="bf", delay=0.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><g class="{cls}" style="animation-delay:{delay:.1f}s">'
            f'<g class="wl"><path d="M0 0C-6-12-16-12-15-4C-14 2-6 3 0 0Z" fill="{c1}"/><path d="M0 1C-5 8-11 10-11 5C-11 2-5 1 0 1Z" fill="{c2}"/></g>'
            f'<g class="wr"><path d="M0 0C6-12 16-12 15-4C14 2 6 3 0 0Z" fill="{c1}"/><path d="M0 1C5 8 11 10 11 5C11 2 5 1 0 1Z" fill="{c2}"/></g>'
            f'<rect x="-1.1" y="-6" width="2.2" height="12" rx="1.1" fill="#3A2A2E"/>'
            f'<path d="M-.6-6Q-3-11-5-12M.6-6Q3-11 5-12" stroke="#3A2A2E" stroke-width=".7" fill="none"/></g></g>')

def vesicle(x, y, r, c, delay):
    return (f'<g class="ev" style="animation-delay:{delay:.1f}s"><circle cx="{x}" cy="{y}" r="{r}" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.62:.1f}" fill="none" stroke="{c}" stroke-width=".9" opacity=".8"/>'
            f'<circle cx="{x - r*0.35:.1f}" cy="{y - r*0.35:.1f}" r="{r*0.18:.1f}" fill="#FFFFFF" opacity=".8"/></g>')

def myotube(x, y, w, rot, c):
    nuclei = "".join(f'<ellipse cx="{x - w/2 + 14 + k*(w-28)/3:.0f}" cy="{y}" rx="5" ry="3.2" fill="#7B4FD6" opacity=".75"/>' for k in range(4))
    return (f'<g transform="rotate({rot} {x} {y})" opacity=".55"><rect x="{x - w/2}" y="{y-9}" width="{w}" height="18" rx="9" fill="{c}"/>{nuclei}</g>')

def daisy(x, y, s, c):
    petals = "".join(f'<ellipse cx="0" cy="-7" rx="3.2" ry="6.5" fill="#FFFFFF" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return f'<g transform="translate({x} {y}) scale({s})">{petals}<circle r="4" fill="{c}"/></g>'

dots = "".join(f'<circle cx="{(i % 4) * 14 + (7 if (i // 4) % 2 else 0)}" cy="{(i // 4) * 14}" r="1.7" fill="#FFFFFF" opacity=".9"/>' for i in range(16))

avatar = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" role="img" aria-labelledby="t d">
<title id="t">Megha Pashupati</title>
<desc id="d">Illustrated 3D-style avatar of Megha: oval face with a big happy smile, black hair side-parted and tied back, a sunflower-yellow kurta with white dots, holding a cell-culture flask of pink medium from which tiny extracellular vesicles drift, with small butterflies in a sunny garden of muscle cells.</desc>
<style>
.bf{{animation:fl 7s ease-in-out infinite}} @keyframes fl{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(10px,-12px)}}}}
.wl,.wr{{transform-box:fill-box;animation:flap .32s ease-in-out infinite alternate}} .wl{{transform-origin:right center}} .wr{{transform-origin:left center}}
@keyframes flap{{to{{transform:scaleX(.35)}}}}
.ev{{animation:rise 5.5s ease-in-out infinite}} @keyframes rise{{0%{{transform:translate(0,0);opacity:0}}15%{{opacity:1}}100%{{transform:translate(-14px,-70px);opacity:0}}}}
.head{{transform-origin:222px 290px;animation:tilt 6s ease-in-out infinite}} @keyframes tilt{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(2deg)}}}}
.flask{{transform-origin:252px 400px;animation:sway 4s ease-in-out infinite}} @keyframes sway{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-3deg)}}}}
.ring{{animation:hue 12s linear infinite}} @keyframes hue{{to{{filter:hue-rotate(360deg)}}}}
.sp{{animation:tw 3s ease-in-out infinite}} @keyframes tw{{0%,100%{{opacity:.2}}50%{{opacity:1}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs>
  <radialGradient id="sky" cx="50%" cy="38%" r="65%"><stop offset="0" stop-color="#FFFBE6"/><stop offset=".55" stop-color="#D6F7E3"/><stop offset="1" stop-color="#7FD3A8"/></radialGradient>
  <radialGradient id="sun" cx="78%" cy="18%" r="35%"><stop offset="0" stop-color="#FFE27A" stop-opacity=".9"/><stop offset="1" stop-color="#FFE27A" stop-opacity="0"/></radialGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFC83D"/><stop offset=".35" stop-color="#FF6FAE"/><stop offset=".7" stop-color="#9B7BFF"/><stop offset="1" stop-color="#3FD6A6"/></linearGradient>
  <radialGradient id="face" cx="40%" cy="34%" r="72%"><stop offset="0" stop-color="{SKIN_HI}"/><stop offset=".45" stop-color="{SKIN}"/><stop offset=".78" stop-color="{SKIN_MID}"/><stop offset="1" stop-color="#AD775C"/></radialGradient>
  <radialGradient id="ear" cx="40%" cy="40%" r="70%"><stop offset="0" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_SH}"/></radialGradient>
  <linearGradient id="neck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B27A5F"/><stop offset=".45" stop-color="{SKIN_MID}"/><stop offset="1" stop-color="{SKIN}"/></linearGradient>
  <linearGradient id="hair" x1="0" y1="0" x2=".8" y2="1"><stop offset="0" stop-color="{HAIR_HI}"/><stop offset=".45" stop-color="#231A20"/><stop offset="1" stop-color="{HAIR}"/></linearGradient>
  <linearGradient id="dress" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DRESS_HI}"/><stop offset=".5" stop-color="{DRESS}"/><stop offset="1" stop-color="{DRESS_SH}"/></linearGradient>
  <pattern id="dots" width="56" height="56" patternUnits="userSpaceOnUse">{dots}</pattern>
  <radialGradient id="dshade" cx="50%" cy="20%" r="85%"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#7A4A00" stop-opacity=".35"/></radialGradient>
  <radialGradient id="iris" cx="45%" cy="35%" r="65%"><stop offset="0" stop-color="#7A4A2A"/><stop offset=".6" stop-color="#4A2A18"/><stop offset="1" stop-color="#24120A"/></radialGradient>
  <linearGradient id="hand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKIN_HI}"/><stop offset="1" stop-color="{SKIN_MID}"/></linearGradient>
  <linearGradient id="medium" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF8FB8"/><stop offset="1" stop-color="#E0457B"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset="1" stop-color="#E6F1FF" stop-opacity=".55"/></linearGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#2D5B3F" flood-opacity=".35"/></filter>
  <filter id="blur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
  <clipPath id="disc"><circle cx="220" cy="220" r="200"/></clipPath>
</defs>

<!-- garden of cells -->
<circle cx="220" cy="220" r="214" fill="none" stroke="url(#rim)" stroke-width="12" opacity=".7" filter="url(#glow)" class="ring"/>
<circle cx="220" cy="220" r="206" fill="none" stroke="url(#rim)" stroke-width="6" class="ring"/>
<circle cx="220" cy="220" r="200" fill="url(#sky)"/>
<g clip-path="url(#disc)">
  <circle cx="220" cy="220" r="200" fill="url(#sun)"/>
  {myotube(92, 150, 120, -28, "#FFB3CC")}{myotube(352, 128, 110, 24, "#FFC2D6")}{myotube(70, 250, 96, 12, "#FFB3CC")}
  <circle cx="358" cy="262" r="30" fill="#C9B8FF" opacity=".45"/><circle cx="364" cy="258" r="11" fill="#7B4FD6" opacity=".6"/>
  {vesicle(336, 222, 7, "#9B7BFF", 0)}{vesicle(392, 300, 5, "#FF6FAE", 1.4)}{vesicle(60, 196, 6, "#3FD6A6", 2.2)}
  <path d="M20 420C80 360 140 380 180 420M260 420C300 370 380 360 430 410" fill="#5DBB86" opacity=".55"/>
  {daisy(64, 352, 1.1, "#FFC83D")}{daisy(384, 360, 0.9, "#FF6FAE")}{daisy(104, 392, 0.7, "#FFC83D")}
  <!-- kurta: sunflower yellow with white dots -->
  <g filter="url(#soft)">
    <path d="M284 214C300 228 304 252 296 272C290 258 284 244 274 232Z" fill="url(#hair)"/>
    <path d="M96 440C98 368 128 318 176 300L204 284L222 302L240 284L268 300C316 318 346 368 348 440Z" fill="url(#dress)"/>
    <path d="M96 440C98 368 128 318 176 300L204 284L222 302L240 284L268 300C316 318 346 368 348 440Z" fill="url(#dots)"/>
    <path d="M96 440C98 368 128 318 176 300L204 284L222 302L240 284L268 300C316 318 346 368 348 440Z" fill="url(#dshade)"/>
    <path d="M204 282L180 298L194 324L219 303Z" fill="url(#dress)" stroke="#C88A00" stroke-width="1.2" stroke-linejoin="round"/>
    <path d="M240 282L264 298L250 324L225 303Z" fill="url(#dress)" stroke="#C88A00" stroke-width="1.2" stroke-linejoin="round"/>
    <path d="M222 303V440" stroke="#C88A00" stroke-width="2"/>
    <circle cx="222" cy="330" r="2.6" fill="#FFF4C2" stroke="#B07800"/><circle cx="222" cy="362" r="2.6" fill="#FFF4C2" stroke="#B07800"/>
  </g>
</g>

<!-- neck and head: oval face, big smile, side-swept hair tied back -->
<path d="M204 258L240 258L242 304L202 304Z" fill="url(#neck)"/>
<g class="head" filter="url(#soft)">
  <path d="M136 204C126 116 170 54 224 54C280 54 320 116 308 204C302 184 296 168 288 158L158 158C148 170 140 186 136 204Z" fill="url(#hair)"/>
  <ellipse cx="151" cy="200" rx="9" ry="13" fill="url(#ear)"/><ellipse cx="153" cy="201" rx="4" ry="7.5" fill="{SKIN_SH}" opacity=".55"/>
  <ellipse cx="293" cy="200" rx="9" ry="13" fill="url(#ear)"/><ellipse cx="291" cy="201" rx="4" ry="7.5" fill="{SKIN_SH}" opacity=".55"/>
  <path d="M151 184C151 130 184 102 222 102C260 102 293 130 293 184C293 236 264 266 222 270C180 266 151 236 151 184Z" fill="url(#face)"/>
  <path d="M160 214C166 246 188 266 222 272" fill="none" stroke="#FFF1E6" stroke-width="2.6" opacity=".3" stroke-linecap="round"/>
  <path d="M284 210C280 242 260 262 232 270" fill="none" stroke="#9E6A52" stroke-width="5" opacity=".18" stroke-linecap="round" filter="url(#blur2)"/>
  <ellipse cx="200" cy="140" rx="22" ry="9" fill="#FFFFFF" opacity=".12"/>
  <!-- hair: parting left of centre; fringe sweeps across to her left temple -->
  <path d="M194 60C164 68 150 100 149 140C148 160 151 178 154 194C158 170 164 150 174 138C182 130 190 126 197 124C192 106 191 80 194 60Z" fill="url(#hair)"/>
  <path d="M195 60C230 56 272 74 290 110C298 128 298 154 294 182C288 160 276 146 260 140C246 134 232 128 222 126C212 124 204 125 197 124C192 104 192 80 195 60Z" fill="url(#hair)"/>
  <path d="M197 124C210 121 232 124 252 134C266 141 280 152 290 170C276 150 260 140 244 134C228 128 212 126 197 124Z" fill="#2A1F25" opacity=".55"/>
  <path d="M195 62C193 84 194 106 197 123" stroke="#7E6A72" stroke-width="1.6" opacity=".8" fill="none"/>
  <path d="M206 70C236 70 266 84 282 110M204 86C230 86 258 100 274 122M206 104C228 106 250 116 266 132" stroke="#5D4A52" stroke-width="1.3" opacity=".7" fill="none"/>
  <path d="M208 62C232 60 258 68 276 86" stroke="#FFFFFF" stroke-width="4" opacity=".16" fill="none" stroke-linecap="round"/>
  <path d="M156 178C150 188 148 200 151 212M291 176C297 186 298 198 295 210" stroke="{HAIR}" stroke-width="1.3" fill="none" opacity=".8"/>
  <!-- rosy cheeks, soft brows, big sparkly eyes -->
  <ellipse cx="180" cy="223" rx="19" ry="11" fill="#FF8FA3" opacity=".42" filter="url(#blur2)"/>
  <ellipse cx="264" cy="223" rx="19" ry="11" fill="#FF8FA3" opacity=".42" filter="url(#blur2)"/>
  <ellipse cx="178" cy="214" rx="10" ry="5" fill="#FFFFFF" opacity=".2"/><ellipse cx="266" cy="214" rx="9" ry="4.5" fill="#FFFFFF" opacity=".14"/>
  <path d="M175 161Q191 152 208 157" stroke="#2A1C1E" stroke-width="3.8" fill="none" stroke-linecap="round"/>
  <path d="M236 157Q253 152 269 161" stroke="#2A1C1E" stroke-width="3.8" fill="none" stroke-linecap="round"/>
  <g class="eyes">
    <path d="M180 185Q194 169 208 185Q194 196 180 185Z" fill="#FFFFFF"/><path d="M236 185Q250 169 264 185Q250 196 236 185Z" fill="#FFFFFF"/>
    <circle cx="194.5" cy="184.5" r="7.4" fill="url(#iris)"/><circle cx="249.5" cy="184.5" r="7.4" fill="url(#iris)"/>
    <circle cx="194.5" cy="184.5" r="3.6" fill="#120806"/><circle cx="249.5" cy="184.5" r="3.6" fill="#120806"/>
    <circle cx="197.6" cy="181" r="2.5" fill="#FFFFFF"/><circle cx="252.6" cy="181" r="2.5" fill="#FFFFFF"/>
    <circle cx="192" cy="188" r="1.1" fill="#FFFFFF" opacity=".9"/><circle cx="247" cy="188" r="1.1" fill="#FFFFFF" opacity=".9"/>
    <path d="M178.5 184Q194 166 209.5 183M234.5 183Q250 166 265.5 184" stroke="#160C0C" stroke-width="3.2" fill="none" stroke-linecap="round"/>
    <path d="M181 181L175 177M184 177L180 172M263 181L269 177M260 177L264 172" stroke="#160C0C" stroke-width="2" stroke-linecap="round"/>
  </g>
  <!-- small cute nose -->
  <path d="M218 214Q222 219 227 214" stroke="#B57A60" stroke-width="2.1" fill="none" stroke-linecap="round"/>
  <ellipse cx="223" cy="208" rx="3.5" ry="2.5" fill="#FFFFFF" opacity=".28"/>
  <!-- sweet smile -->
  <path d="M203 237Q222 244 241 237Q237 254 222 256Q207 254 203 237Z" fill="#8A2A3A"/>
  <path d="M206 238Q222 244 238 238L236 243.5Q222 248 208 243.5Z" fill="#FFFFFF"/>
  <path d="M211 250Q222 245 233 250Q228 255 222 255Q216 255 211 250Z" fill="#F28C9A"/>
  <path d="M203 237Q222 244 241 237Q237 254 222 256Q207 254 203 237Z" fill="none" stroke="#C85C6C" stroke-width="2" stroke-linejoin="round"/>
  <path d="M199 235Q201 239 204 239.5M245 235Q243 239 240 239.5" stroke="#C07068" stroke-width="1.5" fill="none" opacity=".7" stroke-linecap="round"/>
  <!-- a tiny butterfly hair clip -->
  <g transform="translate(262 108) rotate(24) scale(.95)">
    <path d="M0 0C-6-12-16-12-15-4C-14 2-6 3 0 0Z" fill="#FF6FAE"/><path d="M0 1C-5 8-11 10-11 5C-11 2-5 1 0 1Z" fill="#FFC83D"/>
    <path d="M0 0C6-12 16-12 15-4C14 2 6 3 0 0Z" fill="#FF6FAE"/><path d="M0 1C5 8 11 10 11 5C11 2 5 1 0 1Z" fill="#FFC83D"/>
    <rect x="-1.2" y="-6" width="2.4" height="12" rx="1.2" fill="#3A2A2E"/>
    <circle cx="-8" cy="-5" r="1.6" fill="#FFFFFF" opacity=".8"/><circle cx="8" cy="-5" r="1.6" fill="#FFFFFF" opacity=".8"/>
  </g>
</g>

<!-- a culture flask of pink medium, shedding tiny vesicles -->
<g class="flask" filter="url(#soft)">
  <g transform="rotate(-14 252 384)">
    <path d="M222 352H276L286 336H300V352V412H222Z" fill="url(#glass)" stroke="#8AA6C8" stroke-width="2" stroke-linejoin="round"/>
    <path d="M224 376H298V410H224Z" fill="url(#medium)" opacity=".9"/>
    <path d="M224 376Q260 370 298 376" stroke="#FFFFFF" stroke-width="1.5" opacity=".7" fill="none"/>
    <rect x="296" y="328" width="16" height="14" rx="3" fill="#3D7BFF"/>
    <circle cx="240" cy="392" r="2" fill="#FFFFFF" opacity=".8"/><circle cx="256" cy="398" r="1.6" fill="#FFFFFF" opacity=".8"/><circle cx="272" cy="388" r="1.8" fill="#FFFFFF" opacity=".8"/>
    <path d="M228 356H262" stroke="#FFFFFF" stroke-width="2" opacity=".8"/>
  </g>
  <path d="M196 414C200 402 226 398 250 400C274 398 296 402 300 414C288 426 262 430 248 428C232 430 206 426 196 414Z" fill="url(#hand)"/>
  <ellipse cx="204" cy="404" rx="7" ry="12" transform="rotate(-30 204 404)" fill="url(#hand)"/>
  {vesicle(300, 318, 6, "#FF6FAE", 0.3)}{vesicle(318, 296, 4.5, "#9B7BFF", 1.8)}{vesicle(286, 300, 3.5, "#3FD6A6", 3.1)}
</g>

{butterfly(84, 92, 1.3, "#FF6FAE", "#FFC83D", delay=0)}
{butterfly(372, 196, 1.0, "#9B7BFF", "#3FD6A6", delay=1.5)}
{butterfly(318, 338, 0.8, "#FFC83D", "#FF6FAE", delay=2.6)}
<path class="sp" d="M120 300l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#FFFFFF"/>
<path class="sp" style="animation-delay:1.2s" d="M346 92l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#FFFFFF"/>
</svg>'''
open(os.path.join(OUT, "megha.svg"), "w").write(avatar)

# ── app icon: a butterfly with vesicle wing-spots on a sunrise gradient ──────
WINGS = [(-1, 1, -22, -14, 19, 14, -35), (1, 1, 22, -14, 19, 14, 35), (-1, 1, -16, 12, 12, 9, 30), (1, 1, 16, 12, 12, 9, -30)]
def icon_fg(s, mono=False):
    f = lambda v: f"{v*s:.2f}"
    o = []
    for _, _, cx, cy, rx, ry, rot in WINGS:
        o.append(f'<ellipse cx="{f(54+cx)}" cy="{f(52+cy)}" rx="{f(rx)}" ry="{f(ry)}" transform="rotate({rot} {f(54+cx)} {f(52+cy)})" fill="#FFFFFF"/>')
    spots = [(-24, -16, 5.5, "#FF6FAE"), (24, -16, 5.5, "#FF6FAE"), (-16, 12, 4, "#FFC83D"), (16, 12, 4, "#FFC83D")]
    for x, y, r, c in spots:
        col = "#FFFFFF" if mono else c
        o.append(f'<circle cx="{f(54+x)}" cy="{f(52+y)}" r="{f(r)}" fill="{col}" stroke="{"#FFFFFF" if mono else "#FFFFFF"}" stroke-width="{f(1.2)}"/>' if not mono else "")
    o.append(f'<rect x="{f(51.5)}" y="{f(32)}" width="{f(5)}" height="{f(40)}" rx="{f(2.5)}" fill="{"#FFFFFF" if mono else "#3A2A2E"}"/>')
    o.append(f'<path d="M{f(53)} {f(33)}Q{f(46)} {f(22)} {f(42)} {f(21)}M{f(55)} {f(33)}Q{f(62)} {f(22)} {f(66)} {f(21)}" stroke="{"#FFFFFF" if mono else "#3A2A2E"}" stroke-width="{f(2)}" fill="none" stroke-linecap="round"/>')
    return "".join(o)
BG = ('<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFB72B"/>'
      '<stop offset=".5" stop-color="#FF5E9C"/><stop offset="1" stop-color="#8A5CFF"/></linearGradient></defs>')
icon = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{BG}<rect width="512" height="512" rx="116" fill="url(#g)"/>{icon_fg(512/108)}</svg>'
mask = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{BG}<rect width="512" height="512" fill="url(#g)"/>{icon_fg(512/108)}</svg>'
open(os.path.join(OUT, "icon.svg"), "w").write(icon)

import resvg_py
def png(svg, size, path):
    open(path, "wb").write(bytes(resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size)))
png(icon, 192, f"{OUT}/icon-192.png"); png(icon, 512, f"{OUT}/icon-512.png")
png(mask, 512, f"{OUT}/icon-maskable-512.png"); png(mask, 180, f"{OUT}/apple-touch-icon.png")
if os.environ.get("PREVIEW"):
    png(avatar, 880, os.environ["PREVIEW"])

def epath(cx, cy, rx, ry):
    return f"M{cx-rx:.2f},{cy:.2f}a{rx:.2f},{ry:.2f} 0 1,0 {2*rx:.2f},0a{rx:.2f},{ry:.2f} 0 1,0 {-2*rx:.2f},0"
def vector(mono):
    p = ['<?xml version="1.0" encoding="utf-8"?>',
         '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">']
    for _, _, cx, cy, rx, ry, rot in WINGS:
        X, Y = 54 + cx, 52 + cy
        p.append(f'  <group android:rotation="{rot}" android:pivotX="{X}" android:pivotY="{Y}"><path android:fillColor="#FFFFFF" android:pathData="{epath(X, Y, rx, ry)}"/></group>')
    if not mono:
        for x, y, r, c in [(-24, -16, 5.5, "#FF6FAE"), (24, -16, 5.5, "#FF6FAE"), (-16, 12, 4, "#FFC83D"), (16, 12, 4, "#FFC83D")]:
            p.append(f'  <path android:fillColor="{c}" android:pathData="{epath(54+x, 52+y, r, r)}"/>')
    body = "#FFFFFF" if mono else "#3A2A2E"
    p.append(f'  <path android:fillColor="{body}" android:pathData="M51.5,34.5a2.5,2.5 0 0,1 5,0v35a2.5,2.5 0 0,1 -5,0z"/>')
    p.append(f'  <path android:strokeColor="{body}" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M53,33Q46,22 42,21M55,33Q62,22 66,21"/>')
    p.append('</vector>')
    return "\n".join(p) + "\n"
res = os.path.join(ROOT, "android", "app", "src", "main", "res", "drawable")
os.makedirs(res, exist_ok=True)
open(os.path.join(res, "ic_launcher_foreground.xml"), "w").write(vector(False))
open(os.path.join(res, "ic_launcher_monochrome.xml"), "w").write(vector(True))
print("art written")
