# Cartoonimations - Educational Animation Generator

A platform for creating educational animations using Manim, powered by AI.

## Project Overview

Cartoonimations is a system that generates educational animations based on user prompts. It uses:

- **Flask**: Backend web server
- **Manim**: Mathematical animation library
- **LangGraph**: AI workflow for content generation
- **gTTS**: Text-to-speech for narration

## Project Structure

```
Cartoonimations/
├── Backend/
│   ├── app/            # Flask application
│   │   ├── controllers/  # Business logic
│   │   ├── langgraph/    # AI workflow
│   │   ├── services/     # External integrations
│   │   └── routes/       # API endpoints
│   ├── animation/      # Manim integration
│   │   ├── templates/    # Reusable scenes
│   │   ├── generators/   # Scene generators
│   │   └── output/       # Generated videos and audio
│   ├── app.py          # Main application entry point
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment variables
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- FFmpeg (required for Manim)
- LaTeX distribution (required for Manim)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Cartoonimations.git
   cd Cartoonimations
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Edit `.env` to add your API keys

### Running the Application

Start the Flask server:
```bash
cd Backend
python app.py
```

The server will start at http://localhost:5000

## API Endpoints

- `GET /api/health`: Health check endpoint
- `POST /api/generate`: Generate animation from prompt
  - Request body: `{ "prompt": "Explain the Pythagorean theorem" }`
  - Response: Video and audio paths

## Development Phases

### Phase 1: Core Environment (Complete)
- Basic Flask backend
- Simple Manim template system
- Text-to-speech integration

### Phase 2: Animation Pipeline (In Progress)
- Manim code generation
- Video rendering pipeline
- Voice-over creation

### Phase 3: AI Integration (Planned)
- LLM-based content generation
- LangGraph decision flow
- Scene planning with AI

### Phase 4: User Interface (Future)
- Web-based chat interface
- Video playback
- Session management

## Examples

Example prompts:
- "Explain the Pythagorean theorem with visual examples"
- "Show how derivatives work in calculus"
- "Demonstrate the concept of gravity with simple objects"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
