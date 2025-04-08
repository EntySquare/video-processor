from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
from fastapi.staticfiles import StaticFiles
import mimetypes
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

# 挂载静态文件目录
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

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
        success = await tts_service.generate_audio(prompt, str(audio_path))
        print(f"音频生成{'成功' if success else '失败'}")
    
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
    
    # 获取文件信息
    file_stat = Path(output_path).stat()
    
    response_data = {
        "status": "success",
        "video_id": session_id,
        "metadata": {
            "filename": f"video_{session_id}.mp4",
            "file_size": file_stat.st_size,
            "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
            "resolution": resolution,
            "fps": fps
        },
        "urls": {
            "download": f"/outputs/{session_id}.mp4",
            "preview": f"/preview/{session_id}",
            "stream": f"/stream/{session_id}"
        }
    }
    
    return JSONResponse(content=response_data)
    
@app.get("/preview/{video_id}")
async def preview_video(video_id: str):
    video_path = Path(OUTPUT_DIR) / f"{video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="视频不存在")
        
    # 返回文件下载响应
    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"video_{session_id}.mp4",
        headers={
            "Content-Disposition": f"inline; filename=video_{session_id}.mp4"
        }
    )
