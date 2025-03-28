from .utils import parse_qcm_response, build_prompt, parse_analyse_response
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

cle_api_openai = os.getenv("OPENAI_API_KEY")

def generate_questions(question_type="multiple choice questions", theme_name="Patent Law", level="entry", nbre=5):
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
    
    print('reponse rag = ', response)
    
    if question_type == "QCM":
        questions = parse_qcm_response(response)
    elif question_type == "Analyse":
        questions = parse_analyse_response(response)
        
    return questions