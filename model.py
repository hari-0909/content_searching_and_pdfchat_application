import streamlit as st
import os
from transformers import AutoTokenizer
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
def offline_mode(user_question, pdf_paths):
    try:
        docs = []
        for pdf_path in pdf_paths:
            loader = PyPDFLoader(pdf_path)
            docs.extend(loader.load())
        print("Loaded PDF documents:", len(docs))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = text_splitter.split_documents(docs)
        print("Split documents:", len(documents))

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
        db = FAISS.from_documents(documents, embeddings)
        db.save_local("faiss")
        print("Embeddings and FAISS index created and saved")

        template = """You are an AI assistant designed to answer questions based solely on the context of a provided PDF document. Your task is to find the most relevant information from the PDF to answer the questions. If the information is not available in the PDF, you should respond with "I don't know."
        
        Context:\n {context}\n
        Question:\n {question}?\n
        Remember, if the answer to a question is not available in the PDF content, respond with "I don't know." return helpful answer.
        Helpful answer:
        """
        model_path = "llama-2-7b-chat.ggmlv3.q2_K.bin"
        llm = CTransformers(model=model_path, model_type='llama', config={'max_new_tokens': 256, 'temperature': 0.05}, force_download=True)
        print("Model loaded:", model_path)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
        db = FAISS.load_local("faiss", embeddings, allow_dangerous_deserialization="True")
        docss = db.similarity_search(user_question)
        print("FAISS index loaded")

        retriever = db.as_retriever(search_kwargs={'k': 2})
        prompt = PromptTemplate(template=template, input_variables=['context', 'question'])
        qa_llm = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever, return_source_documents=True, chain_type_kwargs={'prompt': prompt})
        print("Retriever and QA chain created")

        original_prompt = user_question
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        tokenized_prompt = tokenizer.encode(original_prompt, return_tensors="pt")
        tokenized_prompt_str = tokenizer.decode(tokenized_prompt[0], skip_special_tokens=True)
        print("Original prompt:", original_prompt)
        print("Tokenized prompt:", tokenized_prompt_str)

        output = qa_llm({'query': tokenized_prompt_str})
        print("Output from QA model:", output)
        res = output["result"]
        print("response:", res)
        return {"response": res}
    except Exception as e:
        print(e)
        return {"response": "Something went wrong"}
st.title("Chat with Me")
temp_file_path = 'temp\selected_files.txt'
pdf_docs = []
if os.path.exists(temp_file_path):
    with open(temp_file_path, 'r') as file:
        pdf_docs = [line.strip() for line in file.readlines()]
question = st.text_input("Enter your query")
if st.button("Begin Search"):
    if not pdf_docs:
        st.write("No PDF paths provided. Please check the input.")
    elif not question:
        st.write("No query provided. Please enter a question.")
    else:
        result = offline_mode(question, pdf_docs)
        st.write(result["response"])