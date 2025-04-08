from openai import OpenAI
import whisper
from pathlib import Path
import os
from typing import Optional
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        # 获取配置
        api_key = os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not api_key:
            raise ValueError("未找到OPENAI_API_KEY环境变量")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        # 加载Whisper模型
        try:
            self.whisper_model = whisper.load_model("base")
        except Exception as e:
            print(f"Whisper模型加载失败: {e}")
            self.whisper_model = None
        
    def generate_subtitle(self, prompt: str, output_path: str) -> bool:
        """生成字幕文件"""
        try:
            # 使用 GPT-4o-mini 生成文本
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个专业的视频字幕生成助手，请生成简洁有力的字幕内容。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            text = response.choices[0].message.content.strip()
            
            # 转换为SRT格式
            srt_content = self._convert_to_srt(text)
            Path(output_path).write_text(srt_content, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"字幕生成失败: {e}")
            return False
        
    def _convert_to_srt(self, text: str) -> str:
        """将文本转换为SRT格式"""
        lines = text.split("\n")
        srt = ""
        
        current_time = 0
        duration = 3  # 每条字幕显示3秒
        
        for i, line in enumerate(lines, 1):
            if line.strip():
                start_time = self._format_time(current_time)
                end_time = self._format_time(current_time + duration)
                srt += f"{i}\n{start_time} --> {end_time}\n{line}\n\n"
                current_time += duration
                
        return srt
        
    def _format_time(self, seconds: int) -> str:
        """将秒数转换为SRT时间格式"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d},000"