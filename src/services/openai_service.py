import openai
import whisper
from pathlib import Path

class OpenAIService:
    def __init__(self):
        self.model = whisper.load_model("base")
        
    def generate_subtitle(self, prompt: str, output_path: str):
        """生成字幕文件"""
        # 使用 OpenAI API 生成文本
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000
        )
        text = response.choices[0].text.strip()
        
        # 转换为SRT格式
        srt_content = self._convert_to_srt(text)
        Path(output_path).write_text(srt_content, encoding='utf-8')
        
    def _convert_to_srt(self, text: str) -> str:
        """将文本转换为SRT格式"""
        # 简单实现，可以根据需要完善
        lines = text.split("\n")
        srt = ""
        for i, line in enumerate(lines, 1):
            if line.strip():
                start_time = f"00:00:{i*5:02d},000"
                end_time = f"00:00:{(i+1)*5-1:02d},000"
                srt += f"{i}\n{start_time} --> {end_time}\n{line}\n\n"
        return srt
