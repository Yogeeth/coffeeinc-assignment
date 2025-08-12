from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from generate_answer import generate_answer
from loadmodule import load_module

if __name__ == "__main__":
    ollama_installed = input('Do you have Ollama installed? Yes/No: ').strip().lower()
    memory = None
    llm = None
    model = None
    length=0
    if ollama_installed == "yes":
        print("Commands To Remember : \n/load : Load the module\n/chat : Start chatting (after /load)\n/exit: Exit\n/help : Show help")

        while True:
            command = input('\nCommand = ').strip().lower()

            if command == "/load":
                try:
                    memory = ConversationBufferMemory()
                    model = load_module()
                    llm = model[0]
                    print(f"You have chosen: {model[1]}\n")
                except Exception as e:
                    print(f"Error loading model: {e}")
                    memory = None
                    llm = None

            elif command == '/chat':
                if memory is None or llm is None:
                    print("Please do /load first.")
                    continue

                print('Chat started... 😊')
                while True:
                    user_input = input("\nHuman: ").strip()

                    if user_input == '/exit':
                        break

                    elif user_input == '/memory':
                        if memory is None:
                            print("No memory found. Please /load first.")
                            continue
                        role=["AI","Human"]
                        for a, msg in enumerate(memory.chat_memory.messages, start=1):
                            print(f"{role[a%2]}: {msg.content}")

                    elif user_input == '/reset':
                        memory = ConversationBufferMemory()
                        llm = None
                        model = None
                        length=0
                        print("Memory has been erased.")
                        choice = input("Do you want to reload the LLM? Type /load to load it or any other key to continue without LLM: ").strip().lower()
                        if choice == "/load":
                            print("Please use /load command to load the model.")
                        else:
                            print("Continuing without a loaded model. Use /load when ready.")

                    elif user_input == '/help':
                        print("Inside chat commands:\n"
                              "/memory - Show conversation history\n"
                              "/reset  - Clear memory\n"
                              "/exit   - Back to main menu\n"
                              "Just type anything else to chat.")

                    elif user_input.startswith('/'):
                        print("Unknown command inside chat. Try /help.")

                    else:
                        if length>2000:
                            print("context window Overload....")
                            memory=ConversationBufferMemory()
                            length=0
                            break
                        memory.chat_memory.add_user_message(user_input)
                        print("Generating...")
                        length+=len(user_input)
                        response = generate_answer(memory, user_input, llm)
                        length+=len(response)
                        memory.chat_memory.add_ai_message(response)

            elif command == "/help":
                print("Commands To Remember:\n"
                      "/load   - Load the module\n"
                      "/chat   - Chat with memory (after /load)\n"
                      "/exit   - Exit\n"
                      "/help   - Show help")

            elif command == "/exit":
                print("Goodbye!")
                break

            else:
                print("Unknown command. Try /help.")

    else:
        print("Please install Ollama and come back 😊")