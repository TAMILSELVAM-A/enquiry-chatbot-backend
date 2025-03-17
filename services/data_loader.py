import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_csv_file(file_path):
    df = pd.read_csv(file_path)
    documents = df.apply(lambda row: f"Brand: {row['Brand']}, Model: {row['Model']}, "
                                     f"Price: {row['Price (INR)']}, Specifications: {row['Specifications']}, "
                                     f"Features: {row['Features']}, Availability: {row['Availability']}, "
                                     f"Discount: {row['Discount (%)']}", axis=1).tolist()
    return documents

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return splitter.create_documents(documents)
