import React, { useState } from "react";

export default function UploadForm({ onTaskId }) {
  const [file, setFile] = useState(null);
  const [params, setParams] = useState('{"detect_mode": "YOLOFace"}');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("media_type", "image");
    formData.append("file", file);
    formData.append("params", params);
    const resp = await fetch("/scene_analysis/analyze", { method: "POST", body: formData });
    const data = await resp.json();
    onTaskId(data.task_id);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} />
      <input type="text" value={params} onChange={e => setParams(e.target.value)} />
      <button type="submit">Enviar</button>
    </form>
  );
} 