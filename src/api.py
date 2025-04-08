from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import uuid
import os
from pathlib import Path
from services.openai_service import OpenAIService
from services.tts_service import TTSService
from main import process_video

app = FastAPI()
openai_service = OpenAIService()
tts_service = TTSService()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

@app.post("/generate_video")
async def process_video_api(
    images: list[UploadFile] = File(...),
    prompt: str = Form(None),
    fps: int = Form(30),
    resolution: str = Form("1080x1920"),
    music_volume: float = Form(0.5)
):
    # 创建临时目录
    session_id = str(uuid.uuid4())
    image_dir = Path(UPLOAD_DIR) / session_id / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存上传的图片
    image_paths = []
    for img in images:
        path = image_dir / img.filename
        content = await img.read()
        path.write_bytes(content)
        image_paths.append(str(path))
    
    # 生成字幕和音频
    if prompt:
        # OpenAI生成字幕
        subtitle_path = Path(UPLOAD_DIR) / session_id / "subtitle.srt"
        openai_service.generate_subtitle(prompt, str(subtitle_path))
        
        # TTS生成音频
        audio_path = Path(UPLOAD_DIR) / session_id / "audio.mp3"
        tts_service.generate_audio(prompt, str(audio_path))
    
    # 处理视频
    output_path = Path(OUTPUT_DIR) / f"{session_id}.mp4"
    process_video(
        image_dir=str(image_dir),
        output_path=str(output_path),
        subtitle_path=str(subtitle_path) if prompt else None,
        audio_path=str(audio_path) if prompt else None,
        fps=fps,
        resolution=resolution,
        music_volume=music_volume
    )
    
    return FileResponse(output_path)
