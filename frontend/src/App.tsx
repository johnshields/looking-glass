// src/App.tsx
import { useEffect, useState } from "react";
import "./App.css";

interface LogEntry {
  id: string;
  title: string;
  entries: string;
  log_date: string;
  created_at: string;
  updated_at: string;
  mood: string;
  tags: string[];
}

export default function App() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/api/logs");
        if (!response.ok) throw new Error("Failed to fetch logs");
        const data: LogEntry[] = await response.json();
        setLogs(data);
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    };

    fetchLogs();
  }, []);

  const handleNewEntry = async () => {
    const title = prompt("Title for the log entry:");
    if (!title) return;

    const entries = prompt("What did you do today? (use - for bullets)");
    if (!entries) return;

    const mood = prompt("Mood (e.g. productive, chill, tired):") || "neutral";
    const tagsInput = prompt("Tags (comma-separated):");
    const tags = tagsInput ? tagsInput.split(",").map((tag) => tag.trim()) : [];

    const log_date = new Date().toISOString().split("T")[0]; // Today's date in YYYY-MM-DD

    const newEntry = {
      title,
      entries,
      mood,
      tags,
      log_date,
    };

    const response = await fetch("http://127.0.0.1:8080/api/logs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newEntry),
    });

    if (!response.ok) throw new Error("Failed to submit log entry");

    if (response.headers.get("Content-Type")?.includes("application/json")) {
      const createdLog = await response.json();
      setLogs((prev) => [createdLog, ...prev]);
    } else {
      const refreshed = await fetch("http://127.0.0.1:8080/api/logs");
      const logsData = await refreshed.json();
      setLogs(logsData);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-zinc-900 text-white font-sans">
      {/* Header */}
      <header className="app-container border-b border-zinc-700 py-4 flex justify-between items-center">
        <div className="space-y-2">
          <h1 className="text-3xl font-extrabold tracking-wide">
            🪞LookingGlass
          </h1>
          <p className="text-sm text-gray-300">
            For tracking what you did today when the day disappears and you want
            to know where it went.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-container py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">All Logs</h2>
          <button
            id="newEntryButton"
            onClick={handleNewEntry}
            className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded transition"
          >
            New Entry
          </button>
        </div>

        <div className="log-grid">
          {logs.map((log) => (
            <div key={log.id} className="log-window">
              <div className="log-header">
                <span className="log-title">{log.title}</span>
                <div className="log-controls">
                  <span className="dot blue" />
                  <span className="dot red" />
                </div>
              </div>
              <div className="log-body">
                <p className="text-sm text-gray-400 mb-2">
                  {new Date(log.log_date).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })}{" "}
                  — <span className="capitalize">{log.mood}</span>
                </p>
                <p className="mb-2 whitespace-pre-line">{log.entries}</p>
                <p className="text-xs text-blue-300">
                  Tags: {log.tags.join(", ")}
                </p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
