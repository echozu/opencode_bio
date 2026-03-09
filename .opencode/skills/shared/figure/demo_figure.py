#!/usr/bin/env python3
"""
figure skill 集成 Demo
======================

演示如何使用 figure skill 的 AutoFigure-Edit 引擎（方法段文本 → 可编辑 SVG）。

运行前请先安装依赖：
  pip install openai google-genai requests pillow numpy

使用方法：
  # 查看帮助
  python demo_figure.py --help

  # 用 bianxie 把方法段生成 SVG (最简单)
  python demo_figure.py autofigure \
      --api_key "YOUR_BIANXIE_KEY" \
      --text "We propose a dual-encoder framework. The image encoder extracts visual features, the text encoder processes captions. Features are fused via cross-attention and fed into a classifier."

  # 用 gemini 并指定多个 SAM3 prompt
  python demo_figure.py autofigure \
      --api_key "YOUR_GEMINI_KEY" \
      --provider gemini \
      --text "Our pipeline: raw reads → quality control → alignment → variant calling → annotation → clinical report." \
      --sam_prompt "icon,diagram,arrow"

  # 从文件读取方法段
  python demo_figure.py autofigure \
      --api_key "YOUR_KEY" \
      --method_file my_method_section.txt
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path

SKILL_DIR = Path(__file__).parent

def _find_autofigure_dir():
    """Locate autofigure-edit directory.
    Search order:
      1. ../../../../../autofigure-edit  (openBio/autofigure-edit — moved out of skills)
      2. ./autofigure-edit               (legacy: still inside skills/shared/figure/)
    """
    # From skills/shared/figure/ → go up to opencode_bio/ → up to openBio/
    external = SKILL_DIR.parent.parent.parent.parent.parent / "autofigure-edit"
    if external.is_dir():
        return external
    # Fallback: legacy location (still inside this skill dir)
    legacy = SKILL_DIR / "autofigure-edit"
    if legacy.is_dir():
        return legacy
    # Not found — return expected external path for error messages
    return external

AUTOFIGURE_DIR = _find_autofigure_dir()


def check_deps(packages):
    """检查哪些包没装"""
    missing = []
    for pkg in packages:
        import_name = pkg.replace("-", "_").replace("google-genai", "google.genai")
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)
    return missing


def run_autofigure(args):
    """运行 AutoFigure-Edit 引擎"""
    # 检查依赖
    missing = check_deps(["openai", "requests", "PIL", "numpy", "torch"])
    if missing:
        print(f"[!] 缺少依赖: {', '.join(missing)}")
        print(f"    请运行: pip install {' '.join(m if m != 'PIL' else 'pillow' for m in missing)}")
        return 1

    # 准备方法段文本
    if args.method_file:
        with open(args.method_file, "r", encoding="utf-8") as f:
            method_text = f.read().strip()
    elif args.text:
        method_text = args.text
    else:
        print("[!] 请通过 --text 或 --method_file 提供方法段文本")
        return 1

    # 写临时文件
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp_method = output_dir / "_method_input.txt"
    tmp_method.write_text(method_text, encoding="utf-8")

    # 构建命令
    script = AUTOFIGURE_DIR / "autofigure2.py"
    cmd_parts = [
        sys.executable, str(script),
        "--method_file", str(tmp_method),
        "--output_dir", str(output_dir),
        "--api_key", args.api_key,
        "--provider", args.provider,
        "--placeholder_mode", args.placeholder_mode,
    ]
    if args.sam_prompt:
        cmd_parts += ["--sam_prompt", args.sam_prompt]
    if args.optimize_iterations is not None:
        cmd_parts += ["--optimize_iterations", str(args.optimize_iterations)]

    print("=" * 60)
    print("AutoFigure-Edit Engine")
    print("=" * 60)
    print(f"  Provider:   {args.provider}")
    print(f"  Mode:       {args.placeholder_mode}")
    print(f"  Output:     {output_dir}/")
    print(f"  Method text ({len(method_text)} chars):")
    print(textwrap.indent(method_text[:200] + ("..." if len(method_text) > 200 else ""), "    "))
    print("-" * 60)
    print(f"  Running: {' '.join(cmd_parts[:6])} ...")
    print("-" * 60)

    os.execv(sys.executable, cmd_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Figure Skill Demo - AutoFigure-Edit 方法段 → SVG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        示例:
          python demo_figure.py autofigure --api_key KEY --text "We propose..."
        """)
    )
    subparsers = parser.add_subparsers(dest="engine", help="选择引擎")

    # ── AutoFigure-Edit ──
    af = subparsers.add_parser("autofigure", help="AutoFigure-Edit: 方法段 → 可编辑 SVG")
    af.add_argument("--api_key", required=True, help="API Key")
    af.add_argument("--provider", default="bianxie", choices=["bianxie", "openrouter", "gemini"],
                    help="LLM 提供商 (默认: bianxie)")
    af.add_argument("--text", type=str, help="方法段文本 (直接传入)")
    af.add_argument("--method_file", type=str, help="方法段文本文件路径")
    af.add_argument("--output_dir", default="./output_autofigure", help="输出目录")
    af.add_argument("--placeholder_mode", default="label", choices=["none", "box", "label"],
                    help="占位符模式 (默认: label)")
    af.add_argument("--sam_prompt", default=None, help='SAM3 prompts, 逗号分隔 (如 "icon,diagram,arrow")')
    af.add_argument("--optimize_iterations", type=int, default=None,
                    help="SVG 优化迭代次数 (0=跳过, 默认1)")

    args = parser.parse_args()

    if not args.engine:
        parser.print_help()
        print("\n" + "=" * 60)
        print("请选择引擎: autofigure")
        print("=" * 60)
        return 0

    if args.engine == "autofigure":
        return run_autofigure(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
