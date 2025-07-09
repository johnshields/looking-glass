// src/App.tsx
import { useEffect, useState } from 'react';
import './App.css';

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
    const simulatedResponse: LogEntry = {
      created_at: '2025-07-09T13:48:42',
      entries: '- Worked on the API setup today.',
      id: 'f12a234c-d45b-11ec-9d64-0242ac120002',
      log_date: '2025-07-07',
      mood: 'productive',
      tags: ['work', 'api', 'python'],
      title: 'Monday Entry',
      updated_at: '2025-07-09T13:48:42',
    };

    setLogs([simulatedResponse]);
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center bg-zinc-900 text-white font-sans">
      {/* Header */}
      <header className="w-full max-w-7xl flex justify-between items-center px-6 py-4 border-b border-zinc-700">
        <h1 className="text-3xl font-extrabold tracking-wide">LookingGlass</h1>
      </header>

      {/* Main Content */}
      <main className="w-full max-w-7xl px-4 py-8">
        <div className="flex justify-between items-center mb-6 w-full">
        <h2 className="text-2xl font-bold">All Logs</h2>
        <button id="newEntryButton"
        className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded transition">
        New Entry
        </button>
    </div>

        <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
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
                  {new Date(log.log_date).toLocaleDateString()} —{' '}
                  <span className="capitalize">{log.mood}</span>
                </p>
                <p className="mb-2 whitespace-pre-line">{log.entries}</p>
                <p className="text-xs text-blue-300">Tags: {log.tags.join(', ')}</p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
