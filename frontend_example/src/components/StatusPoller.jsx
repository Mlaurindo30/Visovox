import React, { useEffect, useState } from "react";

export default function StatusPoller({ taskId, onResult }) {
  const [status, setStatus] = useState("queued");
  useEffect(() => {
    if (!taskId) return;
    let interval = setInterval(async () => {
      const resp = await fetch(`/scene_analysis/status/${taskId}`);
      const data = await resp.json();
      setStatus(data.status);
      if (data.status === "success" || data.status === "failure") {
        clearInterval(interval);
        onResult(data.result);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [taskId]);
  return <div>Status: {status}</div>;
} 