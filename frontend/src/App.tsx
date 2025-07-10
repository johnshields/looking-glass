import { useEffect, useState } from "react";
import "./App.css";

// Define the structure of a log entry
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
  // React state for holding all log entries
  const [logs, setLogs] = useState<LogEntry[]>([]);

  // ---------------- FETCH LOGS ---------------- //

  // useEffect to fetch logs on initial component mount
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

  // ---------------- CREATE NEW LOG ---------------- //

  // Create a new daily log via prompts and send to backend
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

      // Attempt to parse the returned new log
      const responseText = await response.text();
      if (responseText) {
        try {
          const createdLog = JSON.parse(responseText);
          // Prepend new log to UI
          setLogs((prev) => [createdLog, ...prev]);
        } catch {
          // Fallback: fetch all logs again if response is not parseable
          const refreshed = await fetch("http://127.0.0.1:8080/api/logs");
          const logsData = await refreshed.json();
          setLogs(logsData);
        }
      } else {
        // No response body: fetch logs again just in case
        const refreshed = await fetch("http://127.0.0.1:8080/api/logs");
        const logsData = await refreshed.json();
        setLogs(logsData);
      }
    } catch (err) {
      alert("Failed to save entry. Try again.");
    }
  };

  // ---------------- UPDATE EXISTING LOG ---------------- //

  const handleUpdateEntry = async (log: LogEntry) => {
    const updatedTitle = prompt("Update title:", log.title);
    const updatedEntries = prompt("Update entry text:", log.entries);
    const updatedMood = prompt("Update mood:", log.mood);

    // Convert array of tags to comma-separated string for editing
    const cleanedTags = log.tags.toString().replace(/[\[\]"]/g, "");

    const updatedTagsInput = prompt(
      "Update tags (comma-separated):",
      cleanedTags
    );

    const updatedTags = updatedTagsInput
      ? updatedTagsInput
          .split(",")
          .map((tag) => tag.trim())
          .filter((tag) => tag.length > 0)
      : [];

    // Skip update if any required fields are missing
    if (!updatedTitle || !updatedEntries || !updatedMood) return;

    const updatedLog = {
      title: updatedTitle,
      entries: updatedEntries,
      mood: updatedMood,
      tags: updatedTags,
      log_date: log.log_date, // Keep original log date
    };

    try {
      const response = await fetch(`http://127.0.0.1:8080/api/logs/${log.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedLog),
      });

      if (!response.ok) throw new Error("Failed to update entry");

      // Update log in UI
      setLogs((prevLogs) =>
        prevLogs.map((l) => (l.id === log.id ? { ...l, ...updatedLog } : l))
      );
    } catch {
      alert("Failed to update entry. Try again.");
    }
  };

  // ---------------- DELETE LOG ---------------- //

  const handleDelete = async (id: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this entry?"
    );
    if (!confirmed) return;

    try {
      const response = await fetch(`http://127.0.0.1:8080/api/logs/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Failed to delete log");

      // Remove from UI
      setLogs((prevLogs) => prevLogs.filter((log) => log.id !== id));
    } catch {
      alert("Failed to delete log. Try again.");
    }
  };

  // ---------------- RENDER UI ---------------- //

  return (
    // Full screen container with dark theme
    <div className="min-h-screen flex flex-col items-center bg-zinc-900 text-white font-sans">

      {/* Header with app name and description */}
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

      <main className="app-container py-8">
        {/* Section heading and new log button */}
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

        {/* Render each log entry */}
        <div className="log-grid">
          {logs.map((log) => (
            <div key={log.id} className="log-window">
              <div className="log-header">
                <span className="log-title">
                  {log.title}&nbsp;-&nbsp;
                  {new Date(log.log_date).toLocaleDateString("en-US", {
                    month: "long",
                    day: "numeric",
                  })}{" "}
                </span>
                {/* Edit and delete buttons */}
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
                {/* Date + mood */}
                <p className="text-sm text-gray-400 mb-2">
                  {new Date(log.log_date).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })}{" "}
                  — <span className="capitalize">{log.mood}</span>
                </p>

                {/* Entries (convert dashes to bullet formatting) */}
                <p className="mb-2 whitespace-pre-line">
                  {log.entries.replace(/(?!^)-/g, "\n-")}
                </p>

                {/* Display tags in brackets */}
                <p className="text-xs text-blue-300">
                  Tags:{" "}
                  {log.tags
                    .toString()
                    .replace(/^\[|\]$/g, "")
                    .replace(/"/g, "")
                    .split(",")
                    .map((tag: string, index: number) => `[${tag.trim()}]`)
                    .join(" ")}
                </p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
