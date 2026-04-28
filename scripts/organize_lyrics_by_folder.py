import os
import shutil
from pathlib import Path
from datetime import datetime

# 配置项 - 可自行修改
CONFIG = {
    'FILES_PER_FOLDER': 50,  # 每个文件夹包含的文件数
    'FOLDER_PREFIX': 'lrc',  # 文件夹名前缀
    'LYRICS_EXTENSION': '.lrc',
    'DRY_RUN': False,  # 如果为 True，只模拟操作但不实际移动文件
}


def get_all_lyrics_files(base_folder):
    """获取所有 .lrc 文件并排序"""
    lyrics_files = []
    
    for file in os.listdir(base_folder):
        if file.lower().endswith(CONFIG['LYRICS_EXTENSION']):
            file_path = os.path.join(base_folder, file)
            # 只获取文件，不包括目录
            if os.path.isfile(file_path):
                lyrics_files.append(file)
    
    # 按文件名排序
    lyrics_files.sort()
    return lyrics_files


def create_folder_structure(base_folder, lyrics_files):
    """创建文件夹结构并返回操作日志"""
    if not lyrics_files:
        print("警告: 未找到任何 .lrc 文件")
        return []
    
    operations = []
    files_per_folder = CONFIG['FILES_PER_FOLDER']
    folder_prefix = CONFIG['FOLDER_PREFIX']
    
    # 计算需要创建的文件夹数量
    total_files = len(lyrics_files)
    num_folders = (total_files + files_per_folder - 1) // files_per_folder
    
    print(f"总文件数: {total_files}")
    print(f"每个文件夹: {files_per_folder} 个文件")
    print(f"需要创建: {num_folders} 个文件夹")
    print()
    
    # 遍历每个文件夹
    for folder_idx in range(num_folders):
        folder_num = folder_idx + 1
        folder_name = f"{folder_prefix}_{folder_num:03d}"
        folder_path = os.path.join(base_folder, folder_name)
        
        # 计算该文件夹包含的文件范围
        start_idx = folder_idx * files_per_folder
        end_idx = min(start_idx + files_per_folder, total_files)
        files_in_folder = lyrics_files[start_idx:end_idx]
        
        # 创建文件夹（如果不存在）
        if not os.path.exists(folder_path):
            if not CONFIG['DRY_RUN']:
                os.makedirs(folder_path)
            print(f"✓ 创建文件夹: {folder_name} ({len(files_in_folder)} 个文件)")
        else:
            print(f"! 文件夹已存在: {folder_name}（跳过）")
            continue
        
        # 移动文件
        for file_name in files_in_folder:
            src = os.path.join(base_folder, file_name)
            dst = os.path.join(folder_path, file_name)
            
            if not CONFIG['DRY_RUN']:
                shutil.move(src, dst)
            
            operations.append({
                'action': 'move',
                'source': src,
                'destination': dst,
                'file': file_name,
                'folder': folder_name
            })
        
        print(f"  → 已移动 {len(files_in_folder)} 个文件到 {folder_name}")
    
    return operations


def generate_report(base_folder, operations, start_time):
    """生成操作报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"organize_lyrics_report_{timestamp}.txt"
    report_path = os.path.join(base_folder, report_filename)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("歌词文件组织操作报告\n")
        f.write("=" * 100 + "\n")
        f.write(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"耗时: {duration:.2f} 秒\n")
        f.write(f"操作文件夹: {base_folder}\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"【配置信息】\n")
        f.write(f"  每个文件夹包含文件数: {CONFIG['FILES_PER_FOLDER']}\n")
        f.write(f"  文件夹名前缀: {CONFIG['FOLDER_PREFIX']}\n")
        f.write(f"  文件扩展名: {CONFIG['LYRICS_EXTENSION']}\n")
        f.write(f"  模拟运行: {CONFIG['DRY_RUN']}\n")
        f.write("\n")
        
        f.write(f"【操作统计】\n")
        f.write(f"  总操作数: {len(operations)}\n")
        
        if operations:
            # 统计每个文件夹
            folders = {}
            for op in operations:
                folder = op['folder']
                if folder not in folders:
                    folders[folder] = []
                folders[folder].append(op)
            
            f.write(f"  创建文件夹数: {len(folders)}\n\n")
            
            f.write(f"【详细操作】\n")
            f.write("-" * 100 + "\n")
            
            for folder_name in sorted(folders.keys()):
                files = folders[folder_name]
                f.write(f"\n{folder_name} ({len(files)} 个文件):\n")
                for i, op in enumerate(files, 1):
                    f.write(f"  {i}. {op['file']}\n")
        else:
            f.write(f"  创建文件夹数: 0\n")
            f.write("\n  没有进行任何操作\n")
    
    return report_path


def main():
    import sys
    
    base_folder = None
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        base_folder = sys.argv[1]
    
    # 如果没有提供路径，交互式选择
    if base_folder is None:
        print("=" * 100)
        print("歌词文件组织工具 - 按文件夹分组 (每50个文件一个文件夹)")
        print("=" * 100)
        print("\n请选择查询方式:")
        print("1. 使用脚本所在目录的上级目录 (默认 - 通常是 Music 文件夹)")
        print("2. 使用当前工作目录")
        print("3. 手动输入路径")
        
        choice = input("\n请选择 (1/2/3，默认为1): ").strip()
        
        if choice == '2':
            base_folder = os.getcwd()
        elif choice == '3':
            base_folder = input("请输入要查询的路径: ").strip()
        else:
            # 默认使用脚本上级目录的 jp 子文件夹
            base_folder = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'jp'
            )
    
    # 确保路径存在
    if not os.path.isdir(base_folder):
        print(f"错误: 路径 '{base_folder}' 不存在或不是目录")
        return
    
    print("=" * 100)
    print("歌词文件组织工具")
    print("=" * 100)
    print(f"工作目录: {base_folder}")
    print(f"每个文件夹包含: {CONFIG['FILES_PER_FOLDER']} 个文件")
    print(f"模拟运行: {CONFIG['DRY_RUN']}")
    print("=" * 100)
    print()
    
    # 获取所有歌词文件
    lyrics_files = get_all_lyrics_files(base_folder)
    
    if not lyrics_files:
        print("错误: 未找到任何 .lrc 文件")
        return
    
    print(f"找到 {len(lyrics_files)} 个 .lrc 文件\n")
    
    # 确认操作
    if not CONFIG['DRY_RUN']:
        confirm = input("是否继续执行操作? (y/n，默认为 n): ").strip().lower()
        if confirm != 'y':
            print("操作已取消")
            return
        print()
    
    start_time = datetime.now()
    
    # 创建文件夹结构
    operations = create_folder_structure(base_folder, lyrics_files)
    
    # 生成报告
    report_path = generate_report(base_folder, operations, start_time)
    
    print("\n" + "=" * 100)
    print("操作完成！")
    print("=" * 100)
    print(f"报告已保存到: {report_path}")
    
    if CONFIG['DRY_RUN']:
        print("\n注意: 这是模拟运行，没有实际移动文件")
        print("要执行实际操作，请在脚本中修改:")
        print("  CONFIG['DRY_RUN'] = False")


if __name__ == "__main__":
    main()
