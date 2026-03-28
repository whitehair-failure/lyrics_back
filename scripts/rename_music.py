import os
import sys
import re
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from mutagen.mp4 import MP4
from mutagen.asf import ASF
from mutagen.apev2 import APEv2
from mutagen.oggopus import OggOpus
from mutagen.oggflac import OggFLAC

def get_metadata(file_path):
    """获取音乐文件的艺术家和标题，支持多种格式"""
    try:
        ext = file_path.lower()
        audio = None
        artist = None
        title = None
        
        # MP3 格式
        if ext.endswith(".mp3"):
            audio = MP3(file_path, ID3=EasyID3)
            artist = audio.get("artist", [None])[0]
            title = audio.get("title", [None])[0]
        
        # FLAC 格式
        elif ext.endswith(".flac"):
            audio = FLAC(file_path)
            artist = audio.get("artist", [None])[0]
            title = audio.get("title", [None])[0]
        
        # OGG Vorbis 格式
        elif ext.endswith(".ogg") or ext.endswith(".oga"):
            try:
                audio = OggVorbis(file_path)
                artist = audio.get("artist", [None])[0]
                title = audio.get("title", [None])[0]
            except:
                # 尝试 OggFlac
                try:
                    audio = OggFLAC(file_path)
                    artist = audio.get("artist", [None])[0]
                    title = audio.get("title", [None])[0]
                except:
                    # 尝试 OggOpus
                    try:
                        audio = OggOpus(file_path)
                        artist = audio.get("artist", [None])[0]
                        title = audio.get("title", [None])[0]
                    except:
                        pass
        
        # WAV 格式
        elif ext.endswith(".wav"):
            audio = WAVE(file_path)
            artist = audio.get("artist", [None])[0] if audio.get("artist") else None
            title = audio.get("title", [None])[0] if audio.get("title") else None
        
        # M4A/AAC 格式 (MP4)
        elif ext.endswith(".m4a") or ext.endswith(".m4b") or ext.endswith(".mp4"):
            audio = MP4(file_path)
            artist = audio.get("\xa9ART", [None])[0] if audio.get("\xa9ART") else None
            title = audio.get("\xa9nam", [None])[0] if audio.get("\xa9nam") else None
        
        # WMA 格式 (ASF)
        elif ext.endswith(".wma"):
            audio = ASF(file_path)
            artist = audio.get("WM/AlbumArtist", [None])[0] if audio.get("WM/AlbumArtist") else None
            title = audio.get("Title", [None])[0] if audio.get("Title") else None
        
        # APE 格式
        elif ext.endswith(".ape") or ext.endswith(".wv"):
            audio = APEv2(file_path)
            artist = audio.get("Artist", [None])[0] if audio.get("Artist") else None
            title = audio.get("Title", [None])[0] if audio.get("Title") else None
        
        # Opus 格式
        elif ext.endswith(".opus"):
            audio = OggOpus(file_path)
            artist = audio.get("artist", [None])[0]
            title = audio.get("title", [None])[0]
        
        return artist, title
    except Exception as e:
        print(f"无法读取 {file_path} 的元数据: {e}")
        return None, None

def sanitize_filename(name):
    """清理文件名，替换不合法字符"""
    if not name:
        return None
    # 替换 Windows 文件名不允许的字符
    return re.sub(r'[\\/:*?"<>|]', '_', name)

def rename_music_files(folder_path):
    """扫描文件夹并重命名音乐文件"""
    # 支持的音乐文件扩展名
    supported_formats = {'.mp3', '.flac', '.ogg', '.oga', '.wav', '.m4a', '.m4b', 
                        '.mp4', '.wma', '.ape', '.wv', '.opus'}
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue
        
        # 检查是否是支持的音乐格式
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in supported_formats:
            continue
        
        artist, title = get_metadata(file_path)
        if artist and title:
            artist = sanitize_filename(artist)
            title = sanitize_filename(title)
            
            new_filename = f"{artist} - {title}{file_ext}"
            new_filepath = os.path.join(folder_path, new_filename)
            
            if new_filepath != file_path:
                try:
                    os.rename(file_path, new_filepath)
                    print(f"重命名: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"无法重命名 {filename}: {e}")

def main():
    if len(sys.argv) < 2:
        print("用法: python rename_music.py <文件夹路径>")
        print("\n支持的音乐格式:")
        print("  MP3 (.mp3)")
        print("  FLAC (.flac)")
        print("  OGG Vorbis (.ogg, .oga)")
        print("  WAV (.wav)")
        print("  M4A/AAC (.m4a, .m4b, .mp4)")
        print("  WMA (.wma)")
        print("  APE (.ape, .wv)")
        print("  Opus (.opus)")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("错误: 提供的路径不是文件夹")
        sys.exit(1)
    
    rename_music_files(folder_path)

if __name__ == "__main__":
    main()
