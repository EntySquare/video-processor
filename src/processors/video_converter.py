import subprocess
import os
from typing import Optional

class VideoConverter:
    def convert_to_vertical(self, input_file: str, output_file: str, audio_file: Optional[str] = None, 
                          audio_volume: float = 1.0):
        """转换视频为竖屏，可选添加背景音乐"""
        if audio_file:
            command = [
                'ffmpeg',
                '-i', input_file,
                '-i', audio_file,
                '-filter_complex', f'[0:v]scale=1080:1920,setsar=1[v];[1:a]volume={audio_volume}[a]',
                '-map', '[v]',
                '-map', '[a]',
                '-shortest',
                '-c:a', 'aac',
                output_file
            ]
        else:
            command = [
                'ffmpeg',
                '-i', input_file,
                '-vf', 'scale=1080:1920,setsar=1',
                '-c:a', 'copy',
                output_file
            ]
        self.run_ffmpeg_command(command)

    def crop_video(self, input_file: str, output_file: str, crop_width: int, crop_height: int, 
                  x_offset: int, y_offset: int, audio_file: Optional[str] = None, 
                  audio_volume: float = 1.0):
        """裁剪视频并转换为竖屏，可选添加背景音乐"""
        if audio_file:
            command = [
                'ffmpeg',
                '-i', input_file,
                '-i', audio_file,
                '-filter_complex', 
                f'[0:v]crop={crop_width}:{crop_height}:{x_offset}:{y_offset},scale=1080:1920,setsar=1[v];[1:a]volume={audio_volume}[a]',
                '-map', '[v]',
                '-map', '[a]',
                '-shortest',
                '-c:a', 'aac',
                output_file
            ]
        else:
            command = [
                'ffmpeg',
                '-i', input_file,
                '-vf', f'crop={crop_width}:{crop_height}:{x_offset}:{y_offset},scale=1080:1920,setsar=1',
                '-c:a', 'copy',
                output_file
            ]
        self.run_ffmpeg_command(command)

    def merge_audio_video(self, video_file: str, audio_file: str, output_file: str):
        """
        合并独立的音频和视频文件
        
        Args:
            video_file: 视频文件路径
            audio_file: 音频文件路径
            output_file: 输出文件路径
        """
        # 验证文件存在
        for file in [video_file, audio_file]:
            if not os.path.exists(file):
                raise FileNotFoundError(f"文件不存在: {file}")
        
        # 合并音频和视频
        command = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-map', '0:v',       # 保留视频流
            '-map', '1:a',       # 保留音频流
            output_file
        ]
        
        self.run_ffmpeg_command(command)

    def add_background_music(self, video_file: str, audio_file: str, output_file: str, 
                            audio_volume: float = 1.0, start_time: Optional[str] = None, 
                            duration: Optional[str] = None):
        """为视频添加背景音乐，可控制音量和时长"""
        # 混合音频流：视频音频和背景音乐
        filter_complex = f'[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2,volume={audio_volume}[a]'
        
        command = ['ffmpeg', '-i', video_file, '-i', audio_file]
        
        if start_time:
            command.extend(['-ss', start_time])
        if duration:
            command.extend(['-t', duration])
        
        # 将背景音乐和原始音频流混合
        command.extend([
            '-filter_complex', filter_complex,
            '-map', '0:v',         # 保留视频流
            '-map', '[a]',         # 混合后的音频流
            '-shortest',
            '-c:v', 'copy',
            '-c:a', 'aac',
            output_file
        ])
        
        self.run_ffmpeg_command(command)


    def run_ffmpeg_command(self, command):
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg命令执行失败: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError("找不到FFmpeg，请确保已安装FFmpeg并添加到系统路径")