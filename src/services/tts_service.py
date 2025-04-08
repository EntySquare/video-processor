
from pathlib import Path
import edge_tts

class TTSService:
    async def generate_audio(self, text: str, output_path: str):
        """生成音频文件"""
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(output_path)