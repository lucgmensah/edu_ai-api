def build_prompt(question_type="QCM", theme="Général", level="débutant", nbre=5):
    if question_type == "QCM":
        return f"""
        Tu es un professeur de mathématiques.
        Génère un QCM de {nbre} questions sur le thème "{theme}", niveau {level}.
        
        Ta réponse DOIT suivre strictement ce format :
        
        Question : Quel est le mot clé utilisé pour définir une fonction en Python ?
        A. define
        B. function
        C. def
        D. fun
        Réponse correcte : C
        """
    elif question_type == "Analyse":
        return f"""
        Tu es un enseignant.
        
        En te basant sur le thème "{theme}", niveau {level}, génère {nbre} exercices.
        
        Génère une question ouverte de type analyse. Formate ta réponse comme ceci :
        
        Question : ...
        Consignes : ...
        """
    else:
        raise ValueError("Type de question non reconnu.")


def parse_qcm_response(response_text):
    questions = []
    lines = response_text.strip().splitlines()
    question, choices, correct = "", {}, ""
    for line in lines:
        line = line.strip()
        if line.lower().startswith("question"):
            # Si une nouvelle question commence, sauvegardez la précédente
            if question:
                questions.append({"question": question, "choices": choices, "correct": correct})
                question, choices, correct = "", {}, ""  # Réinitialiser pour la prochaine question
            question = line.split(":", 1)[-1].strip()
        elif line.startswith(("A.", "B.", "C.", "D.")):
            key, val = line.split(".", 1)
            choices[key.strip()] = val.strip()
        elif "réponse correcte" in line.lower():
            correct = line.split(":")[-1].strip()
    # Ajouter la dernière question si elle existe
    if question:
        questions.append({"question": question, "choices": choices, "correct": correct})
    return questions

def parse_analyse_response(response_text):
    questions = []
    lines = response_text.strip().split("\n")
    question, instructions = "", ""
    for line in lines:
        line = line.strip()
        if line.lower().startswith("question"):
            # Si une nouvelle question commence, sauvegardez la précédente
            if question:
                questions.append({"question": question, "instructions": instructions})
                question, instructions = "", ""  # Réinitialiser pour la prochaine question
            question = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("consignes"):
            instructions = line.split(":", 1)[-1].strip()
    # Ajouter la dernière question si elle existe
    if question:
        questions.append({"question": question, "instructions": instructions})
    return questions