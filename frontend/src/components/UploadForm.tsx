import { useState, useRef } from 'react';

interface UploadFormProps {
  onUploadSuccess: (taskId: string) => void;
}

export default function UploadForm({ onUploadSuccess }: UploadFormProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [images, setImages] = useState<File[]>([]);
  const promptRef = useRef<HTMLTextAreaElement>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setImages(files);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData();
    
    // 添加图片文件
    images.forEach((image) => {
      formData.append('images', image);
    });

    // 添加音频文件
    const bgmInput = e.currentTarget.querySelector('input[name="bgm"]') as HTMLInputElement;
    if (bgmInput?.files?.[0]) {
      formData.append('bgm', bgmInput.files[0]);
    }

    // 添加其他参数
    formData.append('prompt', promptRef.current?.value || '');
    formData.append('fps', '30');
    formData.append('resolution', '1080x1920');
    formData.append('music_volume', '0.5');

    setUploading(true);
    setError('');

    try {
      const response = await fetch('https://audio.enty.services/v1/generate_video', {
        method: 'POST',
        body: formData,
        // 设置超时
        signal: AbortSignal.timeout(30000)
      });
      
      if (!response.ok) throw new Error('上传失败');
      
      const data = await response.json();
      onUploadSuccess(data.video_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : '上传出错');
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <label className="block">
          <span className="text-gray-700">上传图片（支持多选）</span>
          <input
            type="file"
            multiple
            accept="image/*"
            onChange={handleImageChange}
            required
            className="mt-1 block w-full"
          />
        </label>
        
        <label className="block">
          <span className="text-gray-700">背景音乐</span>
          <input
            type="file"
            name="bgm"
            accept="audio/*"
            required
            className="mt-1 block w-full"
          />
        </label>

        <label className="block">
          <span className="text-gray-700">文案提示</span>
          <textarea
            ref={promptRef}
            required
            rows={4}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </label>
      </div>

      {error && <p className="text-red-500">{error}</p>}
      <div className="flex items-center space-x-2">
        <button
          type="submit"
          disabled={uploading || images.length === 0}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-400"
        >
          {uploading ? '生成中...' : '开始生成'}
        </button>
        {images.length > 0 && (
          <span className="text-sm text-gray-600">
            已选择 {images.length} 张图片
          </span>
        )}
      </div>
    </form>
  );
}
