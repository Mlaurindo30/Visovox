export async function analyzeScene(file, params) {
  const formData = new FormData();
  formData.append("media_type", "image");
  formData.append("file", file);
  formData.append("params", JSON.stringify(params));
  const resp = await fetch("/scene_analysis/analyze", { method: "POST", body: formData });
  return await resp.json();
}

export async function getSceneStatus(taskId) {
  const resp = await fetch(`/scene_analysis/status/${taskId}`);
  return await resp.json();
} 