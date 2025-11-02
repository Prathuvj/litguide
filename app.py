import chainlit as cl
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import config
import prompts
from vector_store_manager import VectorStoreManager

# Initialize vector store manager
vector_manager = VectorStoreManager()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=config.MODEL_NAME,
    google_api_key=config.GOOGLE_API_KEY,
    temperature=config.TEMPERATURE,
    max_tokens=config.MAX_OUTPUT_TOKENS
)

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    cl.user_session.set("memory", memory)
    
    # Welcome message
    welcome_msg = """# ⚖️ Legal AI Assistant - Indian Law Expert

Welcome! I'm your AI Legal Assistant specializing in Indian Law and the Indian Penal Code (IPC).

**How I can help:**
- Answer questions about Indian laws, IPC sections, and legal provisions
- Analyze uploaded legal documents (PDF format)
- Provide legal information and context
- Search through your uploaded documents

**Getting Started:**
1. **Upload Documents**: Click the attachment icon to upload legal PDFs
2. **Ask Questions**: Type your legal queries directly

**Important Disclaimer:**
⚠️ I provide legal information, not legal advice. Always consult a qualified lawyer for specific legal matters.

How can I assist you today?"""
    
    await cl.Message(content=welcome_msg).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    memory = cl.user_session.get("memory")
    
    # Check for file uploads
    if message.elements:
        await handle_file_upload(message.elements)
        return
    
    # Process query
    query = message.content
    
    # Send thinking message
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Check if we have documents in vector store
        if vector_manager.has_documents():
            # Use RAG approach with documents
            response = await query_with_documents(query, memory)
        else:
            # Direct query to Gemini
            response = await query_without_documents(query, memory)
        
        msg.content = response
        await msg.update()
        
    except Exception as e:
        error_msg = f"❌ An error occurred: {str(e)}\n\nPlease try again or rephrase your question."
        msg.content = error_msg
        await msg.update()

async def handle_file_upload(elements):
    """Handle PDF file uploads"""
    processing_msg = cl.Message(content="📄 Processing your document(s)...")
    await processing_msg.send()
    
    processed_files = []
    errors = []
    
    for element in elements:
        if element.mime == "application/pdf":
            try:
                # Process PDF
                documents = vector_manager.process_pdf(element.path)
                vector_manager.add_documents(documents)
                processed_files.append(element.name)
            except Exception as e:
                errors.append(f"{element.name}: {str(e)}")
    
    # Send result message
    if processed_files:
        success_msg = f"✅ Successfully processed {len(processed_files)} document(s):\n"
        success_msg += "\n".join([f"- {name}" for name in processed_files])
        success_msg += "\n\nYou can now ask questions about these documents!"
        await cl.Message(content=success_msg).send()
    
    if errors:
        error_msg = "⚠️ Some files could not be processed:\n"
        error_msg += "\n".join([f"- {err}" for err in errors])
        await cl.Message(content=error_msg).send()

async def query_with_documents(query: str, memory):
    """Query using RAG with uploaded documents"""
    # Get relevant documents
    relevant_docs = vector_manager.similarity_search(query, k=4)
    
    # Build context from documents
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Build prompt
    prompt = prompts.LEGAL_SYSTEM_PROMPT + "\n\n" + prompts.DOCUMENT_QUERY_PROMPT.format(
        context=context,
        question=query
    )
    
    # Get chat history
    chat_history = memory.load_memory_variables({}).get("chat_history", [])
    history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history[-4:]])
    
    if history_text:
        prompt = f"Previous conversation:\n{history_text}\n\n{prompt}"
    
    # Generate response using LangChain's ChatGoogleGenerativeAI
    response = await llm.ainvoke(prompt)
    answer = response.content
    
    # Save to memory
    memory.save_context({"input": query}, {"answer": answer})
    
    return answer

async def query_without_documents(query: str, memory):
    """Query directly without documents"""
    # Build prompt
    prompt = prompts.LEGAL_SYSTEM_PROMPT + "\n\n" + prompts.GENERAL_QUERY_PROMPT.format(
        question=query
    )
    
    # Get chat history
    chat_history = memory.load_memory_variables({}).get("chat_history", [])
    history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history[-4:]])
    
    if history_text:
        prompt = f"Previous conversation:\n{history_text}\n\n{prompt}"
    
    # Generate response using LangChain's ChatGoogleGenerativeAI
    response = await llm.ainvoke(prompt)
    answer = response.content
    
    # Save to memory
    memory.save_context({"input": query}, {"answer": answer})
    
    return answer
