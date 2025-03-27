from utils import parse_qcm_response, build_prompt, parse_analyse_response
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

cle_api_openai = "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"

def generate_questions(question_type="QCM", theme_name="Général", level="débutant", nbre=5):
    prompt = build_prompt(question_type, theme_name, level, nbre)
    
    # Charger la base existante
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="db", embedding_function=embeddings)

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",  # ou "gpt-3.5-turbo" selon le modèle souhaité
        openai_api_key=cle_api_openai,
    )

    # Le reste reste identique
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
    )

    response = qa.run(prompt)
    
    if question_type == "QCM":
        questions = parse_qcm_response(response)
    elif question_type == "Analyse":
        questions = parse_analyse_response(response)
        
    return questions