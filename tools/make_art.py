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

# ── Megha: a stylised 3D-shaded portrait (fresh design) ─────────────────────
def _eye(cx, cy, side, clip_id):
    """side=-1: outer corner to the left (her right eye); side=+1: outer corner to the right."""
    k = 0.92
    X = lambda x: f"{cx + side * x * k:.1f}"
    Y = lambda y: f"{cy + y * k:.1f}"
    shape = f"M{X(-15)} {Y(1)}C{X(-11)} {Y(-10)} {X(10)} {Y(-12)} {X(15)} {Y(0)}C{X(10)} {Y(7)} {X(-9)} {Y(8)} {X(-15)} {Y(1)}Z"
    return (f'<clipPath id="{clip_id}"><path d="{shape}"/></clipPath>',
            f'<path d="{shape}" fill="#FCF8F5"/>'
            f'<g clip-path="url(#{clip_id})">'
            f'<circle cx="{X(0.5)}" cy="{Y(-0.5)}" r="8.3" fill="url(#iris)"/>'
            f'<circle cx="{X(0.5)}" cy="{Y(-0.5)}" r="8.3" fill="none" stroke="#1A0D07" stroke-width="1.1" opacity=".7"/>'
            f'<circle cx="{X(0.5)}" cy="{Y(-0.5)}" r="3.9" fill="#0B0503"/>'
            f'<path d="M{X(-18)} {Y(-14)}H{X(18)}V{Y(-4)}C{X(8)} {Y(-8)} {X(-8)} {Y(-8)} {X(-18)} {Y(-4)}Z" fill="#7A4A3A" opacity=".28"/></g>'
            f'<circle cx="{X(3.6)}" cy="{Y(-4.4)}" r="2.7" fill="#FFFFFF"/><circle cx="{X(-2.6)}" cy="{Y(3)}" r="1.15" fill="#FFFFFF" opacity=".85"/>'
            f'<path d="M{X(-16)} {Y(1)}C{X(-11)} {Y(-11.5)} {X(10)} {Y(-13.5)} {X(16.5)} {Y(-0.5)}" fill="none" stroke="#140A08" stroke-width="3.3" stroke-linecap="round"/>'
            f'<path d="M{X(16.5)} {Y(-0.5)}Q{X(19.5)} {Y(-2.5)} {X(21.5)} {Y(-5)}M{X(13)} {Y(-5.5)}Q{X(15)} {Y(-8)} {X(16)} {Y(-10.5)}" fill="none" stroke="#140A08" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M{X(-12)} {Y(-9)}C{X(-6)} {Y(-16)} {X(9)} {Y(-17)} {X(14)} {Y(-10)}" fill="none" stroke="#B07A60" stroke-width="1.3" opacity=".55" stroke-linecap="round"/>'
            f'<path d="M{X(-12)} {Y(4.5)}C{X(-5)} {Y(9.5)} {X(7)} {Y(9.5)} {X(13)} {Y(3.5)}" fill="none" stroke="#B9806A" stroke-width="1.1" opacity=".5" stroke-linecap="round"/>')

def _brow(cx, cy, side):
    X = lambda x: f"{cx + side * x:.1f}"
    Y = lambda y: f"{cy + y + 3:.1f}"
    return (f'<path d="M{X(-15)} {Y(-19)}C{X(-8)} {Y(-26)} {X(8)} {Y(-29)} {X(19)} {Y(-22)}C{X(18)} {Y(-19.8)} {X(16)} {Y(-19.6)} {X(14)} {Y(-20.5)}'
            f'C{X(6)} {Y(-24.5)} {X(-6)} {Y(-22.5)} {X(-13)} {Y(-16.5)}Z" fill="#2A1813"/>')

def _bokeh_vesicles():
    out = []
    cols = ["#FFFFFF", "#FFE7A8", "#FFC4DD", "#CDBBFF", "#B8F0DC"]
    for i in range(15):
        x, y, r = random.uniform(30, 410), random.uniform(40, 330), random.uniform(5, 16)
        c = random.choice(cols)
        out.append(f'<g class="bk" style="animation-delay:{random.uniform(0, 5):.1f}s"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 1.8:.0f}" fill="url(#bokeh)" opacity=".55"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="1.4" opacity=".8"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * .62:.0f}" fill="none" stroke="{c}" stroke-width=".9" opacity=".7"/></g>')
    return "".join(out)

eyeL_clip, eyeL = _eye(196, 204, -1, "eyeL")
eyeR_clip, eyeR = _eye(244, 204, +1, "eyeR")

avatar = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" role="img" aria-labelledby="t d">
<title id="t">Megha Pashupati</title>
<desc id="d">Illustrated 3D-style portrait of Megha: long glossy black hair parted in the middle, warm brown eyes, a gentle smile, wearing a white lab coat over a sunflower-yellow top with a small name badge, in a dreamy circle of glowing vesicles, fluorescent muscle fibres and tiny butterflies.</desc>
<style>
.bf{animation:fl 7s ease-in-out infinite} @keyframes fl{0%,100%{transform:translate(0,0)}50%{transform:translate(10px,-12px)}}
.wl,.wr{transform-box:fill-box;animation:flap .32s ease-in-out infinite alternate} .wl{transform-origin:right center} .wr{transform-origin:left center}
@keyframes flap{to{transform:scaleX(.35)}}
.who{transform-origin:220px 330px;animation:tilt 8s ease-in-out infinite} @keyframes tilt{0%,100%{transform:rotate(-2.5deg)}50%{transform:rotate(-0.5deg)}}
.eyes{transform-box:fill-box;transform-origin:center;animation:blink 6s infinite} @keyframes blink{0%,94%,100%{transform:scaleY(1)}96.5%{transform:scaleY(.1)}}
.lockL{transform-origin:196px 110px;animation:swayL 6s ease-in-out infinite} @keyframes swayL{50%{transform:rotate(1.2deg)}}
.lockR{transform-origin:244px 110px;animation:swayR 6s ease-in-out infinite} @keyframes swayR{50%{transform:rotate(-1.2deg)}}
.bk{animation:tw 5s ease-in-out infinite} @keyframes tw{0%,100%{opacity:.45}50%{opacity:1}}
.ring{animation:hue 14s linear infinite} @keyframes hue{to{filter:hue-rotate(360deg)}}
.sp{animation:tw 3s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
</style>
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE3C8"/><stop offset=".45" stop-color="#FFF3EA"/><stop offset=".75" stop-color="#E7DBFF"/><stop offset="1" stop-color="#C9F1E2"/></linearGradient>
  <radialGradient id="flare" cx="78%" cy="20%" r="40%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
  <radialGradient id="bokeh"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".7"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFC83D"/><stop offset=".35" stop-color="#FF6FAE"/><stop offset=".7" stop-color="#9B7BFF"/><stop offset="1" stop-color="#3FD6A6"/></linearGradient>
  <radialGradient id="skin" cx="42%" cy="34%" r="76%"><stop offset="0" stop-color="#FBDCC6"/><stop offset=".42" stop-color="#EEC2A2"/><stop offset=".78" stop-color="#DDA683"/><stop offset="1" stop-color="#C38864"/></radialGradient>
  <linearGradient id="neck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B98062"/><stop offset=".55" stop-color="#DDA784"/><stop offset="1" stop-color="#E9BB9A"/></linearGradient>
  <linearGradient id="hair" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#3A2C2E"/><stop offset=".3" stop-color="#1E1517"/><stop offset="1" stop-color="#0B0708"/></linearGradient>
  <linearGradient id="gloss" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFE9F2" stop-opacity=".55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
  <radialGradient id="iris" cx="50%" cy="62%" r="60%"><stop offset="0" stop-color="#A8704A"/><stop offset=".55" stop-color="#5A321D"/><stop offset="1" stop-color="#24120A"/></radialGradient>
  <linearGradient id="lipT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C85E73"/><stop offset="1" stop-color="#B24F65"/></linearGradient>
  <linearGradient id="lipB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E28A9A"/><stop offset="1" stop-color="#CC6F82"/></linearGradient>
  <linearGradient id="coat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#EEF0F6"/><stop offset="1" stop-color="#D5D9E6"/></linearGradient>
  <linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD54A"/><stop offset="1" stop-color="#F0A800"/></linearGradient>
  """ + eyeL_clip + eyeR_clip + """
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#5B3A6B" flood-opacity=".28"/></filter>
  <filter id="blur2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.4"/></filter>
  <filter id="blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
  <clipPath id="disc"><circle cx="220" cy="220" r="200"/></clipPath>
</defs>

<circle cx="220" cy="220" r="214" fill="none" stroke="url(#rim)" stroke-width="12" opacity=".7" filter="url(#glow)" class="ring"/>
<circle cx="220" cy="220" r="206" fill="none" stroke="url(#rim)" stroke-width="6" class="ring"/>
<circle cx="220" cy="220" r="200" fill="url(#sky)"/>
<g clip-path="url(#disc)">
  <circle cx="220" cy="220" r="200" fill="url(#flare)"/>
  <!-- faint fluorescent muscle fibres, like a confocal image -->
  <path d="M10 300C90 270 150 290 210 260M10 330C80 310 140 330 200 300M430 250C360 230 300 250 250 228M430 290C370 280 320 300 270 280" stroke="#FF8FC0" stroke-width="7" fill="none" opacity=".22" stroke-linecap="round" filter="url(#blur2)"/>
  <path d="M20 360C100 340 150 360 210 335M420 330C360 318 310 335 260 320" stroke="#7FE0B5" stroke-width="6" fill="none" opacity=".2" stroke-linecap="round" filter="url(#blur2)"/>
  """ + _bokeh_vesicles() + """
  <g class="who" filter="url(#soft)">
    <!-- long hair, behind -->
    <path d="M220 80C154 82 120 128 118 194C116 254 122 296 112 340C104 380 106 410 96 440H344C334 410 336 380 328 340C318 296 324 254 322 194C320 128 286 82 220 80Z" fill="url(#hair)"/>
    <!-- neck -->
    <path d="M204 266C205 288 203 306 198 322H242C237 306 235 288 236 266Z" fill="url(#neck)"/>
    <ellipse cx="220" cy="284" rx="22" ry="9" fill="#9A6248" opacity=".42" filter="url(#blur2)"/>
    <!-- sunflower-yellow top and a white lab coat -->
    <path d="M178 330C196 322 210 318 220 318C230 318 244 322 262 330L270 440H170Z" fill="url(#top)"/>
    <path d="M196 320C206 334 234 334 244 320" fill="none" stroke="#D99400" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M206 298C212 312 228 312 234 298" fill="none" stroke="#E9B949" stroke-width="1.4"/><circle cx="220" cy="309" r="2.6" fill="#F6CF5C" stroke="#C99A2A" stroke-width=".8"/>
    <path d="M52 440C56 386 92 352 146 338L192 322L176 352L190 384L178 440Z" fill="url(#coat)"/>
    <path d="M388 440C384 386 348 352 294 338L248 322L264 352L250 384L262 440Z" fill="url(#coat)"/>
    <path d="M192 322L176 352L190 384L198 352ZM248 322L264 352L250 384L242 352Z" fill="#E3E6EF" stroke="#C9CDDA" stroke-width="1"/>
    <path d="M146 338C140 370 138 404 140 440M294 338C300 370 302 404 300 440" fill="none" stroke="#C9CDDA" stroke-width="1.4"/>
    <rect x="270" y="384" width="54" height="17" rx="4" fill="#FFFFFF" stroke="#9B7BFF" stroke-width="1.4"/>
    <text x="297" y="396.5" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="10" font-weight="700" fill="#6B3FD4">Megha</text>
    <!-- face -->
    <path d="M156 194C156 148 186 122 220 122C254 122 284 148 284 194C284 232 272 258 254 273C243 282 232 287 220 287C208 287 197 282 186 273C168 258 156 232 156 194Z" fill="url(#skin)"/>
    <path d="M272 200C270 236 258 262 236 280" fill="none" stroke="#FFE7D8" stroke-width="4" opacity=".45" stroke-linecap="round" filter="url(#blur2)"/>
    <path d="M168 210C172 240 186 264 206 280" fill="none" stroke="#B57352" stroke-width="9" opacity=".2" stroke-linecap="round" filter="url(#blur2)"/>
    <ellipse cx="212" cy="156" rx="22" ry="9" fill="#FFFFFF" opacity=".16" filter="url(#blur2)"/>
    <ellipse cx="184" cy="234" rx="16" ry="9.5" fill="#FF8A8A" opacity=".3" filter="url(#blur2)"/>
    <ellipse cx="256" cy="234" rx="16" ry="9.5" fill="#FF8A8A" opacity=".3" filter="url(#blur2)"/>
    <ellipse cx="220" cy="279" rx="9" ry="4" fill="#FFFFFF" opacity=".14" filter="url(#blur2)"/>
    """ + _brow(196, 204, -1) + _brow(244, 204, +1) + """
    <g class="eyes">""" + eyeL + eyeR + """</g>
    <!-- small nose -->
    <path d="M223 208C224 220 225 228 228 234" fill="none" stroke="#B5785A" stroke-width="3" opacity=".25" stroke-linecap="round" filter="url(#blur2)"/>
    <path d="M211 237C213.5 243 218 244 220 243C222 244 226.5 243 229 237" fill="none" stroke="#A4664C" stroke-width="1.9" opacity=".75" stroke-linecap="round"/>
    <ellipse cx="214.5" cy="240" rx="2.6" ry="1.5" fill="#8A5040" opacity=".3"/><ellipse cx="225.5" cy="240" rx="2.6" ry="1.5" fill="#8A5040" opacity=".3"/>
    <ellipse cx="219.5" cy="234.5" rx="3.4" ry="2.3" fill="#FFFFFF" opacity=".42"/>
    <!-- gentle smile -->
    <path d="M201.5 257C209 253.6 214.5 251.4 219 253C219.8 253.5 220.2 253.6 220.6 253.6C221 253.6 221.4 253.5 222.2 253C226.5 251.4 232 253.6 239.5 257C230 259.8 211 259.8 201.5 257Z" fill="url(#lipT)"/>
    <path d="M204 258C210.5 267 230.5 267 237 258C230 260.8 211 260.8 204 258Z" fill="url(#lipB)"/>
    <path d="M201 257Q220.5 262 240 257" fill="none" stroke="#8A3448" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M197.5 253.8Q199.5 257.4 202.4 257.6M243.5 253.8Q241.5 257.4 238.6 257.6" fill="none" stroke="#B0675E" stroke-width="1.4" stroke-linecap="round" opacity=".8"/>
    <ellipse cx="220.5" cy="262.6" rx="6" ry="1.6" fill="#FFFFFF" opacity=".4"/>
    <!-- front hair: middle parting, long locks framing the face -->
    <g class="lockL"><path d="M220 90C188 90 160 106 148 140C136 174 137 216 141 258C146 296 139 330 146 362C153 392 141 418 134 440H180C185 414 172 392 172 362C172 330 166 296 165 264C163 236 160 212 161 190C162 166 172 144 190 128C201 119 211 113 220 110Z" fill="url(#hair)"/>
      <path d="M152 200C150 244 152 292 150 344" fill="none" stroke="#FFFFFF" stroke-width="2.4" opacity=".12" stroke-linecap="round"/>
      <path d="M146 186C141 234 143 300 146 362" fill="none" stroke="#000000" stroke-width="1.4" opacity=".35"/></g>
    <g class="lockR"><path d="M220 90C252 90 280 106 292 140C304 174 304 216 300 258C296 288 304 314 300 338C297 356 305 368 313 380L280 374C283 352 271 330 275 304C277 290 275 280 275 268C276 238 280 212 279 190C278 166 268 144 250 128C239 119 229 113 220 110Z" fill="url(#hair)"/>
      <path d="M288 196C291 240 290 284 292 326" fill="none" stroke="#FFFFFF" stroke-width="2.4" opacity=".12" stroke-linecap="round"/>
      <path d="M294 186C299 234 297 300 302 352" fill="none" stroke="#000000" stroke-width="1.4" opacity=".35"/></g>
    <path d="M220 84V110" stroke="#6E5A5E" stroke-width="1.6" opacity=".8"/>
    <path d="M170 132C184 112 202 102 217 100M270 132C256 112 238 102 223 100" fill="none" stroke="url(#gloss)" stroke-width="7" stroke-linecap="round" opacity=".9"/>
  </g>
</g>
""" + butterfly(74, 118, 1.25, "#FF6FAE", "#FFC83D", delay=0) + butterfly(372, 150, 1.0, "#9B7BFF", "#3FD6A6", delay=1.5) + butterfly(366, 328, 0.85, "#FFC83D", "#FF6FAE", delay=2.6) + """
<path class="sp" d="M118 300l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#FFFFFF"/>
<path class="sp" style="animation-delay:1.2s" d="M330 86l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#FFF7C2"/>
</svg>"""
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
