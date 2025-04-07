import sys
import glob
import os
from processors.video_converter import VideoConverter
from processors.image_merger import ImageMerger

def main():
    merger = ImageMerger()

    # 示例：视频转换
    input_video = "input.mp4"
    output_video = "output.mp4"
    resolution = "1080x1920"

    # 示例1: 基本用法
    images = [
        "images/img001.jpeg",
        "images/img002.jpeg",
        "images/img003.jpeg"
    ]
    merger.merge_images_to_video(
        image_paths=images,
        output_path="output1.mp4"
    )
    
    # 示例2: 自定义帧率和分辨率
    merger.merge_images_to_video(
        image_paths=images,
        output_path="output2.mp4",
        frame_rate=60,
        resolution=resolution
    )
    
    # 示例3: 使用通配符获取所有图片
    all_images = sorted(glob.glob("images/*.jpeg"))
    merger.merge_images_to_video(
        image_paths=all_images,
        output_path="output3.mp4"
    )

    # converter = VideoConverter()

    # # 转换视频并添加背景音乐
    # converter.convert_to_vertical(
    #     input_file="input.mp4",
    #     output_file="output.mp4",
    #     audio_file="background.mp3",
    #     audio_volume=0.5  # 设置音量为原来的50%
    # )

    # # 单独为视频添加背景音乐
    # converter.add_audio_to_video(
    #     video_file="input.mp4",
    #     audio_file="music.mp3",
    #     output_file="output_with_music.mp4",
    #     audio_volume=0.7,
    #     start_time="00:00:10",  # 从10秒开始
    #     duration="00:01:00"     # 持续1分钟
    # )

if __name__ == "__main__":
    main()