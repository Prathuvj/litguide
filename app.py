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
    # Clear previous session data
    vector_manager.clear_vector_store()
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    cl.user_session.set("memory", memory)
    
    welcome_msg = """# 📚 Research Paper AI Assistant

Welcome! I'm your AI Research Assistant for analyzing academic papers and white papers.

**How I can help:**
- Extract key information from research papers automatically
- Answer questions about uploaded papers
- Analyze methodologies, findings, and conclusions
- Compare insights across multiple papers

**Getting Started:**
1. **Upload Papers**: Click the attachment icon to upload research PDFs
2. **Auto-Analysis**: I'll automatically extract key information from each paper
3. **Ask Questions**: Query about the papers, findings, methodologies, or concepts

Ready to analyze your research papers!"""
    
    await cl.Message(content=welcome_msg).send()

@cl.on_chat_end
async def end():
    """Clean up when chat session ends"""
    # Clear vector store and memory
    vector_manager.clear_vector_store()
    await cl.Message(content="🧹 Session data cleared. Thanks for using Research Paper AI Assistant!").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    memory = cl.user_session.get("memory")
    
    if message.elements:
        await handle_file_upload(message.elements)
        return
    
    query = message.content
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        if vector_manager.has_documents():
            response = await query_with_documents(query, memory)
        else:
            response = await query_without_documents(query, memory)
        
        msg.content = response
        await msg.update()
        
    except Exception as e:
        error_msg = f"❌ An error occurred: {str(e)}\n\nPlease try again or rephrase your question."
        msg.content = error_msg
        await msg.update()

async def handle_file_upload(elements):
    """Handle PDF file uploads and extract key information"""
    processing_msg = cl.Message(content="📄 Processing your research paper(s)...")
    await processing_msg.send()
    
    processed_files = []
    errors = []
    
    for element in elements:
        if element.mime == "application/pdf":
            try:
                # Process PDF and get full text
                documents, full_text = vector_manager.process_pdf(element.path, element.name)
                vector_manager.add_documents(documents)
                
                # Extract key information from the paper
                extraction_msg = cl.Message(content=f"🔍 Analyzing **{element.name}**...")
                await extraction_msg.send()
                
                key_info = await extract_paper_info(full_text[:8000])  # Use first 8000 chars for extraction
                
                # Update message with extracted info
                extraction_msg.content = f"## 📄 {element.name}\n\n{key_info}"
                await extraction_msg.update()
                
                processed_files.append(element.name)
            except Exception as e:
                errors.append(f"{element.name}: {str(e)}")
    
    # Send completion message
    if processed_files:
        success_msg = f"\n✅ Successfully processed {len(processed_files)} paper(s). You can now ask questions about them!"
        await cl.Message(content=success_msg).send()
    
    if errors:
        error_msg = "⚠️ Some files could not be processed:\n"
        error_msg += "\n".join([f"- {err}" for err in errors])
        await cl.Message(content=error_msg).send()

async def extract_paper_info(text: str) -> str:
    """Extract key information from research paper"""
    try:
        prompt = prompts.PAPER_EXTRACTION_PROMPT.format(content=text)
        response = await llm.ainvoke(prompt)
        return response.content
    except Exception as e:
        return f"Could not extract information: {str(e)}"

async def query_with_documents(query: str, memory):
    """Query using RAG with uploaded research papers"""
    # Get relevant documents
    relevant_docs = vector_manager.similarity_search(query, k=4)
    
    # Build context from documents with source info
    context_parts = []
    for doc in relevant_docs:
        source = doc.metadata.get("source", "Unknown")
        context_parts.append(f"[From: {source}]\n{doc.page_content}")
    context = "\n\n".join(context_parts)
    
    # Build prompt
    prompt = prompts.RESEARCH_SYSTEM_PROMPT + "\n\n" + prompts.DOCUMENT_QUERY_PROMPT.format(
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
    prompt = prompts.RESEARCH_SYSTEM_PROMPT + "\n\n" + prompts.GENERAL_QUERY_PROMPT.format(
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
