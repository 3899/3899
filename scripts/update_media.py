# 格式：python update_media.py "影视名称" "播放时间/评分" "偏好与追番等整体内容"
# 示例：python update_media.py "大话西游" "01:38:42 / 01:54:12" "偏好: 武侠 • 仙侠 • 古装 • 爱情 • 校园  丨  追番: 凡人修仙传 • 剑来"

import os
import sys
import re

def update_media_svg(file_path, new_title, new_time, new_footer):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace title text
    content = re.sub(
        r'(<text[^>]*class="title-text">)[^<]*(</text>)',
        rf'\g<1>{new_title}\g<2>',
        content
    )
    
    # Replace time text
    content = re.sub(
        r'(<text[^>]*class="time-text">)[^<]*(</text>)',
        rf'\g<1>{new_time}\g<2>',
        content
    )
    
    # Replace footer text
    content = re.sub(
        r'(<text[^>]*class="footer-text">)[^<]*(</text>)',
        rf'\g<1>{new_footer}\g<2>',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Successfully updated {os.path.basename(file_path)}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python update_media.py <MovieName> <TimeOrRating> <FooterText>")
        print("Example: python update_media.py \"大话西游\" \"01:38:42 / 01:54:12\" \"偏好: 武侠 • 仙侠 • 古装 • 爱情 • 校园  |  追番: 凡人修仙传 • 剑来\"")
        sys.exit(1)
        
    new_title = sys.argv[1]
    new_time = sys.argv[2]
    new_footer = sys.argv[3]
    
    # Paths to the SVGs
    dir_path = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.abspath(os.path.join(dir_path, "..", "static"))
    dark_path = os.path.join(static_path, 'media-dark.svg')
    light_path = os.path.join(static_path, 'media-light.svg')
    
    success_dark = update_media_svg(dark_path, new_title, new_time, new_footer)
    success_light = update_media_svg(light_path, new_title, new_time, new_footer)
    
    if success_dark and success_light:
        print("\nAll media SVGs updated successfully!")
