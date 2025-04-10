import { useState, useEffect } from 'react';

interface ProcessingStatusProps {
  taskId: string;
  onReset: () => void;
}

export default function ProcessingStatus({ taskId, onReset }: ProcessingStatusProps) {
  const [status, setStatus] = useState<string>('processing');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        // 使用预览 API 检查状态
        const response = await fetch(`https://audio.enty.services/v1/preview/${taskId}`);
        if (response.ok) {
          setStatus('completed');
        }
      } catch (error) {
        console.error('状态查询失败:', error);
      }
    };

    const interval = setInterval(checkStatus, 2000);
    return () => clearInterval(interval);
  }, [taskId]);

  const handleDownload = async () => {
    try {
      window.location.href = `https://audio.enty.services/v1/download/${taskId}`;
    } catch (error) {
      console.error('下载失败:', error);
    }
  };

  return (
    <div className="space-y-4">
      <div className="p-4 bg-gray-100 rounded-lg">
        <p>任务ID: {taskId}</p>
        <p>状态: {status}</p>
        {status === 'completed' && (
          <div className="mt-4 space-y-2">
            <a
              href={`https://audio.enty.services/v1/preview/${taskId}`}
              className="block text-blue-500 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              预览视频
            </a>
            <button
              onClick={handleDownload}
              className="bg-green-500 text-white px-4 py-2 rounded"
            >
              下载视频
            </button>
          </div>
        )}
      </div>
      <button
        onClick={onReset}
        className="bg-gray-500 text-white px-4 py-2 rounded"
      >
        生成新视频
      </button>
    </div>
  );
}
