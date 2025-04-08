
# 视频处理工具

这个项目是一个视频处理工具，旨在使用 `ffmpeg` 将视频转换为 9:16 纵向比例，并合成视频。

## 功能

- **视频转换**：将视频转换为 9:16 纵向比例。
- **视频裁剪**：裁剪视频到指定尺寸。
- **图片合成视频**：将一组图片合成一个视频。

## 安装

请确保你已经安装了 `ffmpeg`。你可以通过以下命令安装所需的 Python 库：

```bash

# 安装中文字体
sudo apt update
sudo apt install fonts-noto-cjk

pip install -r requirements.txt
```

## 使用

```bash
python main.py \
  --image-dir ./images \
  --output final.mp4 \
  --subtitle subtitles.srt \
  --audio voice.mp3 \
  --music bgm.mp3 \
  --resolution 1080x1920 \
  --fps 30 \
  --music-volume 0.5
```
curl -X POST "https://audio.enty.services/v1/generate_video" \
  -F "images=@/Users/es/video-processor/src/images/img001.png" \
  -F "images=@/Users/es/video-processor/src/images/img002.png" \
  -F "images=@/Users/es/video-processor/src/images/img003.png" \
  -F "images=@/Users/es/video-processor/src/images/img004.png" \
  -F "images=@/Users/es/video-processor/src/images/img005.png" \
  -F "images=@/Users/es/video-processor/src/images/img006.jpeg" \
  -F "prompt=在这个快节奏的时代，我们深知您对品质生活的追求。我们始终坚持以创新为驱动，以品质为核心，为您提供卓越的产品和服务。我们的产品，不仅是功能性的体现，更是情感的寄托，是您美好生活的见证。 我们精选优质材料，采用先进工艺，力求每一个细节都精益求精。我们的服务，始终以客户为中心，用心倾听，耐心解答，为您提供全方位、个性化的解决方案。选择我们，就是选择品质，选择放心，选择美好的未来。我们期待与您携手，共创美好生活的新篇章。" \
  -F "bgm=@/Users/es/video-processor/src/bgm.mp3" \
  -F "fps=30" \
  -F "resolution=1080x1920" \
  -F "music_volume=0.5"


  curl -# -o downloaded_video.mp4 https:/audio.enty.services/v1/download/{video_id}

```json

```

1. **视频转换**：
   在 `main.py` 中调用 `VideoConverter` 类的 `convert_to_vertical` 方法。

2. **裁剪视频**：
   使用 `VideoConverter` 类的 `crop_video` 方法裁剪视频。

3. **合成视频**：
   使用 `ImageMerger` 类的 `merge_images_to_video` 方法将图片合成视频。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证

此项目采用 MIT 许可证。
