# 📚 Research Paper AI Assistant

An AI-powered research assistant for analyzing academic papers and white papers. Built with Chainlit, Gemini AI, FAISS, and LangChain.

## Features

- **Automatic Information Extraction**: Upload papers and get key information extracted automatically
- **Document Upload & Analysis**: Upload research PDFs (single or multiple)
- **Intelligent Q&A**: Ask questions about methodologies, findings, and conclusions
- **Vector-Based Search**: FAISS-powered similarity search for relevant paper sections
- **Conversation Memory**: Maintains context throughout the conversation
- **Real-Time Responses**: Powered by Google's Gemini 2.5 Flash
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
   - **Upload Papers**: Click the attachment icon to upload research PDFs
   - **Auto-Analysis**: Key information is automatically extracted and displayed
   - **Ask Questions**: Query about methodologies, findings, or concepts
   - **Get Answers**: Receive detailed responses with citations from the papers

## Project Structure

```
.
├── app.py                      # Main Chainlit application
├── config.py                   # Configuration settings
├── prompts.py                  # AI prompt templates
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

## Guidelines

The AI assistant follows strict guidelines:
1. Provides accurate information based on research papers
2. Cites relevant papers, sections, and findings
3. Explains complex concepts clearly and concisely
4. Maintains academic and professional tone
5. Acknowledges limitations when uncertain
6. Focuses on factual, objective information from research

## License

MIT License
