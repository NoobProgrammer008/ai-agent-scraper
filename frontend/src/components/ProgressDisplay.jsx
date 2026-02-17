import React from "react";

export default function ProgressDisplay({ progress }) {
  const getStatusColor = (status) => {
    switch (status) {
      case "started":
        return "#3498db";
      case "progress":
        return "#f39c12";
      case "completed":
        return "#27ae60";
      case "error":
        return "#e74c3c";
      default:
        return "#95a5a6";
    }
  };

  const getStatusEmoji = (status) => {
    switch (status) {
      case "started":
        return "🚀";
      case "progress":
        return "⏳";
      case "completed":
        return "✅";
      case "error":
        return "❌";
      default:
        return "❓";
    }
  };

  if (!progress) return null;

  return (
    <div
      style={{
        padding: "20px",
        margin: "20px",
        border: `3px solid ${getStatusColor(progress.status)}`,
        borderRadius: "5px",
        backgroundColor: "#f9f9f9",
      }}
    >
      <h2>
        {getStatusEmoji(progress.status)} {progress.status.toUpperCase()}
      </h2>

      <p>
        <strong>Message:</strong> {progress.message}
      </p>

      {progress.status === "progress" && (
        <>
          {progress.task && (
            <p>
              <strong>Task:</strong> {progress.task}
            </p>
          )}
          {progress.tool_calls && (
            <p>
              <strong>Tool Calls:</strong> {progress.tool_calls}
            </p>
          )}
        </>
      )}

      {progress.status === "completed" && (
        <div style={{ marginTop: "20px" }}>
          <h3>📊 Results:</h3>
          <div
            style={{
              backgroundColor: "white",
              padding: "15px",
              borderRadius: "5px",
              maxHeight: "300px",
              overflowY: "auto",
              fontFamily: "monospace",
              fontSize: "12px",
              whiteSpace: "pre-wrap",
            }}
          >
            {typeof progress.results === "string"
              ? progress.results
              : JSON.stringify(progress.results, null, 2)}
          </div>
          {progress.result_id && (
            <p style={{ marginTop: "10px", color: "#666" }}>
              Result ID: {progress.result_id}
            </p>
          )}
        </div>
      )}

      {progress.status === "error" && (
        <p style={{ color: "#e74c3c", fontSize: "16px" }}>
          {progress.message}
        </p>
      )}
    </div>
  );
}