import subprocess
from pathlib import Path
import platform
import shlex

class VideoSubtitler:
    def _get_default_font(self):
        system = platform.system()
        if system == "Windows":
            return "SimHei"
        elif system == "Linux":
            return "Noto Sans CJK SC"
        else:  # MacOS
            return "PingFang SC"

    def burn_subtitles(
        self, 
        video_path: str, 
        subtitle_path: str, 
        output_path: str, 
        font_name: str = None,
        font_size: int = 24
    ) -> None:
        """
        将字幕文件烧录到视频中
        
        Args:
            video_path: 输入视频文件路径
            subtitle_path: 字幕文件路径(.srt格式)
            output_path: 输出视频文件路径
            font_name: 字体名称，默认根据系统选择中文字体
            font_size: 字幕字体大小，默认24
        """
        if not all(Path(p).exists() for p in [video_path, subtitle_path]):
            raise FileNotFoundError("视频文件或字幕文件不存在")
            
        if not subtitle_path.lower().endswith('.srt'):
            raise ValueError("字幕文件必须是.srt格式")

        # 使用默认字体或指定字体
        font = font_name or self._get_default_font()
        escaped_subtitle_path = shlex.quote(subtitle_path)
        
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles={escaped_subtitle_path}:force_style='FontName={font},FontSize={font_size},Alignment=2'",
            '-c:a', 'copy',
            output_path
        ]

        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stderr:
                print(f"警告信息: {result.stderr}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"添加字幕时发生错误: {e.stderr}")