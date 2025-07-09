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

  // Fetch all logs on load
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

  // Create a new log entry
  const handleNewEntry = async () => {
    const title = prompt("Title for the log entry:");
    if (!title) return;

    const entries = prompt("What did you do today? (use - for bullets)");
    if (!entries) return;

    const mood = prompt("Mood (e.g. productive, chill, tired):") || "neutral";

    const tagsInput = prompt("Tags (comma-separated):");
    const tags = tagsInput
      ? tagsInput
          .split(",")
          .map((tag) => tag.trim().toLowerCase())
          .filter((tag) => tag.length > 0)
      : [];

    const log_date = new Date().toISOString().split("T")[0];

    const newEntry = { title, entries, mood, tags, log_date };

    try {
      const response = await fetch("http://127.0.0.1:8080/api/logs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newEntry),
      });

      if (!response.ok) throw new Error("Failed to submit log entry");

      const responseText = await response.text();
      if (responseText) {
        try {
          const createdLog = JSON.parse(responseText);
          setLogs((prev) => [createdLog, ...prev]);
        } catch {
          const refreshed = await fetch("http://127.0.0.1:8080/api/logs");
          const logsData = await refreshed.json();
          setLogs(logsData);
        }
      } else {
        const refreshed = await fetch("http://127.0.0.1:8080/api/logs");
        const logsData = await refreshed.json();
        setLogs(logsData);
      }
    } catch (err) {
      alert("Failed to save entry. Try again.");
    }
  };

  // Delete a log entry
  const handleDelete = async (id: string) => {
    const confirmed = window.confirm("Are you sure you want to delete this entry?");
    if (!confirmed) return;

    try {
      const response = await fetch(`http://127.0.0.1:8080/api/logs/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Failed to delete log");

      setLogs((prevLogs) => prevLogs.filter((log) => log.id !== id));
    } catch {
      alert("Failed to delete log. Try again.");
    }
  };

  // Update a log entry
  const handleUpdateEntry = async (log: LogEntry) => {
    const updatedTitle = prompt("Update title:", log.title);
    const updatedEntries = prompt("Update entry text:", log.entries);
    const updatedMood = prompt("Update mood:", log.mood);
    const updatedTagsInput = prompt("Update tags (comma-separated):", log.tags.join(", "));
    const updatedTags = updatedTagsInput
      ? updatedTagsInput.split(",").map((tag) => tag.trim())
      : [];

    if (!updatedTitle || !updatedEntries || !updatedMood) return;

    const updatedLog = {
      title: updatedTitle,
      entries: updatedEntries,
      mood: updatedMood,
      tags: updatedTags,
      log_date: log.log_date,
    };

    try {
      const response = await fetch(`http://127.0.0.1:8080/api/logs/${log.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedLog),
      });

      if (!response.ok) throw new Error("Failed to update entry");

      setLogs((prevLogs) =>
        prevLogs.map((l) => (l.id === log.id ? { ...l, ...updatedLog } : l))
      );
    } catch {
      alert("Failed to update entry. Try again.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-zinc-900 text-white font-sans">
      <header className="app-container border-b border-zinc-700 py-4 flex justify-between items-center">
        <div className="space-y-2">
          <h1 className="text-3xl font-extrabold tracking-wide">🪞LookingGlass</h1>
          <p className="text-sm text-gray-300">
            For tracking what you did today when the day disappears and you want to know where it went.
          </p>
        </div>
      </header>

      <main className="app-container py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">All Logs</h2>
          <button id="newEntryButton"
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
                  <span
                    className="dot blue cursor-pointer"
                    onClick={() => handleUpdateEntry(log)}
                    title="Edit log entry"
                  />
                  <span
                    className="dot red cursor-pointer"
                    onClick={() => handleDelete(log.id)}
                    title="Delete Entry"
                  />
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
                <div className="flex flex-wrap gap-1 text-xs mt-2">
                  {log.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="bg-blue-800 text-blue-100 px-2 py-1 rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
