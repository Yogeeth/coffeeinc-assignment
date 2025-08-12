def generate_answer(memory,user_input,llm):
    
    context = memory.load_memory_variables({})["history"]
    prompt = f"""
        You are a helpful and concise AI assistant.
        Only provide accurate, relevant answers.
        If the question refers to earlier parts of the conversation, use the provided history.

        Conversation history:
        {context}

        Current question:
        User: {user_input}

        Your response (be concise and clear):
        AI:
        """

    ai_response = ""
    for chunk in llm.stream(prompt):
        print(chunk, end="", flush=True)
        ai_response += chunk
    return ai_response

