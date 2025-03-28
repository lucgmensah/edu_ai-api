def build_prompt(question_type="QCM", theme="Patent Law", level="entry", nbre=5):
    # Common context to establish expertise and expectations
    common_context = f"""
    You are an expert law professor with extensive knowledge in legal education. 
    Your task is to create high-quality, educational content that demonstrates 
    deep understanding of legal concepts.

    Context Details:
    - Topic: {theme}
    - Difficulty Level: {level}
    - Number of Questions: {nbre}

    Important Guidelines:
    1. Ensure all content is factually accurate and academically rigorous.
    2. Adapt the complexity to the specified difficulty level.
    3. Focus on core legal principles and practical understanding.
    4. Avoid overly complex or trick questions.
    5. Provide clear, unambiguous answers.
    """
    
    if question_type == "QCM":
        return common_context + f"""
        Prompt: Generate a multiple-choice quiz with {nbre} questions about {theme}.

        Strict Output Format:
        Question 1: [Clear, concise legal question]
        A. [Precise, plausible option]
        B. [Precise, plausible option]
        C. [Precise, plausible option]
        D. [Precise, plausible option]
        Correct answer: [Single letter corresponding to the correct answer]

        Example:
        Question: What is the primary purpose of civil law?
        A. To punish criminal behavior
        B. To resolve disputes between individuals and entities
        C. To create government regulations
        D. To define international treaties
        Correct answer: B
        """
    
    elif question_type == "Analyse":
        return common_context + f"""
        Prompt: Create {nbre} in-depth analysis exercises about {theme}.

        Detailed Exercise Format:
        Question: [Thought-provoking legal scenario or conceptual challenge]
        Context: [Brief background providing necessary information]
        Instructions: 
        1. [First analytical step]
        2. [Second analytical step]
        3. [Additional guidance for comprehensive analysis]

        Evaluation Criteria:
        - Clarity of legal reasoning
        - Depth of analysis
        - Use of relevant legal principles
        - Coherence of argumentation

        Example:
        Question: Analyze the ethical and legal implications of a corporate whistleblower's actions.
        Context: A mid-level manager discovers systematic financial fraud within her company.
        Instructions:
        1. Identify the legal protections available to whistleblowers
        2. Evaluate the potential personal and professional risks
        3. Discuss the broader societal impact of whistleblowing
        """
    
    else:
        raise ValueError("Unrecognized question type. Must be 'QCM' or 'Analyse'.")


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