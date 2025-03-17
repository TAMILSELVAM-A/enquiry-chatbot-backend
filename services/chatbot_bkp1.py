from services.data_loader import load_csv_file, split_text
from vectorstore.vectordb import create_vector_store
from services.model_loader import load_llm
from app.config import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load data
file_path = "D:/ai-chatbot/backend/data/mobile_data.csv"
documents = load_csv_file(file_path)
# text_chunks = split_text(documents)

# Create vector store
vector_store = create_vector_store(documents)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Load LLM model
llm = load_llm()

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ('human', "{input}")
])

# Create chains
qanda_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}), qanda_chain)
rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

def process_query(query: str) -> str:
    response = rag_chain.invoke({"question": query})
    return response['answer']
