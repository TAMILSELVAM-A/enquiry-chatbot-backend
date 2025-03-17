from services.data_loader import load_csv_file, split_text
from vectorstore.vectordb import create_vector_store, retrieve_answer
from services.model_loader import load_llm
from app.config import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '../data/mobile_data.csv')


try:
    file_path = CSV_PATH
    documents = load_csv_file(file_path)
    text_chunks = split_text(documents)
except Exception as e:
    print(f"Error loading or processing data: {e}")
    raise

# Create vector store
try:
    vector_store = create_vector_store(text_chunks)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
except Exception as e:
    print(f"Error creating vector store: {e}")
    raise

# Load LLM model
try:
    llm = load_llm()
except Exception as e:
    print(f"Error loading LLM model: {e}")
    raise

# Create prompt template
try:
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ('human', "{input}")
    ])
except Exception as e:
    print(f"Error creating prompt template: {e}")
    raise

# Create chains
try:
    qanda_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qanda_chain)
except Exception as e:
    print(f"Error creating chains: {e}")
    raise

def process_query(query: str) -> str:
    response = rag_chain.invoke({"input": query})
    return response['answer']
