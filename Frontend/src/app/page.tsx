'use client'

import { useState } from 'react'
import ChatInterface from '@/components/ChatInterface'
import VideoPlayer from '@/components/VideoPlayer'
import SessionHistory from '@/components/SessionHistory'
import Header from '@/components/Header'

export default function Home() {
  const [currentVideo, setCurrentVideo] = useState<string | null>(null)
  const [currentAudio, setCurrentAudio] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [history, setHistory] = useState<Array<{
    prompt: string;
    timestamp: Date;
    response: {
      video_path: string;
      audio_path: string;
      message: string;
    }
  }>>([])

  const addToHistory = (prompt: string, response: any) => {
    setHistory(prev => [...prev, {
      prompt,
      timestamp: new Date(),
      response
    }])
    
    // Update current media
    setCurrentVideo(response.video_path)
    setCurrentAudio(response.audio_path)
  }

  const selectFromHistory = (index: number) => {
    const item = history[index]
    setCurrentVideo(item.response.video_path)
    setCurrentAudio(item.response.audio_path)
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Session History Sidebar */}
          <div className="lg:col-span-1 order-2 lg:order-1">
            <SessionHistory 
              history={history} 
              onSelect={selectFromHistory} 
            />
          </div>
          
          {/* Main Content Area */}
          <div className="lg:col-span-3 space-y-8 order-1 lg:order-2">
            {/* Video Player */}
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
              {currentVideo ? (
                <div className="p-6">
                  <h2 className="text-2xl font-bold mb-4 text-gray-800">Your Animation</h2>
                  <VideoPlayer 
                    videoUrl={currentVideo} 
                    audioUrl={currentAudio}
                  />
                </div>
              ) : (
                <div className="p-10 flex flex-col items-center justify-center text-center">
                  <div className="w-24 h-24 rounded-full bg-primary-100 flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h2 className="text-2xl font-bold mb-2 text-gray-800">No Animation Yet</h2>
                  <p className="text-gray-500 max-w-md">
                    Enter a prompt below to generate your first educational animation.
                    Try something like "Explain the Pythagorean theorem with visual examples."
                  </p>
                </div>
              )}
            </div>
            
            {/* Chat Interface */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-gray-800">Generate an Animation</h2>
              <ChatInterface 
                onSubmit={addToHistory} 
                setIsLoading={setIsLoading} 
              />
            </div>
            
            {/* Feature highlights */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
              <div className="bg-white rounded-xl shadow-md p-5">
                <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">AI-Powered Generation</h3>
                <p className="text-gray-600 text-sm">Advanced AI models create custom educational animations from your text prompts.</p>
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-5">
                <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Mathematical Precision</h3>
                <p className="text-gray-600 text-sm">Built with Manim for beautiful, accurate mathematical visualizations.</p>
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-5">
                <div className="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Voice Narration</h3>
                <p className="text-gray-600 text-sm">Synchronized voiceover makes complex concepts easier to understand.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <footer className="mt-24 bg-gray-800 text-white py-12 px-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="mb-6 md:mb-0">
            <h2 className="text-2xl font-bold">Cartoonimations</h2>
            <p className="mt-2 text-gray-300">Educational animations powered by AI</p>
          </div>
          <div className="flex space-x-8">
            <div>
              <h3 className="font-semibold mb-3">Resources</h3>
              <ul className="space-y-2">
                <li><a href="/about" className="text-gray-300 hover:text-white">About</a></li>
                <li><a href="https://github.com/yourusername/cartoonimations" className="text-gray-300 hover:text-white">GitHub</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Contact</h3>
              <ul className="space-y-2">
                <li><a href="mailto:contact@example.com" className="text-gray-300 hover:text-white">Email</a></li>
                <li><a href="https://twitter.com/example" className="text-gray-300 hover:text-white">Twitter</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-8 pt-8 border-t border-gray-700 text-center text-gray-400 text-sm">
          <p>&copy; {new Date().getFullYear()} Cartoonimations. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}