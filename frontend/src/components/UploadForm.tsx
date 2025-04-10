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
    if (!images.length) {
      setError('请选择至少一张图片');
      return;
    }

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
        headers: {
          'Accept': 'application/json',
        },
        signal: AbortSignal.timeout(300000) // 5分钟超时
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `上传失败 (${response.status})`);
      }
      
      const data = await response.json();
      console.group('视频生成响应');
      console.log('状态码:', response.status);
      console.log('响应数据:', data);
      console.log('视频ID:', data.video_id);
      console.log('元数据:', data.metadata);
      console.log('链接:', data.urls);
      console.groupEnd();
      onUploadSuccess(data.video_id);
    } catch (err) {
      console.error('上传错误:', err);
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
            className="mt-1 block w-full"
          />
          {images.length > 0 && (
            <span className="text-sm text-gray-500">
              已选择 {images.length} 张图片
            </span>
          )}
        </label>
        
        <label className="block">
          <span className="text-gray-700">背景音乐（可选）</span>
          <input
            type="file"
            name="bgm"
            accept="audio/*"
            className="mt-1 block w-full"
          />
        </label>

        <label className="block">
          <span className="text-gray-700">文案提示</span>
          <textarea
            ref={promptRef}
            rows={4}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="请输入文案提示..."
          />
        </label>
      </div>

      {error && (
        <div className="bg-red-50 text-red-500 p-4 rounded">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={uploading || images.length === 0}
        className={`w-full py-2 px-4 rounded transition-colors ${
          uploading || images.length === 0
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 text-white'
        }`}
      >
        {uploading ? '处理中...' : '开始生成'}
      </button>
    </form>
  );
}