# text2mp4

# Text Scroll Video Generator

A Python tool that converts `.txt`, `.json`, or `.csv` files into smooth scrolling videos with customizable resolution, colors, speed, and animation direction.

# Features

- Supports:
  - TXT files
  - JSON files
  - CSV files
- Vertical or horizontal scrolling
- Automatic font scaling
- Multiple resolutions:
  - 720p
  - 1080p
  - 1440p
  - 4K
  - Custom sizes
- Custom background/text colors
- High quality H264 rendering
- Interactive setup wizard
- Smooth scrolling at customizable speed

# Requirements

- Python 3.9+
- FFmpeg installed on system

Python dependencies:

```bash
pip install numpy pillow moviepy
```

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/text-scroll-video-generator.git

cd text-scroll-video-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Usage

Run the script with an input file:

```bash
python3 main.py input.txt
```

The program will start an interactive wizard asking for the options given before.

# Output Quality

The video is rendered using:

- H264 codec
- Very slow preset
- CRF 6 quality
- yuv444p pixel format

This produces very high quality output videos.

---

# Notes

- FFmpeg must be installed and accessible from terminal.
- Font auto-sizing attempts to maximize screen usage automatically. Although it isn't fully working, yet.
- Default fonts use DejaVu Sans.

---

# License

## Non-Commercial License

This project is provided for personal, educational, and non-commercial use only.

You are NOT allowed to:

- Sell this software
- Use this software in commercial products
- Monetize content generated directly with this software
- Redistribute modified versions for commercial purposes

Commercial use requires explicit written permission from the author.

---

# Disclaimer

This software is provided "as is", without warranty of any kind.
The author is not responsible for any damages or misuse resulting from the use of this software.
