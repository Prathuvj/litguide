# ⚖️ Legal AI Assistant - Indian Law Expert

An AI-powered legal assistant application specializing in Indian Law and the Indian Penal Code (IPC). Built with Chainlit, Gemini AI, FAISS, and LangChain.

## Features

- **Document Upload & Analysis**: Upload legal PDFs and ask questions about them
- **Indian Law Expertise**: Direct chat about IPC sections, acts, and legal provisions
- **Vector-Based Search**: FAISS-powered similarity search for relevant document sections
- **Conversation Memory**: Maintains context throughout the conversation
- **Real-Time Responses**: Powered by Google's Gemini AI
- **Clean UI**: Intuitive Chainlit interface

## Tech Stack

- **Frontend**: Chainlit
- **LLM**: Google Gemini (via genai library)
- **Vector Store**: FAISS
- **Orchestration**: LangChain
- **Document Processing**: PyPDF

## Installation

1. **Clone the repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. **Get Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Create a new API key
   - Add it to your `.env` file

## Usage

1. **Start the application**:
```bash
chainlit run app.py -w
```

2. **Access the interface**:
   - Open your browser to `http://localhost:8000`

3. **Use the assistant**:
   - **Upload Documents**: Click the attachment icon to upload legal PDFs
   - **Ask Questions**: Type your queries about Indian law or uploaded documents
   - **Get Answers**: Receive detailed responses with legal citations

## Project Structure

```
.
├── app.py                      # Main Chainlit application
├── config.py                   # Configuration settings
├── prompts.py                  # Legal prompt templates
├── vector_store_manager.py     # FAISS vector store management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .chainlit/
│   └── config.toml            # Chainlit UI configuration
└── vector_store/              # FAISS vector database (created on first upload)
```

## Configuration

Edit `config.py` to customize:
- Model name and parameters
- Chunk size for document processing
- Vector store location
- Temperature and token limits

## Important Disclaimer

⚠️ This application provides legal information, not legal advice. Always consult a qualified lawyer for specific legal matters.

## Guidelines

The AI assistant follows strict guidelines:
1. Provides accurate information based on Indian legal framework
2. Cites relevant IPC sections and legal provisions
3. Distinguishes between general guidance and specific legal advice
4. Recommends consulting qualified lawyers for specific cases
5. Maintains professional and formal tone
6. Acknowledges limitations when uncertain

## License

MIT License
