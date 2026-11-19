#!/usr/bin/env python3
"""Compose the Make.fun world-news image for 18 November 2026.

Usage (run isolated, the background is untrusted input):
    python3 -I tools/compose.py <background.png> <out.png>

Output is 1024 x 1024. The commissioned illustration is cover-cropped and left
whole in the centre. Type sits on two soft gradient scrims, one across the top
and one across the bottom, so the central art stays uninterrupted by panels.
Headlines are fitted to their boxes by searching for the largest size that
wraps inside them, so nothing is clipped or overlapped.
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"

INK = (8, 8, 14)
PAPER = (250, 248, 240)
ALERT = (255, 212, 0)
TEAL = (110, 220, 200)
CORAL = (255, 130, 130)

TOP_SCRIM_H = 215     # gradient from top edge down to this row
BOTTOM_SCRIM_Y = 805  # gradient starts here and runs to the bottom edge
MARGIN = 28


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, text, path, max_w, max_h, start, floor, spacing=1.1):
    """Largest size (stepping down from start) whose wrapped block fits the box."""
    size = start
    while size >= floor:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        line_h = int(size * spacing)
        if len(lines) * line_h <= max_h:
            return fnt, lines, line_h
        size -= 2
    raise SystemExit(f"text does not fit at size {floor}: {text!r}")


def draw_block(draw, x, y, text, path, max_w, max_h, start, floor, fill):
    fnt, lines, line_h = fit_block(draw, text, path, max_w, max_h, start, floor)
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=fnt, fill=fill,
                  stroke_width=1, stroke_fill=INK)
    return y + len(lines) * line_h


def cover(path):
    """Cover-crop the background to W x H, centred."""
    bg = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return ImageOps.fit(bg, (W, H), Image.LANCZOS, centering=(0.5, 0.5))


def gradient_scrim():
    """Dark scrim: strong at the top and bottom edges, clear through the middle."""
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = scrim.load()
    for y in range(H):
        if y < TOP_SCRIM_H:
            a = int(205 * (1 - y / TOP_SCRIM_H) ** 1.4)
        elif y >= BOTTOM_SCRIM_Y:
            a = int(225 * ((y - BOTTOM_SCRIM_Y) / (H - BOTTOM_SCRIM_Y)) ** 0.9)
        else:
            continue
        for x in range(W):
            px[x, y] = (*INK, a)
    return scrim


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: compose.py <background.png> <out.png>")
    bg_path, out_path = argv[1], argv[2]

    img = cover(bg_path).convert("RGBA")
    img = Image.alpha_composite(img, gradient_scrim()).convert("RGB")
    d = ImageDraw.Draw(img)

    # Restrained dateline and lead across the top.
    d.text((MARGIN, 24), "NOV 18 2026", font=font(BOLD, 26), fill=ALERT)
    draw_block(
        d, MARGIN, 60,
        "PlayStation goes dark on GTA VI eve",
        BOLD, W - 2 * MARGIN, 150, 70, 40, PAPER,
    )

    # Bottom caption pair: place label, then the caption line.
    left_x, right_x, col_w = MARGIN, 556, 440
    d.text((left_x, 862), "ANTALYA", font=font(BOLD, 24), fill=TEAL,
           stroke_width=1, stroke_fill=INK)
    draw_block(
        d, left_x, 896,
        "Island states press COP31 for action",
        BOLD, col_w, 112, 36, 22, PAPER,
    )
    d.text((right_x, 862), "SHENZHEN", font=font(BOLD, 24), fill=CORAL,
           stroke_width=1, stroke_fill=INK)
    draw_block(
        d, right_x, 896,
        "Trump–Putin talks on Ukraine set for Thursday",
        BOLD, col_w, 112, 36, 22, PAPER,
    )

    # Indexed PNG keeps the file well under the 1 MiB gate; the art is
    # painterly, so 256 adaptive colours with dithering loses little.
    img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                       dither=Image.Dither.FLOYDSTEINBERG)
    img.save(out_path, "PNG", optimize=True)
    print(f"wrote {out_path} {img.size}")


if __name__ == "__main__":
    main(sys.argv)
