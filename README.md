# README.md

# 视频处理工具

这个项目是一个视频处理工具，旨在使用 `ffmpeg` 将视频转换为 9:16 纵向比例，并合成视频。

## 功能

- **视频转换**：将视频转换为 9:16 纵向比例。
- **视频裁剪**：裁剪视频到指定尺寸。
- **图片合成视频**：将一组图片合成一个视频。

## 安装

请确保你已经安装了 `ffmpeg`。你可以通过以下命令安装所需的 Python 库：

```bash
pip install -r requirements.txt
```

## 使用

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
