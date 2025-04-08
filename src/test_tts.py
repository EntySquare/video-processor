import asyncio
from services.tts_service import TTSService

async def test_tts():
    try:
        tts = TTSService()
        success = await tts.generate_audio(
            text="这是一段测试文本",
            output_path="output.mp3",
            speed=1.2
        )
        print(f"音频生成{'成功' if success else '失败'}")
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_tts())