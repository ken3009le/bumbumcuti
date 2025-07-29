import os, zipfile, tempfile, json
from pathlib import Path
from moviepy.editor import VideoFileClip
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed

IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
VIDEO_EXT = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'}
COLOR_SEQ = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']
RESET = '\033[0m'

def color_text(text, mode='cycle'):
    if mode == 'cycle':
        return ''.join(COLOR_SEQ[i % len(COLOR_SEQ)] + c for i, c in enumerate(text)) + RESET
    color = COLOR_SEQ[hash(text) % len(COLOR_SEQ)]
    return f"{color}{text}{RESET}"

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def format_duration(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"

def process_file(fp):
    try:
        ext = Path(fp).suffix.lower()
        if ext in IMAGE_EXT:
            return ('img', fp.replace(os.sep, '/'), os.path.getsize(fp))
        elif ext in VIDEO_EXT:
            size = os.path.getsize(fp)
            clip = VideoFileClip(fp)
            duration = clip.duration
            clip.close()
            return ('vid', fp.replace(os.sep, '/'), duration, size)
    except:
        return None

def scan_folder(folder, base_folder):
    images, videos = [], []
    file_paths = []
    for root, _, fs in os.walk(folder):
        for f in fs:
            abs_path = os.path.join(root, f)
            file_paths.append(abs_path)

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(process_file, f): f for f in file_paths}
        for future in as_completed(futures):
            result = future.result()
            if result:
                rel_path = os.path.relpath(result[1], base_folder).replace("\\", "/")
                if result[0] == 'img':
                    images.append({"path": rel_path, "size": result[2]})
                elif result[0] == 'vid':
                    videos.append({"path": rel_path, "duration": result[2], "size": result[3]})
    return images, videos

def show(images, videos, folder):
    if images:
        table = [[color_text(img["path"]), format_size(img["size"])] for img in images]
        print(color_text(f"\n📁 {folder} - ẢNH:", 'line'))
        print(tabulate(table, headers=["Tên ảnh", "Dung lượng"], tablefmt="fancy_grid"))
    if videos:
        table = [[color_text(v["path"]), format_duration(v["duration"]), format_size(v["size"])] for v in videos]
        print(color_text(f"\n📁 {folder} - VIDEO:", 'line'))
        print(tabulate(table, headers=["Tên video", "Thời lượng", "Dung lượng"], tablefmt="fancy_grid"))

def process_directory(base_path):
    data = {}
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            images, videos = scan_folder(full_path, base_path)
            show(images, videos, entry)
            data[entry] = {
                "images": images,
                "videos": videos
            }

    with open("media.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(color_text("\n✅ Đã lưu kết quả vào media.json", 'line'))

def process(p):
    if not p:
        p = "."
    if os.path.isfile(p) and p.lower().endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(p) as z:
                z.extractall(tmp)
            process_directory(tmp)
    elif os.path.isdir(p):
        process_directory(p)
    else:
        print("❌ Đường dẫn không hợp lệ.")

if __name__ == "__main__":
    print(color_text("📂 Nhập đường dẫn thư mục hoặc file .zip", 'line'))
    print(color_text("↪ Nhấn Enter để quét toàn bộ thư mục hiện tại\n", 'line'))
    user_input = input(">>> ").strip()
    process(user_input)
