# 格式：python update_hobbies.py <1|2> "分类/名称" "加粗标题" "底部状态" [颜色名称]
# 示例：python update_hobbies.py 1 "Smart Home Automation" "Home Assistant • MIJIA 自动化中枢" "Home Assistant 正常运行 • 节点已组网" "blue"

import os
import sys
import re

COLOR_THEMES = {
    "blue": {"dark": "#00BFFF", "light": "#0366d6"},
    "green": {"dark": "#2ea44f", "light": "#2ea44f"},
    "red": {"dark": "#ff4d4f", "light": "#cf1322"},
    "orange": {"dark": "#ff9f0a", "light": "#f0883b"},
    "purple": {"dark": "#bf5af2", "light": "#8957e5"},
    "yellow": {"dark": "#ffd60a", "light": "#b58900"},
}

def update_hobby_svg(file_path, title, bold_highlight, status, color_hex):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace gray-text (Title)
    content = re.sub(
        r'(<text[^>]*class="gray-text">)[^<]*(</text>)',
        rf'\g<1>{title}\g<2>',
        content
    )
    
    # Replace bold-highlight (Subtitle)
    content = re.sub(
        r'(<text[^>]*class="bold-highlight">)[^<]*(</text>)',
        rf'\g<1>{bold_highlight}\g<2>',
        content
    )
    
    # Replace status text
    content = re.sub(
        r'(<text[^>]*class="status-text">)[^<]*(</text>)',
        rf'\g<1>{status}\g<2>',
        content
    )
    
    # Replace colors in stylesheet
    # 1. replace status-text color
    content = re.sub(
        r'(\.status-text\s*\{[^}]*fill:\s*)[^;}]+',
        rf'\g<1>{color_hex}',
        content
    )
    # 2. replace dot-color fill
    content = re.sub(
        r'(\.dot-color\s*\{\s*fill:\s*)[^;}]+',
        rf'\g<1>{color_hex}',
        content
    )
    # 3. replace dot-color drop-shadow
    content = re.sub(
        r'(drop-shadow\(0 0 3px\s*)[^)]+',
        rf'\g<1>{color_hex}',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Successfully updated {os.path.basename(file_path)}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python update_hobbies.py <1|2> <Title> <HighlightText> <StatusText> [ColorName/Hex]")
        print("Example: python update_hobbies.py 1 \"Smart Home\" \"Home Assistant\" \"节点已组网\" \"blue\"")
        sys.exit(1)
        
    idx = sys.argv[1]
    if idx not in ("1", "2"):
        print("Error: Hobby index must be 1 or 2.")
        sys.exit(1)
        
    title = sys.argv[2]
    highlight = sys.argv[3]
    status = sys.argv[4]
    
    color_input = sys.argv[5].lower() if len(sys.argv) >= 6 else ("blue" if idx == "1" else "green")
    
    # Determine dark and light hex values
    if color_input in COLOR_THEMES:
        dark_color = COLOR_THEMES[color_input]["dark"]
        light_color = COLOR_THEMES[color_input]["light"]
    else:
        # Fallback to direct hex color if provided
        dark_color = color_input
        light_color = color_input
        
    dir_path = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.abspath(os.path.join(dir_path, "..", "static"))
    dark_file = os.path.join(static_path, f"hobby-{idx}-dark.svg")
    light_file = os.path.join(static_path, f"hobby-{idx}-light.svg")
    
    success_dark = update_hobby_svg(dark_file, title, highlight, status, dark_color)
    success_light = update_hobby_svg(light_file, title, highlight, status, light_color)
    
    if success_dark and success_light:
        print(f"\nHobby {idx} updated successfully!")
