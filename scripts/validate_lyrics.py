import os
import re
from datetime import datetime
from pathlib import Path

def extract_artist_and_title(filename):
    """从文件名中提取艺术家和歌曲名
    文件名格式: [艺术家] - [歌曲名].lrc
    """
    # 移除 .lrc 扩展名
    name_without_ext = os.path.splitext(filename)[0]
    
    # 使用正则表达式分割
    match = re.match(r'^(.+?)\s*-\s*(.+)$', name_without_ext)
    if match:
        artist = match.group(1).strip()
        title = match.group(2).strip()
        return artist, title
    return None, None

def read_first_lines(file_path, num_lines=10):
    """读取文件的前N行"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= num_lines:
                    break
                lines.append(line.strip())
            return lines
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return []

def content_contains_key_info(lines, artist, title):
    """检查前10行是否包含艺术家或歌曲名信息"""
    # 将所有行合并为一个字符串，便于检查
    content = '\n'.join(lines).lower()
    artist_lower = artist.lower()
    title_lower = title.lower()
    
    # 检查是否包含艺术家或歌曲名
    has_artist = artist_lower in content
    has_title = title_lower in content
    
    return has_artist or has_title, has_artist, has_title

def validate_lyrics_files(base_folder, lyric_folders=None):
    """验证歌词文件"""
    unmatched_files = []
    total_files = 0
    
    if lyric_folders is None:
        lyric_folders = ['cn', 'en', 'jp']
    
    # 检查基础文件夹是否直接包含 .lrc 文件
    has_lrc_direct = any(f.endswith('.lrc') for f in os.listdir(base_folder) if os.path.isfile(os.path.join(base_folder, f)))
    
    # 如果直接包含 .lrc 文件，则直接检查这个文件夹
    folders_to_check = []
    if has_lrc_direct:
        folders_to_check = [(os.path.basename(base_folder) or 'lyrics', base_folder)]
    else:
        # 否则检查子文件夹
        for folder in lyric_folders:
            folder_path = os.path.join(base_folder, folder)
            if os.path.exists(folder_path):
                folders_to_check.append((folder, folder_path))
    
    # 如果没有找到任何要检查的文件夹
    if not folders_to_check:
        print(f"警告: 在 {base_folder} 中未找到歌词文件夹或 .lrc 文件")
        return total_files, unmatched_files
    
    # 检查每个文件夹
    for folder_name, folder_path in folders_to_check:
        print(f"\n正在检查 {folder_name} 文件夹...")
        print(f"路径: {folder_path}")
        
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith('.lrc'):
                continue
            
            total_files += 1
            file_path = os.path.join(folder_path, filename)
            
            # 提取艺术家和歌曲名
            artist, title = extract_artist_and_title(filename)
            
            if artist is None or title is None:
                unmatched_files.append({
                    'folder': folder_name,
                    'filename': filename,
                    'reason': '文件名格式不符合 [艺术家] - [歌曲名] 规范',
                    'artist': None,
                    'title': None,
                    'has_artist': False,
                    'has_title': False
                })
                continue
            
            # 读取前10行
            first_lines = read_first_lines(file_path, num_lines=10)
            
            if not first_lines:
                unmatched_files.append({
                    'folder': folder_name,
                    'filename': filename,
                    'reason': '无法读取文件内容',
                    'artist': artist,
                    'title': title,
                    'has_artist': False,
                    'has_title': False
                })
                continue
            
            # 检查内容是否包含关键信息
            matches, has_artist, has_title = content_contains_key_info(first_lines, artist, title)
            
            if not matches:
                unmatched_files.append({
                    'folder': folder_name,
                    'filename': filename,
                    'reason': '前10行不包含艺术家或歌曲名信息',
                    'artist': artist,
                    'title': title,
                    'has_artist': has_artist,
                    'has_title': has_title,
                    'preview': first_lines[:3]  # 保存前3行预览
                })
    
    return total_files, unmatched_files

def generate_report(base_folder, total_files, unmatched_files):
    """生成验证报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"lyrics_validation_report_{timestamp}.txt"
    report_path = os.path.join(base_folder, report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("歌词文件验证报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"检查总数: {total_files} 个文件\n")
        f.write(f"不匹配数: {len(unmatched_files)} 个文件\n")
        f.write(f"匹配率: {((total_files - len(unmatched_files)) / total_files * 100) if total_files > 0 else 0:.2f}%\n")
        f.write("=" * 80 + "\n\n")
        
        if not unmatched_files:
            f.write("✓ 所有歌词文件都符合要求！\n")
        else:
            f.write(f"发现 {len(unmatched_files)} 个不匹配的文件:\n")
            f.write("-" * 80 + "\n\n")
            
            for i, item in enumerate(unmatched_files, 1):
                f.write(f"{i}. 文件夹: {item['folder']}\n")
                f.write(f"   文件名: {item['filename']}\n")
                
                if item['artist']:
                    f.write(f"   艺术家: {item['artist']}\n")
                    f.write(f"   歌曲名: {item['title']}\n")
                    f.write(f"   艺术家匹配: {'✓' if item['has_artist'] else '✗'}\n")
                    f.write(f"   歌曲名匹配: {'✓' if item['has_title'] else '✗'}\n")
                    
                    if 'preview' in item:
                        f.write(f"   前3行预览:\n")
                        for line in item['preview']:
                            f.write(f"     > {line[:70]}\n")
                
                f.write(f"   原因: {item['reason']}\n")
                f.write("\n")
    
    return report_path

def main():
    import sys
    
    base_folder = None
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        base_folder = sys.argv[1]
    
    # 如果没有提供路径，交互式选择
    if base_folder is None:
        print("=" * 80)
        print("歌词文件验证工具")
        print("=" * 80)
        print("\n请选择查询方式:")
        print("1. 使用脚本所在目录 (默认)")
        print("2. 使用当前工作目录")
        print("3. 手动输入路径")
        
        choice = input("\n请选择 (1/2/3，默认为1): ").strip()
        
        if choice == '2':
            base_folder = os.getcwd()
        elif choice == '3':
            base_folder = input("请输入要查询的路径: ").strip()
        else:
            base_folder = os.path.dirname(os.path.abspath(__file__))
    
    # 确保路径存在
    if not os.path.isdir(base_folder):
        print(f"错误: 路径 '{base_folder}' 不存在或不是目录")
        return
    
    print("=" * 80)
    print("开始验证歌词文件...")
    print(f"基础文件夹: {base_folder}")
    print("=" * 80)
    
    # 执行验证
    total_files, unmatched_files = validate_lyrics_files(base_folder)
    
    # 生成报告
    report_path = generate_report(base_folder, total_files, unmatched_files)
    
    print(f"\n验证完成！")
    print(f"总检查文件数: {total_files}")
    print(f"不匹配文件数: {len(unmatched_files)}")
    print(f"匹配率: {((total_files - len(unmatched_files)) / total_files * 100) if total_files > 0 else 0:.2f}%")
    print(f"\n报告已保存到: {report_path}")
    
    # 如果有不匹配的文件，也打印到控制台
    if unmatched_files:
        print("\n" + "=" * 80)
        print("不匹配文件列表 (控制台输出):")
        print("=" * 80)
        for i, item in enumerate(unmatched_files[:20], 1):  # 只显示前20个
            print(f"{i}. [{item['folder']}] {item['filename']}")
            if item['artist']:
                print(f"   → 艺术家: {item['artist']}, 歌曲: {item['title']}")
        
        if len(unmatched_files) > 20:
            print(f"\n... 还有 {len(unmatched_files) - 20} 个不匹配的文件")

if __name__ == "__main__":
    main()
