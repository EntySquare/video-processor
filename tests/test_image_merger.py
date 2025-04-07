import unittest
from src.processors.image_merger import ImageMerger

class TestImageMerger(unittest.TestCase):

    def setUp(self):
        self.image_merger = ImageMerger()

    def test_merge_images_to_video(self):
        image_list = ['image1.jpg', 'image2.jpg', 'image3.jpg']
        output_video = 'output_video.mp4'
        
        # Assuming the merge_images_to_video method returns a boolean indicating success
        result = self.image_merger.merge_images_to_video(image_list, output_video)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()