import subprocess
import os

class ImageMerger:
    def merge_images_to_video(self, image_paths, output_path, frame_rate=30, resolution='1080x1920'):
        if not image_paths:
            raise ValueError("Image paths list cannot be empty.")
        
        # Create a temporary text file to hold the image file paths
        with open('images.txt', 'w') as f:
            for image in image_paths:
                f.write(f"file '{os.path.abspath(image)}'\n")

        # Construct the ffmpeg command
        command = [
            'ffmpeg',
            '-r', str(frame_rate),
            '-f', 'concat',
            '-safe', '0',
            '-i', 'images.txt',
            '-s', resolution,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_path
        ]

        # Execute the ffmpeg command
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error occurred while merging images: {e}")
        finally:
            # Clean up the temporary file
            os.remove('images.txt')