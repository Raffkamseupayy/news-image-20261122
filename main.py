#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261122.

Copies the committed news image (news_2026_11_22.png, built deterministically
by build_image.py: the 22 November 2026 world-news front page) to the output
directory as entry.png. No network, no randomness, byte-identical every run.

Run:  python3 main.py                       # writes /output/entry.png
      MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SOURCE = os.path.join(HERE, "news_2026_11_22.png")
TARGET = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SOURCE, TARGET)
print("wrote", TARGET)
