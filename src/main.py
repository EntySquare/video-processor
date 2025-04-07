import argparse
import glob
import uuid
from pathlib import Path
from processors.video_converter import VideoConverter
from processors.image_merger import ImageMerger
from processors.srt import VideoSubtitler

def parse_args():
    parser = argparse.ArgumentParser(description='视频处理工具')
    parser.add_argument('--image-dir', type=str, required=True, help='图片目录路径')
    parser.add_argument('--output', type=str, default='output.mp4', help='输出视频路径')
    parser.add_argument('--subtitle', type=str, help='字幕文件路径(.srt)')
    parser.add_argument('--audio', type=str, help='音频文件路径')
    parser.add_argument('--music', type=str, help='背景音乐文件路径')
    parser.add_argument('--resolution', type=str, default='1080x1920', help='视频分辨率(例如:1080x1920)')
    parser.add_argument('--fps', type=int, default=30, help='视频帧率')
    parser.add_argument('--music-volume', type=float, default=0.5, help='背景音乐音量(0-1)')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 获取所有图片，包括png和其他格式
    image_files = sorted(glob.glob(f"{args.image_dir}/*.[pjgPJG]*"))
    if not image_files:
        raise ValueError(f"目录 {args.image_dir} 中未找到图片文件")

    # 1. 合并图片为视频
    merger = ImageMerger()
    temp_video = f"temp_video_{uuid.uuid4()}.mp4"
    merger.merge_images_to_video(
        image_paths=image_files,
        output_path=temp_video,
        frame_rate=args.fps,
        resolution=args.resolution
    )
    
    current_video = temp_video
    
    # 2. 添加字幕(如果提供)
    if args.subtitle:
        subtitler = VideoSubtitler()
        subtitle_video = f"temp_subtitle_{uuid.uuid4()}.mp4"
        subtitler.burn_subtitles(
            video_path=current_video,
            subtitle_path=args.subtitle,
            output_path=subtitle_video
        )
        current_video = subtitle_video

    # 3. 添加音频(如果提供)
    if args.audio:
        converter = VideoConverter()
        audio_video = f"temp_audio_{uuid.uuid4()}.mp4"
        converter.merge_audio_video(
            video_file=current_video,
            audio_file=args.audio,
            output_file=audio_video
        )
        current_video = audio_video

    # 4. 添加背景音乐(如果提供)
    if args.music:
        converter = VideoConverter()
        converter.add_background_music(
            video_file=current_video,
            audio_file=args.music,
            output_file=args.output,
            audio_volume=args.music_volume
        )
    else:
        # 如果没有背景音乐，重命名最后的临时文件
        Path(current_video).rename(args.output)

    # 清理临时文件
    for temp_file in [temp_video, subtitle_video, audio_video]:
        if Path(temp_file).exists():
            Path(temp_file).unlink()

if __name__ == "__main__":
    main()
