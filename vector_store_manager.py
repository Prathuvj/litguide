import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from pypdf import PdfReader
import config

class VectorStoreManager:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=config.GOOGLE_API_KEY
        )
        self.vector_store = None
        self.load_vector_store()
    
    def load_vector_store(self):
        """Load existing vector store if available"""
        if os.path.exists(config.VECTOR_STORE_PATH):
            try:
                self.vector_store = FAISS.load_local(
                    config.VECTOR_STORE_PATH,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"Could not load vector store: {e}")
                self.vector_store = None
    
    def save_vector_store(self):
        """Save vector store to disk"""
        if self.vector_store:
            os.makedirs(config.VECTOR_STORE_PATH, exist_ok=True)
            self.vector_store.save_local(config.VECTOR_STORE_PATH)
    
    def process_pdf(self, file_path: str, file_name: str = None) -> tuple[List[Document], str]:
        """Extract text from PDF and create documents. Returns (documents, full_text)"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len
        )
        
        chunks = text_splitter.split_text(text)
        metadata = {"source": file_name or file_path}
        documents = [Document(page_content=chunk, metadata=metadata) for chunk in chunks]
        return documents, text
    
    def add_documents(self, documents: List[Document]):
        """Add documents to vector store"""
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        self.save_vector_store()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents"""
        if self.vector_store is None:
            return []
        return self.vector_store.similarity_search(query, k=k)
    
    def has_documents(self) -> bool:
        """Check if vector store has documents"""
        return self.vector_store is not None
    
    def clear_vector_store(self):
        """Clear vector store from memory and disk"""
        self.vector_store = None
        if os.path.exists(config.VECTOR_STORE_PATH):
            import shutil
            try:
                shutil.rmtree(config.VECTOR_STORE_PATH)
                print("Vector store cleared successfully")
            except Exception as e:
                print(f"Error clearing vector store: {e}")
