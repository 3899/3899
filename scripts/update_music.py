# 格式：python update_music.py "歌名" "歌词" "时间进度"
# python update_music.py "七里香" "雨下整夜 我的爱溢出就像雨水" "01:15 / 04:43"

import os
import sys
import re

def update_music_svg(file_path, new_title, new_lyric, new_time=None):
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
    
    # Replace lyric text
    content = re.sub(
        r'(<text[^>]*class="lyric-text">)[^<]*(</text>)',
        rf'\g<1>{new_lyric}\g<2>',
        content
    )
    
    # Replace time text if provided
    if new_time:
        content = re.sub(
            r'(<text[^>]*class="time-text">)[^<]*(</text>)',
            rf'\g<1>{new_time}\g<2>',
            content
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Successfully updated {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_music.py <SongName> <Lyric> [Time]")
        print("Example: python update_music.py \"晴天\" \"故事的小黄花\" \"01:23 / 04:29\"")
        sys.exit(1)
        
    new_title = sys.argv[1]
    new_lyric = sys.argv[2]
    new_time = sys.argv[3] if len(sys.argv) >= 4 else None
    
    # Paths to the SVGs
    dir_path = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.abspath(os.path.join(dir_path, "..", "static"))
    dark_path = os.path.join(static_path, 'music-dark.svg')
    light_path = os.path.join(static_path, 'music-light.svg')
    
    success_dark = update_music_svg(dark_path, new_title, new_lyric, new_time)
    success_light = update_music_svg(light_path, new_title, new_lyric, new_time)
    
    if success_dark and success_light:
        print("\nAll music SVGs updated successfully! You can now commit and push.")
