import React from 'react';
import Link from 'next/link';

const Header = () => {
  return (
    <header className="py-6 border-b border-gray-200 bg-gradient-to-r from-primary-600 to-primary-800 text-white shadow-lg">
      <div className="flex flex-col sm:flex-row items-center justify-between max-w-7xl mx-auto px-4">
        <div className="mb-4 sm:mb-0 text-center sm:text-left">
          <Link href="/" className="no-underline">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 2a2 2 0 00-2 2v14l3.5-2 3.5 2 3.5-2 3.5 2V4a2 2 0 00-2-2H5zm4.707 3.707a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L8.414 9H14a1 1 0 100-2H8.414l1.293-1.293z" clipRule="evenodd" />
              </svg>
              Cartoonimations
            </h1>
          </Link>
          <p className="text-primary-50 mt-1 text-lg">
            Educational animations powered by AI
          </p>
        </div>
        <div className="flex items-center space-x-6">
          <Link 
            href="/about" 
            className="text-white hover:text-primary-100 transition-colors font-medium text-lg flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            About
          </Link>
          <a 
            href="https://github.com/yourusername/cartoonimations" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-white hover:text-primary-100 transition-colors font-medium text-lg flex items-center"
          >
            <svg className="h-6 w-6 mr-1" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
            GitHub
          </a>
          <button 
            className="bg-white text-primary-800 hover:bg-primary-50 transition-colors px-4 py-2 rounded-lg shadow-sm font-bold"
            onClick={() => alert('Welcome to Cartoonimations! Generate educational animations with AI.')}
          >
            Demo
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;