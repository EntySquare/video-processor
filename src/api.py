from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)
openai_service = OpenAIService()
tts_service = TTSService()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

# 挂载静态文件目录
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.post("/v1/generate_video")
async def process_video_api(
    images: list[UploadFile] = File(..., description="图片文件列表"),
    prompt: str = Form(None, description="提示文本，用于生成字幕和语音"),
    bgm: UploadFile = File(None, description="背景音乐文件"),
    fps: int = Form(30, description="视频帧率"),
    resolution: str = Form("1080x1920", description="视频分辨率"),
    music_volume: float = Form(0.5, description="背景音乐音量"),
):
    # 创建临时目录
    session_id = str(uuid.uuid4())
    image_dir = Path(UPLOAD_DIR) / session_id / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = Path(UPLOAD_DIR) / session_id
    # 如果提供了背景音乐，保存文件
    bgm_path = None
    if bgm:
        bgm_path = temp_dir / f"bgm{Path(bgm.filename).suffix}"
        content = await bgm.read()
        bgm_path.write_bytes(content)

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
        music_path=str(bgm_path) if bgm else None,
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
    
@app.get("/v1/download/{video_id}")
async def download_video(video_id: str):
    video_path = Path(OUTPUT_DIR) / f"{video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="视频不存在")
        
    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=f"video_{video_id}.mp4",
        headers={
            "Content-Disposition": f"attachment; filename=video_{video_id}.mp4",
            "Content-Type": "video/mp4"
        }
    )
    
@app.get("/v1/preview/{video_id}")
async def preview_video(video_id: str):
    video_path = Path(OUTPUT_DIR) / f"{video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="视频不存在")
        
    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=f"video_{video_id}.mp4",
        headers={
            "Content-Disposition": f"inline; filename=video_{video_id}.mp4",
            "Content-Type": "video/mp4",
            "Accept-Ranges": "bytes"
        }
    )