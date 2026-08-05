#!/usr/bin/env python3
"""批量提取视频封面图（cv2 中间帧，JPEG q80，幂等 skip-if-exists）。

用法:
    python3 extract_covers.py --src <视频目录> --out <封面输出目录> [--force]

约定: 封面文件名 = 视频文件名去扩展名 + .jpg（与 speedrun 的 covers/{stem}.jpg 一致）。
依赖: opencv-python（pip install opencv-python）
"""
from __future__ import annotations

import argparse
import os
import sys

VIDEO_EXTS = {".mp4", ".webm", ".mkv", ".mov", ".avi", ".m4v"}


def extract_cover(video_path: str, cover_path: str) -> bool:
    import cv2
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total > 2:
        cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
    ok, frame = cap.read()
    cap.release()
    if not ok or frame is None:
        return False
    cv2.imwrite(cover_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="视频目录（递归扫描）")
    ap.add_argument("--out", required=True, help="封面输出目录（自动创建）")
    ap.add_argument("--force", action="store_true", help="已存在的封面也重新提取")
    args = ap.parse_args()

    try:
        import cv2  # noqa: F401
    except ImportError:
        sys.exit("error: 需要 opencv-python（pip install opencv-python）")

    if not os.path.isdir(args.src):
        sys.exit(f"error: 视频目录不存在: {args.src}")
    os.makedirs(args.out, exist_ok=True)

    done = skipped = failed = 0
    for root, _, files in os.walk(args.src):
        for fn in sorted(files):
            if fn.startswith(".") or os.path.splitext(fn)[1].lower() not in VIDEO_EXTS:
                continue
            stem = os.path.splitext(fn)[0]
            cover = os.path.join(args.out, stem + ".jpg")
            if os.path.isfile(cover) and not args.force:
                skipped += 1
                continue
            if extract_cover(os.path.join(root, fn), cover):
                done += 1
                print(f"✓ {stem}.jpg")
            else:
                failed += 1
                print(f"✗ 提取失败: {fn}", file=sys.stderr)

    print(f"完成: {done} 生成, {skipped} 跳过(已存在), {failed} 失败")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
