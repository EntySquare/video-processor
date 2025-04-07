import sys
import glob
import os
from processors.video_converter import VideoConverter
from processors.image_merger import ImageMerger
from processors.srt import VideoSubtitler

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
    subtitler = VideoSubtitler()
    subtitler.burn_subtitles(
        video_path='output1.mp4',
        subtitle_path='subtitles.srt',
        output_path='output_with_subs.mp4',
        #font_name='SimHei'  # 可选，不指定则使用系统默认中文字体
    )

    converter = VideoConverter()
    # 添加人声
    converter.merge_audio_video(
        video_file='output_with_subs.mp4',
        audio_file='audio.mp3',
        output_file='output.mp4'
    )
    # 叠加背景音乐
    converter.add_background_music(
        video_file='output.mp4',
        audio_file='music.mp3',
        output_file='final.mp4',
        audio_volume=0.5,
    )

    # # 示例2: 自定义帧率和分辨率
    # merger.merge_images_to_video(
    #     image_paths=images,
    #     output_path="output2.mp4",
    #     frame_rate=60,
    #     resolution=(1080, 1920)
    # )
    
    # # 示例3: 使用通配符获取所有图片
    # all_images = sorted(glob.glob("images/*.jpeg"))
    # merger.merge_images_to_video(
    #     image_paths=all_images,
    #     output_path="output3.mp4"
    # )

if __name__ == "__main__":
    main()