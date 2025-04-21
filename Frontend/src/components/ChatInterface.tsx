import React, { useState } from 'react';
import axios from 'axios';

interface ChatInterfaceProps {
  onSubmit: (prompt: string, response: any) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Call the backend API to generate animation
      const response = await axios.post('http://localhost:5000/api/generate', {
        prompt: prompt.trim()
      });
      
      // Pass the result to parent component
      onSubmit(prompt, response.data);
      
      // Clear the input
      setPrompt('');
    } catch (err) {
      console.error('Error generating animation:', err);
      setError('Failed to generate animation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-1">
            Enter your animation request:
          </label>
          <textarea
            id="prompt"
            className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring focus:ring-primary-200"
            rows={4}
            placeholder="e.g., Show me how the Pythagorean theorem works with a visual example"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isLoading}
          />
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            type="submit"
            className="btn-primary flex items-center"
            disabled={isLoading || !prompt.trim()}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </>
            ) : (
              'Generate Animation'
            )}
          </button>
          
          <button
            type="button"
            className="btn-secondary"
            onClick={() => setPrompt('')}
            disabled={isLoading || !prompt}
          >
            Clear
          </button>
        </div>
      </form>
      
      <div className="text-sm text-gray-600 mt-2">
        <h3 className="font-medium">Example prompts:</h3>
        <ul className="list-disc pl-5 mt-1 space-y-1">
          <li>"Explain the Pythagorean theorem with visual examples"</li>
          <li>"Show how derivatives work in calculus"</li>
          <li>"Demonstrate the concept of gravity with simple objects"</li>
        </ul>
      </div>
    </div>
  );
};

export default ChatInterface;