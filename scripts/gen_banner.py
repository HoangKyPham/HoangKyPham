import math, random
from PIL import Image, ImageDraw, ImageFont

W, H, SCALE = 320, 82, 5
FRAMES, DUR = 28, 110
rnd = random.Random(20251009)

SKY_TOP, SKY_HZ = (8, 12, 26), (38, 60, 96)
L_FAR, L_MID, L_NEAR = (34, 50, 86), (24, 36, 65), (15, 22, 42)
DESK, DESK_TOP = (9, 12, 21), (24, 32, 52)
WARM, WARM2, COOL = (244, 203, 126), (230, 164, 92), (116, 184, 220)
ACCENT, TEXT, SCREEN = (88, 166, 255), (233, 240, 246), (14, 34, 58)

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

stars = [(rnd.randrange(W), rnd.randrange(2, 46), rnd.random() * math.tau) for _ in range(85)]

def skyline(seed, base, lo, hi, wmin, wmax, step):
    r, x, out = random.Random(seed), -5, []
    while x < W + 6:
        bw, bh = r.randrange(wmin, wmax), r.randrange(lo, hi)
        win = [(wx, wy, r.random() < .22, r.random())
               for wy in range(base - bh + 3, base - 2, step)
               for wx in range(x + 2, x + bw - 2, 3) if r.random() < .40]
        out.append((x, base - bh, bw, bh, win)); x += bw + r.randrange(1, 3)
    return out

far  = skyline(1, 62, 16, 34, 10, 20, 4)
mid  = skyline(2, 66, 12, 26, 13, 23, 4)
near = skyline(3, 70, 8, 18, 16, 28, 5)

def mask_text(txt, px):
    f = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", px)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).text((0, 0), txt, font=f, fill=255)
    return m.point(lambda v: 255 if v > 100 else 0), f.getbbox(txt)[2]

m_name, w_name = mask_text("Hoang Ky Pham", 15)
m_sub,  w_sub  = mask_text("FULLSTACK WEB DEVELOPER", 11)

def frame(t):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(SKY_TOP, SKY_HZ, min(1, (y / 70) ** 1.35)))

    for sx, sy, ph in stars:
        b = .40 + .60 * (.5 + .5 * math.sin(ph + t * math.tau * 2))
        d.point((sx, sy), fill=lerp(SKY_TOP, (210, 229, 255), b))

    for r_, a in ((11, .10), (9, .18), (7, .30)):                      # moon halo
        d.ellipse([293 - r_, 16 - r_, 293 + r_, 16 + r_], fill=lerp(SKY_TOP, (120, 150, 200), a))
    d.ellipse([288, 11, 298, 21], fill=(234, 240, 248))
    d.ellipse([294, 13, 297, 16], fill=(205, 214, 230))

    for layer, col in ((far, L_FAR), (mid, L_MID), (near, L_NEAR)):
        for bx, by, bw, bh, win in layer:
            d.rectangle([bx, by, bx + bw, by + bh], fill=col)
            d.line([(bx, by), (bx + bw, by)], fill=lerp(col, SKY_HZ, .35))
            for wx, wy, cool, ph in win:
                if math.sin(ph * 31.4 + t * math.tau) > -.80:
                    d.point((wx, wy), fill=COOL if cool else (WARM if ph < .5 else WARM2))

    gl = .55 + .45 * math.sin(t * math.tau * 2)
    d.rectangle([0, 70, W, H], fill=DESK)                              # desk slab
    d.line([(0, 70), (W, 70)], fill=DESK_TOP)
    for i in range(40):                                                # light pool on desk
        a = (1 - abs(i - 20) / 20) * .30 * gl
        d.point((242 + i, 71), fill=lerp(DESK, (40, 86, 140), a))
        d.point((242 + i, 72), fill=lerp(DESK, (34, 72, 118), a * .6))

    for r_ in range(18, 3, -3):                                        # monitor bloom
        d.ellipse([262 - r_ * 1.7, 54 - r_, 262 + r_ * 1.7, 54 + r_],
                  fill=lerp(DESK, (30, 64, 104), .13 * gl * (1 - r_ / 20)))
    d.rectangle([236, 36, 288, 66], fill=(17, 23, 40))
    d.rectangle([238, 38, 286, 64], fill=SCREEN)
    for i in range(7):
        ly = 40 + ((i * 4 + int(t * 28)) % 24)
        if 40 <= ly <= 62:
            d.line([(241, ly), (241 + [30, 17, 25, 11, 28, 20, 14][i], ly)],
                   fill=lerp(SCREEN, ACCENT, .60))
    if int(t * 28) % 14 < 7:
        d.rectangle([241, 60, 243, 62], fill=(132, 236, 236))
    d.rectangle([259, 66, 265, 70], fill=(17, 23, 40))                 # stand

    d.ellipse([255, 43, 269, 57], fill=(6, 9, 17))                     # head
    d.polygon([(247, 82), (251, 57), (273, 57), (277, 82)], fill=(6, 9, 17))
    d.rectangle([243, 73, 281, 76], fill=(21, 28, 46))                 # keyboard
    d.rectangle([228, 71, 234, 77], fill=(30, 40, 62))                 # mug
    d.rectangle([226, 73, 228, 75], fill=(30, 40, 62))

    d.polygon([(203, 70), (205, 59), (215, 59), (217, 70)], fill=(44, 30, 23))  # pot
    for cx, cy, r_ in ((210, 53, 6), (205, 49, 4), (215, 50, 4), (210, 45, 4)):
        d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(36, 92, 68))
        d.ellipse([cx - r_ + 1, cy - r_ + 1, cx, cy], fill=(48, 114, 84))

    lx, by_ = 304, 63 - 9 * (.5 + .5 * math.sin(t * math.tau))        # lava lamp
    for r_ in (7, 5, 3):
        d.ellipse([lx - r_, 55 - r_, lx + r_, 55 + r_], fill=lerp(DESK, (120, 40, 70), .22))
    d.rectangle([lx - 4, 45, lx + 4, 67], fill=(22, 28, 46))
    d.rectangle([lx - 3, 47, lx + 3, 66], fill=(52, 26, 44))
    d.ellipse([lx - 2, by_ - 3, lx + 2, by_ + 3], fill=(255, 98, 146))
    d.rectangle([lx - 5, 67, lx + 5, 70], fill=(16, 21, 36))

    img.paste(TEXT, (14, 18), m_name)
    d.rectangle([15, 38, 15 + w_sub, 39], fill=lerp(SKY_HZ, ACCENT, .85))
    img.paste(ACCENT, (15, 42), m_sub)

    big = img.resize((W * SCALE, H * SCALE), Image.NEAREST).convert("RGBA")
    ov = Image.new("RGBA", big.size, (0, 0, 0, 0))                     # soft lofi scanlines
    od = ImageDraw.Draw(ov)
    for y in range(0, H * SCALE, 5):
        od.line([(0, y), (W * SCALE, y)], fill=(0, 0, 0, 26))
    return Image.alpha_composite(big, ov).convert("RGB")

frames = [frame(i / FRAMES) for i in range(FRAMES)]
master = frames[0].quantize(colors=96, method=Image.MEDIANCUT)
pal = [f.quantize(palette=master, dither=Image.NONE) for f in frames]
out = "banner.gif"
pal[0].save(out, save_all=True, append_images=pal[1:], duration=DUR, loop=0, optimize=True, disposal=2)
print("written")
