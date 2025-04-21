import React from 'react';

interface SessionHistoryProps {
  history: Array<{
    prompt: string;
    response: {
      video_path: string;
      audio_path: string;
      message: string;
    }
  }>;
  onSelect: (index: number) => void;
}

const SessionHistory: React.FC<SessionHistoryProps> = ({ history, onSelect }) => {
  if (history.length === 0) {
    return (
      <div className="card h-full">
        <h2 className="text-xl font-semibold mb-4">Session History</h2>
        <div className="py-8 text-center text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="mt-2">No animations yet</p>
          <p className="text-sm mt-1">Enter a prompt to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card h-full">
      <h2 className="text-xl font-semibold mb-4">Session History</h2>
      <ul className="space-y-3 max-h-[60vh] overflow-y-auto pr-2">
        {history.map((item, index) => (
          <li key={index}>
            <button
              onClick={() => onSelect(index)}
              className="w-full text-left p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-200"
            >
              <h3 className="font-medium text-sm line-clamp-2 text-gray-800">
                {item.prompt}
              </h3>
              <div className="flex items-center mt-2 text-xs text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                {formatTimestamp(new Date())}
              </div>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

function formatTimestamp(date: Date): string {
  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });
}

export default SessionHistory;