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

AVATAR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" role="img" aria-labelledby="t d">
<title id="t">Megha Pashupati</title>
<desc id="d">Illustrated portrait of Megha: an oval face with a calm closed-lip smile, almond brown eyes, arched brows, long straight black hair parted slightly to one side and falling past her shoulders, tucked behind one ear with a small stud earring, wearing a black-and-white houndstooth top, in a sunlit garden circle with tiny butterflies.</desc>
<style>
.bf{animation:fl 7s ease-in-out infinite} @keyframes fl{0%,100%{transform:translate(0,0)}50%{transform:translate(10px,-12px)}}
.wl,.wr{transform-box:fill-box;animation:flap .32s ease-in-out infinite alternate} .wl{transform-origin:right center} .wr{transform-origin:left center}
@keyframes flap{to{transform:scaleX(.35)}}
.head{transform-origin:220px 330px;animation:tilt 7s ease-in-out infinite} @keyframes tilt{0%,100%{transform:rotate(0)}50%{transform:rotate(1.6deg)}}
.eyes{transform-box:fill-box;transform-origin:center;animation:blink 6s infinite} @keyframes blink{0%,94%,100%{transform:scaleY(1)}96.5%{transform:scaleY(.1)}}
.bk{animation:tw 4s ease-in-out infinite} @keyframes tw{0%,100%{opacity:.25}50%{opacity:.75}}
.ring{animation:hue 14s linear infinite} @keyframes hue{to{filter:hue-rotate(360deg)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
</style>
<defs>
  <radialGradient id="sky" cx="45%" cy="35%" r="70%"><stop offset="0" stop-color="#FFF6D6"/><stop offset=".45" stop-color="#DCEFC0"/><stop offset="1" stop-color="#7FBF8A"/></radialGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFC83D"/><stop offset=".35" stop-color="#FF6FAE"/><stop offset=".7" stop-color="#9B7BFF"/><stop offset="1" stop-color="#3FD6A6"/></linearGradient>
  <radialGradient id="skin" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#EDC6A5"/><stop offset=".45" stop-color="#DBAA87"/><stop offset=".8" stop-color="#C6906D"/><stop offset="1" stop-color="#A6714F"/></radialGradient>
  <linearGradient id="neck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9765A"/><stop offset=".5" stop-color="#CF9E7D"/><stop offset="1" stop-color="#DDB08F"/></linearGradient>
  <linearGradient id="hair" x1="0" y1="0" x2=".5" y2="1"><stop offset="0" stop-color="#3B3236"/><stop offset=".35" stop-color="#1C1619"/><stop offset="1" stop-color="#0C090B"/></linearGradient>
  <linearGradient id="hairfront" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2E262A"/><stop offset=".5" stop-color="#17121500"/><stop offset="1" stop-color="#0B080A"/></linearGradient>
  <radialGradient id="iris" cx="45%" cy="35%" r="65%"><stop offset="0" stop-color="#7A4C30"/><stop offset=".65" stop-color="#43261A"/><stop offset="1" stop-color="#1F110A"/></radialGradient>
  <linearGradient id="lipT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B66476"/><stop offset="1" stop-color="#A4586A"/></linearGradient>
  <linearGradient id="lipB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D88E9C"/><stop offset="1" stop-color="#C27684"/></linearGradient>
  <pattern id="hound" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-6)">
    <rect width="14" height="14" fill="#17161C"/>
    <path d="M0 0H7L14 7V14L7 7H0Z" fill="#F3F0E8"/><path d="M0 7H3.5V10.5Z" fill="#F3F0E8"/><path d="M7 0V3.5H10.5Z" fill="#17161C"/>
  </pattern>
  <radialGradient id="topshade" cx="50%" cy="10%" r="95%"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>
  <clipPath id="eyeL"><path d="M177 203C183 195 200 194 207 202C201 207 186 208 177 203Z"/></clipPath>
  <clipPath id="eyeR"><path d="M263 203C257 195 240 194 233 202C239 207 254 208 263 203Z"/></clipPath>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#2D4B2F" flood-opacity=".35"/></filter>
  <filter id="blur2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.4"/></filter>
  <filter id="blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
  <clipPath id="disc"><circle cx="220" cy="220" r="200"/></clipPath>
</defs>

<circle cx="220" cy="220" r="214" fill="none" stroke="url(#rim)" stroke-width="12" opacity=".7" filter="url(#glow)" class="ring"/>
<circle cx="220" cy="220" r="206" fill="none" stroke="url(#rim)" stroke-width="6" class="ring"/>
<circle cx="220" cy="220" r="200" fill="url(#sky)"/>
<g clip-path="url(#disc)">
  <!-- sunlit garden bokeh -->
  %BOKEH%
  <path d="M20 120C60 90 70 40 40 10M410 90C380 70 380 30 410 10" stroke="#5E9E62" stroke-width="10" fill="none" opacity=".35" stroke-linecap="round"/>
  <!-- long hair, behind -->
  <path d="M220 80C152 82 112 126 108 192C104 258 100 330 88 440H352C340 330 336 258 332 192C328 126 290 82 220 80Z" fill="url(#hair)"/>
  <!-- neck and shoulders in a houndstooth top -->
  <path d="M194 276C195 298 193 314 188 330H252C247 314 245 298 246 276Z" fill="url(#neck)"/>
  <ellipse cx="220" cy="298" rx="30" ry="10" fill="#8F5E44" opacity=".45" filter="url(#blur2)"/>
  <g filter="url(#soft)">
    <path d="M70 440C74 392 104 362 150 350C170 345 182 336 190 326C202 338 238 338 250 326C258 336 270 345 290 350C336 362 366 392 370 440Z" fill="url(#hound)"/>
    <path d="M70 440C74 392 104 362 150 350C170 345 182 336 190 326C202 338 238 338 250 326C258 336 270 345 290 350C336 362 366 392 370 440Z" fill="url(#topshade)"/>
    <path d="M190 326C202 339 238 339 250 326" fill="none" stroke="#0E0D12" stroke-width="3.5" stroke-linecap="round"/>
  </g>
</g>

<g clip-path="url(#disc)"><g class="head" filter="url(#soft)">
  <!-- ear (her left) with a small stud -->
  <path d="M289 208C298 203 305 212 304 225C303 238 298 247 291 249Z" fill="#CC9673"/>
  <path d="M293 216C298 216 299 226 296 234" fill="none" stroke="#A9725A" stroke-width="1.6" opacity=".7"/>
  <circle cx="295.5" cy="246.5" r="2.8" fill="#F4EBDA"/><circle cx="294.6" cy="245.6" r="1" fill="#FFFFFF"/>
  <!-- face -->
  <path d="M150 198C148 150 180 116 220 116C260 116 292 150 290 198C289 238 276 268 256 285C245 294 233 299 220 299C207 299 195 294 184 285C164 268 151 238 150 198Z" fill="url(#skin)"/>
  <path d="M282 214C278 250 262 276 238 292" fill="none" stroke="#9C6A50" stroke-width="10" opacity=".22" stroke-linecap="round" filter="url(#blur2)"/>
  <path d="M160 220C164 252 180 276 202 290" fill="none" stroke="#FFE9D8" stroke-width="6" opacity=".2" stroke-linecap="round" filter="url(#blur2)"/>
  <ellipse cx="208" cy="146" rx="28" ry="11" fill="#FFFFFF" opacity=".13" filter="url(#blur2)"/>
  <ellipse cx="178" cy="234" rx="18" ry="10" fill="#E8897E" opacity=".24" filter="url(#blur2)"/>
  <ellipse cx="262" cy="234" rx="18" ry="10" fill="#E8897E" opacity=".24" filter="url(#blur2)"/>
  <!-- brows -->
  <path d="M168 187C176 178.5 194 176.5 209 179.5C209 183.5 207 185 204 185C194 182 182 183 170 190Z" fill="#20130F"/>
  <path d="M272 187C264 178.5 246 176.5 231 179.5C231 183.5 233 185 236 185C246 182 258 183 270 190Z" fill="#20130F"/>
  <!-- almond eyes with a soft upper lid -->
  <g class="eyes">
    <path d="M177 203C183 195 200 194 207 202C201 207 186 208 177 203Z" fill="#FAF4EF"/>
    <path d="M263 203C257 195 240 194 233 202C239 207 254 208 263 203Z" fill="#FAF4EF"/>
    <g clip-path="url(#eyeL)"><circle cx="192.5" cy="202.5" r="6.3" fill="url(#iris)"/><circle cx="192.5" cy="202.5" r="2.9" fill="#0E0705"/>
      <path d="M175 197.5C184 195.5 200 195 210 199V193H175Z" fill="#B98364" opacity=".5"/></g>
    <g clip-path="url(#eyeR)"><circle cx="247.5" cy="202.5" r="6.3" fill="url(#iris)"/><circle cx="247.5" cy="202.5" r="2.9" fill="#0E0705"/>
      <path d="M265 197.5C256 195.5 240 195 230 199V193H265Z" fill="#B98364" opacity=".5"/></g>
    <circle cx="194.6" cy="200.6" r="1.8" fill="#FFFFFF" opacity=".95"/><circle cx="249.6" cy="200.6" r="1.8" fill="#FFFFFF" opacity=".95"/>
    <path d="M175.5 203C182 193.5 201 192.5 208.5 201.5" fill="none" stroke="#170D0A" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M264.5 203C258 193.5 239 192.5 231.5 201.5" fill="none" stroke="#170D0A" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M180 206C187 209 199 208.5 205 204.5M260 206C253 209 241 208.5 235 204.5" fill="none" stroke="#9E6B54" stroke-width="1.2" opacity=".6" stroke-linecap="round"/>
    <path d="M180 195C187 189.5 199 189 206 193M260 195C253 189.5 241 189 234 193" fill="none" stroke="#A9765C" stroke-width="1.3" opacity=".45" stroke-linecap="round"/>
  </g>
  <!-- straight nose -->
  <path d="M226 204C227 218 228 230 232 238" fill="none" stroke="#A06C52" stroke-width="3.4" opacity=".28" stroke-linecap="round" filter="url(#blur2)"/>
  <ellipse cx="220" cy="238" rx="5" ry="3.6" fill="#FFFFFF" opacity=".2"/>
  <path d="M207 244C212 250 217.5 251 220.5 250C223.5 251 229 250 234 244" fill="none" stroke="#956049" stroke-width="1.9" opacity=".75" stroke-linecap="round"/>
  <ellipse cx="212" cy="245.5" rx="3.4" ry="1.8" fill="#7E4E3C" opacity=".35"/><ellipse cx="229" cy="245.5" rx="3.4" ry="1.8" fill="#7E4E3C" opacity=".35"/>
  <!-- calm closed-lip smile -->
  <path d="M196 266C204 261.5 212 258 218.5 260C219.8 260.8 220.5 261 221 261C221.5 261 222.2 260.8 223.5 260C230 258 238 261.5 246 266C235 269 207 269 196 266Z" fill="url(#lipT)"/>
  <path d="M198 267C207 280 235 280 244 267C235 270.5 207 270.5 198 267Z" fill="url(#lipB)"/>
  <path d="M196 266Q221 271.5 246 266" fill="none" stroke="#7E3646" stroke-width="1.7" stroke-linecap="round"/>
  <ellipse cx="221" cy="274.5" rx="8" ry="1.8" fill="#FFFFFF" opacity=".3"/>
  <path d="M193 263.5Q195 266.5 197.5 266.8M249 263.5Q247 266.5 244.5 266.8" fill="none" stroke="#A86A5E" stroke-width="1.4" opacity=".6" stroke-linecap="round"/>
  <!-- front hair: parted slightly to her right, falling straight down past the shoulders -->
  <path d="M210 86C174 88 140 112 129 156C118 202 118 258 122 312C126 362 132 404 136 440H176C170 404 166 360 164 318C162 284 158 252 157 224C156 190 162 160 176 138C188 122 200 112 210 104Z" fill="url(#hair)"/>
  <path d="M210 86C250 82 288 100 302 138C308 156 308 178 303 204C298 184 292 168 284 156C272 136 250 122 226 116C218 114 213 110 210 104Z" fill="url(#hair)"/>
  <path d="M210 86C209 93 209 99 210 106" fill="none" stroke="#6E5C62" stroke-width="1.6" opacity=".8"/>
  <path d="M204 92C176 100 152 122 144 164C138 198 138 250 142 310C145 356 150 400 154 440M194 96C170 108 152 134 146 172M218 92C248 92 276 106 290 130M222 102C246 104 268 116 280 132" fill="none" stroke="#4C3E44" stroke-width="1.3" opacity=".7"/>
  <path d="M216 90C244 88 272 98 288 118" fill="none" stroke="#FFFFFF" stroke-width="5" opacity=".13" stroke-linecap="round"/>
  <path d="M190 98C170 108 154 130 146 160" fill="none" stroke="#FFFFFF" stroke-width="4" opacity=".1" stroke-linecap="round"/>
  <path d="M302 204C308 240 312 284 318 334" fill="none" stroke="#0E0A0C" stroke-width="10" opacity=".9" stroke-linecap="round"/>
</g></g>

%BUTTERFLIES%
</svg>"""

def _bokeh():
    out = []
    for i in range(16):
        x, y, r = random.uniform(30, 410), random.uniform(30, 300), random.uniform(6, 22)
        c = random.choice(["#FFFFFF", "#FFF2B0", "#E8FFD0", "#FFE0EE"])
        out.append(f'<circle class="bk" style="animation-delay:{random.uniform(0, 4):.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" opacity=".5" filter="url(#blur6)"/>')
    return "".join(out)

avatar = (AVATAR.replace("%BOKEH%", _bokeh())
          .replace("%BUTTERFLIES%", butterfly(76, 120, 1.25, "#FF6FAE", "#FFC83D", delay=0) +
                   butterfly(372, 170, 1.0, "#9B7BFF", "#3FD6A6", delay=1.5) +
                   butterfly(352, 330, 0.85, "#FFC83D", "#FF6FAE", delay=2.6)))
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
