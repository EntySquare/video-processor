import { useState } from 'react';
import UploadForm from '../components/UploadForm';
import ProcessingStatus from '../components/ProcessingStatus';

export default function Home() {
  const [taskId, setTaskId] = useState<string | null>(null);

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">视频处理工具</h1>
        {!taskId ? (
          <UploadForm onUploadSuccess={setTaskId} />
        ) : (
          <ProcessingStatus taskId={taskId} onReset={() => setTaskId(null)} />
        )}
      </div>
    </main>
  );
}
