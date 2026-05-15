#!/usr/bin/env python3

import argparse
import csv
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip


FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


PRESETS = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "4k": (3840, 2160),
}


def get_screen_size():
    try:
        from tkinter import Tk

        root = Tk()
        root.withdraw()

        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        root.destroy()

        return w, h

    except:
        return 1920, 1080


def load_font(size):
    for p in FONT_PATHS:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass

    return ImageFont.load_default()


def ask(q, d):
    v = input(f"{q} [{d}]: ").strip()
    return v if v else d


def clean(text):
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def load_file(path):
    ext = path.suffix.lower()

    if ext == ".txt":
        return clean(path.read_text(encoding="utf-8"))

    if ext == ".json":
        return clean(
            json.dumps(
                json.loads(path.read_text()),
                indent=2,
                ensure_ascii=False,
            )
        )

    if ext == ".csv":
        rows = []

        with open(path, encoding="utf-8") as f:
            for r in csv.reader(f):
                rows.append(" | ".join(r))

        return clean("\n".join(rows))

    raise ValueError("Unsupported file")


def find_optimal_font(screen_h):

    target = int(screen_h * 0.8)

    test = "AgÇºªgj"

    for size in range(40, 2000, 5):

        font = load_font(size)

        img = Image.new("RGB", (1000, 1000))
        draw = ImageDraw.Draw(img)

        box = draw.textbbox((0, 0), test, font=font)

        h = box[3] - box[1]

        if h >= target:
            return font

    return load_font(300)


def wrap_text(draw, text, font, width):

    words = text.split()

    lines = []

    current = ""

    for word in words:

        test = (current + " " + word).strip()

        if draw.textlength(test, font=font) <= width:
            current = test

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def build_canvas(
    text,
    w,
    h,
    bg,
    color,
    font,
):

    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)

    lines = wrap_text(
        draw,
        text,
        font,
        int(w * 0.95),
    )

    line_h = font.size + 20

    canvas_h = line_h * len(lines) + h

    canvas = Image.new(
        "RGB",
        (w, canvas_h),
        bg,
    )

    draw = ImageDraw.Draw(canvas)

    y = h // 2

    for line in lines:

        tw = draw.textlength(
            line,
            font=font,
        )

        x = (w - tw) // 2

        draw.text(
            (x, y),
            line,
            font=font,
            fill=color,
        )

        y += line_h

    return np.array(canvas)


def wizard(args):

    print()

    args.mode = ask(
        "Scroll mode (vertical/horizontal)",
        "vertical",
    )

    args.quality = ask(
        "Quality (720p/1080p/1440p/4k/custom)",
        "1080p",
    )

    args.fps = int(
        ask(
            "FPS",
            "60",
        )
    )

    args.duration = float(
        ask(
            "Duration in seconds",
            "20",
        )
    )

    args.font_size = ask(
        "Font size (auto/number)",
        "auto",
    )

    args.speed = ask(
        "Scroll speed (auto/number)",
        "auto",
    )

    args.custom_size = ask(
        "Custom size",
        "",
    )

    args.bg = ask(
        "Background color",
        "black",
    )

    args.text = ask(
        "Text color",
        "white",
    )

    args.output = ask(
        "Output filename",
        "output.mp4",
    )

    return args


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
    )

    args = parser.parse_args()

    args = wizard(args)

    if args.custom_size:

        w, h = map(
            int,
            args.custom_size.split("x"),
        )

    else:

        w, h = PRESETS.get(
            args.quality,
            get_screen_size(),
        )

    if args.font_size == "auto":

        font = find_optimal_font(h)

    else:

        font = load_font(
            int(args.font_size)
        )

    text = load_file(
        Path(args.input)
    )

    canvas = build_canvas(
        text,
        w,
        h,
        args.bg,
        args.text,
        font,
    )

    if args.speed == "auto":

        if args.mode == "vertical":

            distance = canvas.shape[0] - h

        else:

            distance = w

        speed = distance / args.duration

    else:

        speed = float(
            args.speed
        )

    def frame(t):

        pos = int(speed * t)

        if args.mode == "horizontal":

            max_pos = canvas.shape[1] - w

            pos = min(
                pos,
                max_pos,
            )

            return canvas[
                :,
                pos:pos + w,
            ]

        max_pos = canvas.shape[0] - h

        pos = min(
            pos,
            max_pos,
        )

        return canvas[
            pos:pos + h
        ]

    video = VideoClip(
        frame,
        duration=args.duration,
    )

    video.write_videofile(
        args.output,
        fps=args.fps,
        codec="libx264",
        bitrate="80000k",
        ffmpeg_params=[
            "-pix_fmt",
            "yuv444p",

            "-preset",
            "veryslow",

            "-crf",
            "6",
        ],
        audio=False,
    )


if __name__ == "__main__":
    main()