import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import StatusPoller from "./components/StatusPoller";
import OverlayViewer from "./components/OverlayViewer";

export default function App() {
  const [taskId, setTaskId] = useState(null);
  const [result, setResult] = useState(null);
  return (
    <div>
      <h1>VisioVox Fusion - Scene Analysis Demo</h1>
      <UploadForm onTaskId={setTaskId} />
      {taskId && <StatusPoller taskId={taskId} onResult={setResult} />}
      <OverlayViewer result={result} />
    </div>
  );
} 