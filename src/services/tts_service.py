from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

class TTSService:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 获取OpenAI配置
        api_key = os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_API_AUDIO_BASE', 'https://api.openai.com/v1')
        
        if not api_key:
            raise ValueError("未找到OPENAI_API_KEY环境变量")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    async def generate_audio(
        self, 
        text: str, 
        output_path: str,
        model: str = "tts-1",
        voice: str = "alloy"
    ) -> bool:
        """
        使用OpenAI TTS生成音频
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            model: TTS模型，默认tts-1
            voice: 声音类型(alloy/echo/fable/onyx/nova/shimmer)
        """
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            
            # 保存音频文件
            response.stream_to_file(output_path)
            return True
            
        except Exception as e:
            print(f"音频生成失败: {e}")
            return False