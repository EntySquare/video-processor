import unittest
import os
import tempfile
from pathlib import Path
from processors.video_converter import VideoConverter

class TestVideoConverter(unittest.TestCase):
    def setUp(self):
        self.converter = VideoConverter()
        # 创建临时测试文件夹
        self.temp_dir = tempfile.mkdtemp()
        self.sample_input = os.path.join(self.temp_dir, "sample_input.mp4")
        self.sample_output = os.path.join(self.temp_dir, "sample_output.mp4")
        
        # 创建一个测试视频文件
        with open(self.sample_input, 'w') as f:
            f.write('dummy video content')

    def tearDown(self):
        # 清理临时文件
        for file in [self.sample_input, self.sample_output]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)

    def test_convert_to_vertical(self):
        """测试视频转换为竖屏"""
        try:
            self.converter.convert_to_vertical(
                self.sample_input,
                self.sample_output,
                resolution="1080x1920"
            )
        except Exception as e:
            self.fail(f"视频转换失败: {str(e)}")

    def test_crop_to_vertical(self):
        """测试视频裁剪为竖屏"""
        try:
            self.converter.crop_to_vertical(
                self.sample_input,
                self.sample_output,
                crop_width=608,
                crop_height=1080,
                x_offset=656
            )
        except Exception as e:
            self.fail(f"视频裁剪失败: {str(e)}")

    def test_invalid_input_file(self):
        """测试无效的输入文件"""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_to_vertical(
                "nonexistent.mp4",
                self.sample_output
            )

    def test_invalid_resolution(self):
        """测试无效的分辨率参数"""
        with self.assertRaises(ValueError):
            self.converter.convert_to_vertical(
                self.sample_input,
                self.sample_output,
                resolution="invalid"
            )

if __name__ == '__main__':
    unittest.main()