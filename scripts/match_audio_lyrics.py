import os
import re
from pathlib import Path
from datetime import datetime
import sys

# 配置项 - 可自行修改
CONFIG = {
    'TIME_TOLERANCE_SECONDS': 50,  # 允许的时长误差（秒）
    'AUDIO_EXTENSIONS': ['.mp3', '.flac', '.m4a', '.aiff', '.wav', '.ogg', '.wma'],
    'LYRICS_EXTENSIONS': ['.lrc'],
}

try:
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.wave import WAVE
    from mutagen.oggvorbis import OggVorbis
    from mutagen.oggflac import OggFLAC
    from mutagen.asf import ASF
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("警告: 未找到 mutagen 库，将无法读取音乐文件时长")
    print("请运行: pip install mutagen")


def get_audio_duration(audio_path):
    """获取音乐文件时长（秒）"""
    if not MUTAGEN_AVAILABLE:
        return None
    
    try:
        # 尝试用通用方法读取
        audio = MutagenFile(audio_path)
        if audio is not None and hasattr(audio.info, 'length'):
            return audio.info.length
        
        # 如果失败，尝试特定格式
        ext = os.path.splitext(audio_path)[1].lower()
        
        if ext == '.mp3':
            audio = MP3(audio_path)
        elif ext == '.flac':
            audio = FLAC(audio_path)
        elif ext == '.wav':
            audio = WAVE(audio_path)
        elif ext in ['.ogg', '.ogv']:
            audio = OggVorbis(audio_path)
        elif ext == '.m4a':
            # M4A 使用 MP4
            try:
                from mutagen.mp4 import MP4
                audio = MP4(audio_path)
            except:
                return None
        elif ext == '.aiff':
            # AIFF 需要特殊处理
            try:
                from mutagen.aiff import AIFF
                audio = AIFF(audio_path)
            except:
                return None
        else:
            return None
        
        return audio.info.length if audio and hasattr(audio.info, 'length') else None
    
    except Exception as e:
        print(f"  ⚠ 读取失败: {e}")
        return None


def extract_last_timestamp(lyrics_path):
    """提取歌词文件的最后一条时间码（秒）"""
    try:
        with open(lyrics_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # 从后向前查找第一条有时间码的行
        for line in reversed(lines):
            # 匹配 [mm:ss.xx] 格式
            match = re.search(r'\[(\d+):(\d+\.\d+)\]', line)
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                return minutes * 60 + seconds
        
        return None
    
    except Exception as e:
        print(f"  ⚠ 读取歌词失败: {e}")
        return None


def format_duration(seconds):
    """将秒数转换为 mm:ss.xx 格式"""
    if seconds is None:
        return "N/A"
    minutes = int(seconds) // 60
    secs = seconds % 60
    return f"{minutes}:{secs:06.2f}"


def find_matching_lyrics(audio_path, lyrics_folders):
    """根据音乐文件名找到对应的歌词文件"""
    # 从音乐文件名提取艺术家和歌曲名
    filename_without_ext = os.path.splitext(os.path.basename(audio_path))[0]
    audio_dir = os.path.dirname(audio_path)
    
    # 首先在音乐文件所在目录中查找
    lyrics_file = os.path.join(audio_dir, filename_without_ext + '.lrc')
    if os.path.exists(lyrics_file):
        return lyrics_file
    
    # 然后在各个指定的歌词文件夹中查找
    for lyrics_folder in lyrics_folders:
        lyrics_file = os.path.join(lyrics_folder, filename_without_ext + '.lrc')
        if os.path.exists(lyrics_file):
            return lyrics_file
    
    return None


def compare_audio_lyrics(base_folder, lyrics_folders=None):
    """比较音乐文件和歌词文件时长"""
    
    if lyrics_folders is None:
        lyrics_folders = ['cn', 'en', 'jp', 'ko']
    
    # 将相对路径转换为绝对路径，同时过滤不存在的文件夹
    abs_lyrics_folders = []
    for folder in lyrics_folders:
        abs_path = os.path.join(base_folder, folder)
        if os.path.isdir(abs_path):
            abs_lyrics_folders.append(abs_path)
    
    lyrics_folders = abs_lyrics_folders
    
    results = {
        'matched': [],      # 时长匹配
        'mismatched': [],   # 时长不匹配
        'no_lyrics': [],    # 没有对应歌词
        'read_error': [],   # 读取错误
    }
    
    # 扫描音乐文件
    audio_count = 0
    for audio_ext in CONFIG['AUDIO_EXTENSIONS']:
        for root, dirs, files in os.walk(base_folder):
            # 跳过歌词文件夹（过滤掉指定的歌词文件夹）
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in lyrics_folders]
            
            for file in files:
                if file.lower().endswith(audio_ext):
                    audio_count += 1
                    audio_path = os.path.join(root, file)
                    
                    # 获取音乐文件时长
                    audio_duration = get_audio_duration(audio_path)
                    
                    if audio_duration is None:
                        results['read_error'].append({
                            'audio_file': audio_path,
                            'reason': '无法读取音乐文件时长'
                        })
                        continue
                    
                    # 查找对应的歌词文件
                    lyrics_file = find_matching_lyrics(audio_path, lyrics_folders)
                    
                    if lyrics_file is None:
                        results['no_lyrics'].append({
                            'audio_file': audio_path,
                            'audio_duration': audio_duration,
                            'audio_duration_str': format_duration(audio_duration)
                        })
                        continue
                    
                    # 获取歌词文件的最后时间码
                    lyrics_duration = extract_last_timestamp(lyrics_file)
                    
                    if lyrics_duration is None:
                        results['read_error'].append({
                            'audio_file': audio_path,
                            'lyrics_file': lyrics_file,
                            'reason': '无法读取歌词文件的时间码'
                        })
                        continue
                    
                    # 比较时长
                    diff = abs(audio_duration - lyrics_duration)
                    
                    if diff <= CONFIG['TIME_TOLERANCE_SECONDS']:
                        results['matched'].append({
                            'audio_file': audio_path,
                            'lyrics_file': lyrics_file,
                            'audio_duration': audio_duration,
                            'lyrics_duration': lyrics_duration,
                            'diff': diff,
                            'audio_duration_str': format_duration(audio_duration),
                            'lyrics_duration_str': format_duration(lyrics_duration),
                        })
                    else:
                        results['mismatched'].append({
                            'audio_file': audio_path,
                            'lyrics_file': lyrics_file,
                            'audio_duration': audio_duration,
                            'lyrics_duration': lyrics_duration,
                            'diff': diff,
                            'audio_duration_str': format_duration(audio_duration),
                            'lyrics_duration_str': format_duration(lyrics_duration),
                        })
    
    return audio_count, results


def generate_report(base_folder, audio_count, results):
    """生成比较报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"audio_lyrics_match_report_{timestamp}.txt"
    report_path = os.path.join(base_folder, report_filename)
    
    matched = len(results['matched'])
    mismatched = len(results['mismatched'])
    no_lyrics = len(results['no_lyrics'])
    read_error = len(results['read_error'])
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("音乐文件与歌词时长比较报告\n")
        f.write("=" * 100 + "\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"时长误差容限: {CONFIG['TIME_TOLERANCE_SECONDS']} 秒\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"【统计信息】\n")
        f.write(f"  总音乐文件数: {audio_count}\n")
        f.write(f"  时长匹配: {matched} 个 ✓\n")
        f.write(f"  时长不匹配: {mismatched} 个 ✗\n")
        f.write(f"  没有歌词: {no_lyrics} 个 -\n")
        f.write(f"  读取错误: {read_error} 个 ⚠\n")
        f.write(f"  匹配率: {(matched / (audio_count - read_error) * 100) if (audio_count - read_error) > 0 else 0:.2f}%\n")
        f.write("\n" + "=" * 100 + "\n\n")
        
        # 时长不匹配的文件
        if mismatched > 0:
            f.write(f"【时长不匹配】({mismatched} 个文件)\n")
            f.write("-" * 100 + "\n")
            for i, item in enumerate(results['mismatched'], 1):
                f.write(f"\n{i}. 音乐: {os.path.relpath(item['audio_file'], base_folder)}\n")
                f.write(f"   歌词: {os.path.relpath(item['lyrics_file'], base_folder)}\n")
                f.write(f"   音乐时长: {item['audio_duration_str']}\n")
                f.write(f"   歌词时长: {item['lyrics_duration_str']}\n")
                f.write(f"   误差: {item['diff']:.2f} 秒\n")
            f.write("\n" + "=" * 100 + "\n\n")
        
        # 没有对应歌词的文件
        if no_lyrics > 0:
            f.write(f"【没有对应歌词】({no_lyrics} 个文件)\n")
            f.write("-" * 100 + "\n")
            for i, item in enumerate(results['no_lyrics'][:30], 1):  # 只显示前30个
                f.write(f"{i}. {os.path.relpath(item['audio_file'], base_folder)} ({item['audio_duration_str']})\n")
            if no_lyrics > 30:
                f.write(f"\n... 还有 {no_lyrics - 30} 个文件\n")
            f.write("\n" + "=" * 100 + "\n\n")
        
        # 读取错误
        if read_error > 0:
            f.write(f"【读取错误】({read_error} 个文件)\n")
            f.write("-" * 100 + "\n")
            for i, item in enumerate(results['read_error'][:20], 1):
                f.write(f"{i}. 音乐: {os.path.relpath(item['audio_file'], base_folder)}\n")
                f.write(f"   原因: {item['reason']}\n")
            if read_error > 20:
                f.write(f"\n... 还有 {read_error - 20} 个文件\n")
            f.write("\n" + "=" * 100 + "\n\n")
        
        # 时长匹配的文件（摘要）
        if matched > 0:
            f.write(f"【时长匹配】({matched} 个文件 ✓)\n")
            f.write("-" * 100 + "\n")
            for i, item in enumerate(results['matched'][:10], 1):
                f.write(f"{i}. {os.path.relpath(item['audio_file'], base_folder)} ({item['audio_duration_str']}) - 差异: {item['diff']:.2f}s\n")
            if matched > 10:
                f.write(f"\n... 还有 {matched - 10} 个文件\n")
            f.write("\n" + "=" * 100 + "\n")
    
    return report_path


def main():
    if not MUTAGEN_AVAILABLE:
        print("错误: 需要安装 mutagen 库")
        print("请运行: pip install mutagen")
        return
    
    base_folder = None
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        base_folder = sys.argv[1]
    
    # 如果没有提供路径，交互式选择
    if base_folder is None:
        print("=" * 100)
        print("音乐文件与歌词时长比较工具")
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
            # 默认使用脚本上级目录
            base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 确保路径存在
    if not os.path.isdir(base_folder):
        print(f"错误: 路径 '{base_folder}' 不存在或不是目录")
        return
    
    print("=" * 100)
    print("开始比较音乐文件与歌词时长...")
    print(f"基础文件夹: {base_folder}")
    print(f"时长误差容限: {CONFIG['TIME_TOLERANCE_SECONDS']} 秒")
    print("=" * 100)
    print()
    
    # 执行比较
    audio_count, results = compare_audio_lyrics(base_folder)
    
    # 生成报告
    report_path = generate_report(base_folder, audio_count, results)
    
    # 打印摘要
    matched = len(results['matched'])
    mismatched = len(results['mismatched'])
    no_lyrics = len(results['no_lyrics'])
    read_error = len(results['read_error'])
    
    print(f"比较完成！")
    print(f"总音乐文件数: {audio_count}")
    print(f"  ✓ 时长匹配: {matched} 个")
    print(f"  ✗ 时长不匹配: {mismatched} 个")
    print(f"  - 没有歌词: {no_lyrics} 个")
    print(f"  ⚠ 读取错误: {read_error} 个")
    
    if audio_count - read_error > 0:
        match_rate = matched / (audio_count - read_error) * 100
        print(f"  匹配率: {match_rate:.2f}%")
    
    print(f"\n报告已保存到: {report_path}")
    
    # 如果有不匹配的文件，打印到控制台
    if mismatched > 0:
        print("\n" + "=" * 100)
        print("时长不匹配文件 (前10个):")
        print("=" * 100)
        for i, item in enumerate(results['mismatched'][:10], 1):
            audio_rel = os.path.relpath(item['audio_file'], base_folder)
            print(f"{i}. 音乐: {audio_rel}")
            print(f"   音乐时长: {item['audio_duration_str']} | 歌词时长: {item['lyrics_duration_str']} | 误差: {item['diff']:.2f}s")
        
        if mismatched > 10:
            print(f"\n... 还有 {mismatched - 10} 个不匹配的文件，详见报告")


if __name__ == "__main__":
    main()
