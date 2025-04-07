import subprocess
import os
import cv2

class ImageMerger:
    def merge_images_to_video(self, image_paths, output_path, frame_rate=30, duration_per_image=3, resolution=(1080, 1920)):
        if not image_paths:
            raise ValueError("Image paths list cannot be empty.")

        # 临时文件夹
        temp_dir = 'temp_frames'
        os.makedirs(temp_dir, exist_ok=True)

        # 每张图要生成多少帧
        frames_per_image = int(frame_rate * duration_per_image)
        frame_index = 0

        # 解析字符串格式的分辨率
        if isinstance(resolution, str) and 'x' in resolution:
            width, height = map(int, resolution.split('x'))
            resolution = (width, height)

        print("🔄 生成帧序列...")
        for image_path in image_paths:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Cannot read image: {image_path}")

            # resize 到统一分辨率
            img = cv2.resize(img, resolution)

            for _ in range(frames_per_image):
                frame_file = os.path.join(temp_dir, f"frame_{frame_index:05d}.jpg")
                cv2.imwrite(frame_file, img)
                frame_index += 1

        print("🎬 调用 ffmpeg 合成视频...")
        command = [
            'ffmpeg',
            '-y',
            '-framerate', str(frame_rate),
            '-i', os.path.join(temp_dir, 'frame_%05d.jpg'),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error occurred while merging images: {e}")
        finally:
            # 清理临时帧
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)
            print("✅ 清理完成")

