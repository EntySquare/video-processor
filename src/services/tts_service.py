import io
import time
import os
from uuid import uuid4
from typing import Optional, Tuple
import edge_tts
import langid
from pathlib import Path
from dotenv import load_dotenv

class TTSService:
    def __init__(self, voice: str = 'zh-CN-XiaoxiaoNeural'):
        self.voice = voice
        self._init_language_list()
        
    def _init_language_list(self):
        self.language_list = [
            'zh-CN-XiaoxiaoNeural', 'zh-CN-YunyangNeural', 'zh-CN-YunxiNeural',
            'zh-CN-XiaoyiNeural', 'zh-CN-YunjianNeural', 'zh-CN-YunxiaNeural',
            'en-US-JennyNeural', 'en-US-GuyNeural', 'ja-JP-NanamiNeural',
            'ko-KR-SunHiNeural', 'fr-FR-DeniseNeural', 'de-DE-KatjaNeural'
        ]

    async def generate_audio(
        self, 
        text: str,
        output_path: str,
        speed: Optional[float] = None,
        voice: Optional[str] = None
    ) -> bool:
        """
        使用EdgeTTS生成音频
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            speed: 语速(0.5-2.0)
            voice: 指定语音，默认自动选择
        """
        try:
            # 确保输出目录存在
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 语言检测
            language, _ = langid.classify(text)
            if language == "zh":
                language = "zh-CN"
                
            # 选择语音
            target_voice = voice or self._select_voice(language)
            
            # 设置参数
            v_speed = 1.0 if speed is None else float(speed)
            v_speed = max(0.5, min(2.0, v_speed))
            
            # 构建TTS参数
            communicate = edge_tts.Communicate(
                text=text,
                voice=target_voice,
                rate=f"+{int(v_speed * 15)}%",
                pitch="+20Hz",
                volume="+110%"
            )

            # 生成音频
            await communicate.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"音频生成失败: {e}")
            return False
            
    def _select_voice(self, language: str) -> str:
        """根据语言选择合适的语音"""
        voices = [v for v in self.language_list if v.startswith(language)]
        return voices[0] if voices else self.voice