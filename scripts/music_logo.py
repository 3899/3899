#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Music Logo SVG Generator
仅生成音乐黑胶唱片 Logo（包含平滑旋转动画与唱针，无任何文字、进度条、按钮或边框等冗余元素）

使用示例:
    # 默认生成深色与浅色版本到 static 目录
    python scripts/generate_music_logo.py

    # 自定义旋转周期（秒）、中心标签颜色、是否包含唱针
    python scripts/generate_music_logo.py --speed 6 --label-color "#e60026"
    python scripts/generate_music_logo.py --no-needle
    python scripts/generate_music_logo.py --target music  # 直接更新 static/music-dark.svg 与 static/music-light.svg
"""

import os
import sys
import argparse

# 确保在 Windows 控制台等环境下正常输出 UTF-8 字符
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 主题配色定义（暗色模式与浅色模式唱片统一采用最佳视觉色差，质感自然适中）
THEME_CONFIG = {
    "dark": {
        "cd_body": "#181f2a",     # 黑胶底色适度调浅，在深色背景下轮廓更清晰
        "cd_groove": "#5c667a",   # 与浅色模式一致的细腻反光纹路色，明暗对比刚刚好
        "stylus": "#6e7781",      # 与浅色模式一致的金属灰唱针，层次自然协调
        "center_hole": "#090d16"  # 唱片轴心孔深色
    },
    "light": {
        "cd_body": "#181f2a",     # 纯黑胶底色
        "cd_groove": "#5c667a",   # 浅色模式下唱片内部细腻反光纹路
        "stylus": "#6e7781",      # 金属灰唱针
        "center_hole": "#090d16"
    }
}

def generate_svg_content(theme="dark", spin_speed=8.0, label_color="#e60026", groove_color=None, stylus_color=None, include_needle=True, size=120):
    """
    生成仅含黑胶唱片 Logo 的纯净 SVG 字符串
    """
    colors = THEME_CONFIG.get(theme, THEME_CONFIG["dark"]).copy()
    if groove_color:
        colors["cd_groove"] = groove_color
    if stylus_color:
        colors["stylus"] = stylus_color
    
    # 唱针元素（如果启用）
    needle_svg = ""
    if include_needle:
        needle_svg = f"""    <!-- Stylus / Needle -->
    <circle cx="93" cy="27" r="2.5" fill="{colors['stylus']}" />
    <path d="M93 27 L79 40 L74 52" stroke="{colors['stylus']}" stroke-width="1.6" stroke-linecap="round" fill="none" />
    <rect x="71" y="50" width="4" height="6" transform="rotate(-25 73 53)" fill="{colors['stylus']}" />"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" fill="none" width="{size}" height="{size}">
  <style>
    @keyframes spin {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .cd-disk {{
      animation: spin {spin_speed}s linear infinite;
      transform-origin: 60px 60px;
    }}
    .cd-groove {{ stroke: {colors['cd_groove']}; }}
  </style>

  <!-- CD Disk Logo Group -->
  <g>
    <!-- Outer CD Body (纯黑胶盘体，无外圈浅色粗边框) -->
    <circle cx="60" cy="60" r="35" fill="{colors['cd_body']}" />
    
    <!-- Spinning Vinyl Record -->
    <g class="cd-disk">
      <!-- Vinyl Grooves -->
      <circle cx="60" cy="60" r="30" fill="none" stroke-width="0.9" class="cd-groove" stroke-dasharray="6,4" />
      <circle cx="60" cy="60" r="26" fill="none" stroke-width="0.9" class="cd-groove" />
      <circle cx="60" cy="60" r="21" fill="none" stroke-width="0.9" class="cd-groove" stroke-dasharray="10,5" />
      <circle cx="60" cy="60" r="16" fill="none" stroke-width="0.9" class="cd-groove" />
      <!-- Center Label & Spindle Hole -->
      <circle cx="60" cy="60" r="10" fill="{label_color}" />
      <circle cx="60" cy="60" r="3" fill="{colors['center_hole']}" />
    </g>

{needle_svg}
  </g>
</svg>
"""
    return svg

def save_svg_file(file_path, content):
    """
    保存 SVG 内容到文件
    """
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Successfully generated: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="生成纯净版音乐黑胶唱片 Logo SVG")
    parser.add_argument("--theme", choices=["all", "dark", "light"], default="all", help="生成的主题模式 (默认: all 同时生成 dark 和 light)")
    parser.add_argument("--speed", type=float, default=8.0, help="黑胶旋转一圈的时间(秒，默认: 8.0)")
    parser.add_argument("--label-color", default="#e60026", help="唱片中心标签颜色 (默认: #e60026)")
    parser.add_argument("--groove-color", default=None, help="自定义黑胶纹路颜色 (如: #5c667a)")
    parser.add_argument("--stylus-color", default=None, help="自定义唱针颜色 (如: #d0d7de)")
    parser.add_argument("--no-needle", action="store_true", help="不包含唱针，仅保留旋转黑胶唱片")
    parser.add_argument("--size", type=int, default=120, help="SVG 视口大小 (默认: 120)")
    parser.add_argument("--output-dir", default=None, help="输出目录 (默认: 项目 static 目录)")
    parser.add_argument("--name", default="music-logo", help="输出文件名称前缀 (默认: music-logo)")
    parser.add_argument("--overwrite-music-card", action="store_true", help="直接覆盖 static/music-dark.svg 与 static/music-light.svg")

    args = parser.parse_args()

    # 确定输出目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = args.output_dir if args.output_dir else os.path.abspath(os.path.join(script_dir, "..", "static"))

    include_needle = not args.no_needle
    themes = ["dark", "light"] if args.theme == "all" else [args.theme]

    for theme in themes:
        svg_content = generate_svg_content(
            theme=theme,
            spin_speed=args.speed,
            label_color=args.label_color,
            groove_color=args.groove_color,
            stylus_color=args.stylus_color,
            include_needle=include_needle,
            size=args.size
        )
        
        # 文件命名
        if args.overwrite_music_card:
            file_name = f"music-{theme}.svg"
        else:
            file_name = f"{args.name}-{theme}.svg"
            
        file_path = os.path.join(output_dir, file_name)
        save_svg_file(file_path, svg_content)

    print("\nLogo SVGs generated successfully!")

if __name__ == "__main__":
    main()
