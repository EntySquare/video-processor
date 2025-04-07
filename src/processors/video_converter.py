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

    def add_audio_to_video(self, video_file: str, audio_file: str, output_file: str, 
                          audio_volume: float = 1.0, start_time: Optional[str] = None, 
                          duration: Optional[str] = None):
        """为视频添加背景音乐，可控制音量和时长"""
        filter_complex = f'[1:a]volume={audio_volume}[a]'
        
        command = ['ffmpeg', '-i', video_file, '-i', audio_file]
        
        if start_time:
            command.extend(['-ss', start_time])
        if duration:
            command.extend(['-t', duration])
            
        command.extend([
            '-filter_complex', filter_complex,
            '-map', '0:v',
            '-map', '[a]',
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