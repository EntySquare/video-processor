import argparse
import glob
import uuid
from pathlib import Path
from processors.video_converter import VideoConverter
from processors.image_merger import ImageMerger
from processors.srt import VideoSubtitler

def parse_args():
    parser = argparse.ArgumentParser(description='视频处理工具')
    parser.add_argument('--image-dir', type=str, default=None, help='图片目录路径')
    parser.add_argument('--image-dir', type=str, default=None, help='视频目录路径')
    parser.add_argument('--output', type=str, default='output.mp4', help='输出视频路径')
    parser.add_argument('--subtitle', type=str, help='字幕文件路径(.srt)')
    parser.add_argument('--audio', type=str, help='音频文件路径')
    parser.add_argument('--music', type=str, help='背景音乐文件路径')
    parser.add_argument('--resolution', type=str, default='1080x1920', help='视频分辨率(例如:1080x1920)')
    parser.add_argument('--fps', type=int, default=30, help='视频帧率')
    parser.add_argument('--music-volume', type=float, default=0.5, help='背景音乐音量(0-1)')
    return parser.parse_args()

def process_video(
    image_dir: str = None,  # 如果没有视频目录，可以使用图片目录
    video_dir: str = None,  # 支持视频目录
    output_path: str = None,
    subtitle_path: str = None,
    audio_path: str = None,
    music_path: str = None,
    fps: int = 30,
    resolution: str = "1080x1920",
    music_volume: float = 0.5
):
    # 确保输出目录存在
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    current_video = None
    temp_video = None
    subtitle_video = None
    audio_video = None

    # 如果提供了视频目录，处理视频文件
    if video_dir:
        video_files = sorted(glob.glob(f"{video_dir}/*.mp4"))
        if not video_files:
            raise ValueError(f"目录 {video_dir} 中未找到视频文件")
        
        # 如果是视频目录，直接使用第一个视频文件
        current_video = video_files[0]
    
    # 如果没有视频文件，使用图片目录合成视频
    if not current_video and image_dir:
        image_files = sorted(glob.glob(f"{image_dir}/*.[pjgPJG]*"))
        if not image_files:
            raise ValueError(f"目录 {image_dir} 中未找到图片文件")

        # 1. 合并图片为视频
        merger = ImageMerger()
        temp_video = f"temp_video_{uuid.uuid4()}.mp4"
        merger.merge_images_to_video(
            image_paths=image_files,
            output_path=temp_video,
            frame_rate=fps,
            resolution=resolution
        )
        current_video = temp_video
    
    # 2. 添加字幕(如果提供)
    if subtitle_path:
        subtitler = VideoSubtitler()
        subtitle_video = f"temp_subtitle_{uuid.uuid4()}.mp4"
        subtitler.burn_subtitles(
            video_path=current_video,
            subtitle_path=subtitle_path,
            output_path=subtitle_video
        )
        current_video = subtitle_video

    # 3. 添加音频(如果提供)
    if audio_path:
        converter = VideoConverter()
        audio_video = f"temp_audio_{uuid.uuid4()}.mp4"
        converter.merge_audio_video(
            video_file=current_video,
            audio_file=audio_path,
            output_file=audio_video
        )
        current_video = audio_video

    # 4. 添加背景音乐(如果提供)
    if music_path:
        converter = VideoConverter()
        converter.add_background_music(
            video_file=current_video,
            audio_file=music_path,
            output_file=output_path,
            audio_volume=music_volume
        )
    else:
        # 复制而不是重命名，以避免跨设备移动问题
        import shutil
        shutil.copy2(str(current_video), output_path)

    # 清理临时文件
    for temp_file in [temp_video, subtitle_video, audio_video]:
        if temp_file and Path(temp_file).exists():
            Path(temp_file).unlink()

def main():
    args = parse_args()
    process_video(
        image_dir=args.image_dir,
        video_dir=args.video_dir,
        output_path=args.output,
        subtitle_path=args.subtitle,
        audio_path=args.audio,
        music_path=args.music,
        fps=args.fps,
        resolution=args.resolution,
        music_volume=args.music_volume
    )

if __name__ == "__main__":
    main()
