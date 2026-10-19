"""Local text-to-card-video renderer. No account, network or license gate."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 720, 1280
COLORS = [(18, 30, 48), (32, 27, 55), (19, 50, 55)]


def font_path() -> Path:
    for name in ("msjh.ttc", "msyh.ttc", "mingliu.ttc"):
        path = Path("C:/Windows/Fonts") / name
        if path.is_file():
            return path
    raise RuntimeError("找不到繁中文字型；請在 Windows 安裝微軟正黑體或新細明體。")


def ffmpeg_path() -> str:
    base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
    bundled = base / "ffmpeg" / "ffmpeg.exe"
    if bundled.is_file():
        return str(bundled)
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise RuntimeError("找不到 FFmpeg；請使用 Windows 安裝版。")


def wrap(text: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if draw.textlength(candidate, font=font) > max_width and current:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_card(text: str, number: int, total: int, destination: Path) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS[(number - 1) % len(COLORS)])
    draw = ImageDraw.Draw(image)
    regular = ImageFont.truetype(str(font_path()), 60)
    small = ImageFont.truetype(str(font_path()), 35)
    caption = ImageFont.truetype(str(font_path()), 40)
    lines = wrap(text, draw, regular, WIDTH - 110)
    if len(lines) > 10:
        raise ValueError("單張字卡文字太長，請分段後重試。")
    top = (HEIGHT - len(lines) * 88) // 2 - 70
    for index, line in enumerate(lines):
        draw.text((WIDTH // 2, top + index * 88), line, font=regular, fill="#fffaf0", anchor="mt")
    draw.rounded_rectangle((44, 1025, WIDTH - 44, 1192), radius=24, fill="#101820")
    subtitle_lines = wrap(text, draw, caption, WIDTH - 150)[:2]
    for index, line in enumerate(subtitle_lines):
        draw.text((WIDTH // 2, 1060 + index * 52), line, font=caption, fill="white", anchor="mt")
    draw.text((WIDTH - 48, 80), f"{number} / {total}", font=small, fill="#c3d2e5", anchor="rt")
    image.save(destination)


def make_video(text: str, output: Path) -> Path:
    cards = [part.strip() for part in text.splitlines() if part.strip()]
    if not cards:
        raise ValueError("請輸入至少一行文字。")
    if len(cards) > 20:
        raise ValueError("免費版一次最多 20 張字卡。")
    ffmpeg = ffmpeg_path()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="anda-title-") as temporary:
        temp = Path(temporary)
        segments: list[Path] = []
        for number, card in enumerate(cards, 1):
            picture = temp / f"card-{number:02}.png"
            segment = temp / f"clip-{number:02}.mp4"
            draw_card(card, number, len(cards), picture)
            command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-framerate", "30", "-i", str(picture),
                       "-vf", "zoompan=z='min(zoom+0.0005,1.06)':d=60:s=720x1280:fps=30,fade=t=in:st=0:d=0.25,fade=t=out:st=1.75:d=0.25,format=yuv420p",
                       "-t", "2", "-an", "-c:v", "mpeg4", "-q:v", "5", str(segment)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            segments.append(segment)
        listing = temp / "clips.txt"
        listing.write_text("".join(f"file '{segment.as_posix()}'\n" for segment in segments), encoding="utf-8")
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                        "-c", "copy", str(output)], check=True, capture_output=True, text=True)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="安達免費字卡影片工具")
    parser.add_argument("--text", help="字卡文字；每行一張")
    parser.add_argument("--input", type=Path, help="UTF-8 文字檔")
    parser.add_argument("--output", type=Path, help="MP4 輸出路徑")
    args = parser.parse_args()
    if args.text or args.input:
        text = args.text if args.text is not None else args.input.read_text(encoding="utf-8-sig")
        path = make_video(text, args.output or Path.cwd() / "字卡影片.mp4")
        print(path)
        return 0
    from tkinter import Tk, Text, Label, Button, filedialog, messagebox
    root = Tk()
    root.title("安達免費字卡影片")
    root.geometry("640x440")
    Label(root, text="每行一句，做成一張字卡", font=("Microsoft JhengHei UI", 16)).pack(pady=14)
    field = Text(root, height=12, font=("Microsoft JhengHei UI", 12))
    field.pack(fill="both", expand=True, padx=18)

    def create() -> None:
        target = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 影片", "*.mp4")])
        if not target:
            return
        try:
            path = make_video(field.get("1.0", "end"), Path(target))
            messagebox.showinfo("完成", f"影片已存到：\n{path}")
        except (ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
            messagebox.showerror("製作失敗", str(exc))

    Button(root, text="製作影片", command=create, font=("Microsoft JhengHei UI", 13)).pack(pady=14)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
