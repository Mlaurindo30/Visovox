import React from "react";
export default function OverlayViewer({ result }) {
  if (!result || !result.overlay_url) return null;
  return <img src={result.overlay_url} alt="Overlay" />;
} 