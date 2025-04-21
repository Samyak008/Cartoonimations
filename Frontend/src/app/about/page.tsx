import React from 'react';
import Link from 'next/link';

export default function About() {
  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <Link href="/" className="text-primary-600 hover:text-primary-700 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
          Back to Home
        </Link>
      </div>
      
      <h1 className="text-3xl font-bold text-gray-900 mb-6">About Cartoonimations</h1>
      
      <div className="space-y-8">
        <section className="card">
          <h2 className="text-xl font-semibold mb-4">Project Overview</h2>
          <p className="text-gray-700 mb-4">
            Cartoonimations is an educational animation platform that uses artificial intelligence to create
            engaging mathematical and scientific visualizations. Our system leverages the powerful Manim library
            for animations, combined with AI-driven content generation.
          </p>
          <p className="text-gray-700">
            Simply enter a prompt describing the concept you want to explore, and Cartoonimations will generate
            a custom animation with synchronized voiceover explaining the concept.
          </p>
        </section>
        
        <section className="card">
          <h2 className="text-xl font-semibold mb-4">Technology Stack</h2>
          <ul className="space-y-2 text-gray-700">
            <li className="flex">
              <span className="font-medium w-32">Frontend:</span>
              <span>Next.js, React, Tailwind CSS</span>
            </li>
            <li className="flex">
              <span className="font-medium w-32">Backend:</span>
              <span>Flask, LangGraph, Manim</span>
            </li>
            <li className="flex">
              <span className="font-medium w-32">AI:</span>
              <span>Groq, LangChain</span>
            </li>
            <li className="flex">
              <span className="font-medium w-32">Audio:</span>
              <span>Google Text-to-Speech (gTTS)</span>
            </li>
          </ul>
        </section>
        
        <section className="card">
          <h2 className="text-xl font-semibold mb-4">How It Works</h2>
          <ol className="list-decimal pl-5 space-y-2 text-gray-700">
            <li>
              <strong>Prompt Analysis:</strong> Your educational request is analyzed by our AI Director.
            </li>
            <li>
              <strong>Scene Planning:</strong> The AI Scene Planner breaks down the concept into teachable scenes.
            </li>
            <li>
              <strong>Code Generation:</strong> Manim animation code is dynamically created for each scene.
            </li>
            <li>
              <strong>Voiceover Creation:</strong> A script is written and converted to speech.
            </li>
            <li>
              <strong>Final Rendering:</strong> The animation is rendered and combined with audio.
            </li>
          </ol>
        </section>
        
        <section className="card">
          <h2 className="text-xl font-semibold mb-4">Example Use Cases</h2>
          <ul className="list-disc pl-5 space-y-1 text-gray-700">
            <li>Visualizing mathematical concepts for students</li>
            <li>Creating instructional content for online courses</li>
            <li>Explaining scientific principles with animated examples</li>
            <li>Developing educational content for presentations</li>
          </ul>
        </section>
      </div>
    </main>
  );
}