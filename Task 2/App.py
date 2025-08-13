import streamlit as st
import time
import subprocess
from datetime import datetime
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory

st.set_page_config(
    page_title="Simple Chat",
    page_icon="💬",
    layout="wide"
)

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0

if "model" not in st.session_state:
    st.session_state.model = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "is_downloading" not in st.session_state:
    st.session_state.is_downloading = False

def list_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]
            models = [line.split()[0] for line in lines if line.strip()]
            return models
        return []
    except Exception as e:
        st.error(f"Error getting models: {e}")
        return []

def download_model(model_name):
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name], 
            capture_output=True, 
            text=True, 
            timeout=300
        )
        
        if result.returncode == 0:
            return True, f"Model '{model_name}' downloaded successfully!"
        else:
            return False, f"Failed to download '{model_name}': {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, f"Download of '{model_name}' timed out. Try again."
    except subprocess.CalledProcessError as e:
        return False, f"Failed to download '{model_name}': {str(e)}"
    except Exception as e:
        return False, f"Error downloading '{model_name}': {str(e)}"

def show_download_interface():
    st.subheader("Download Models")
    popular_models = [
        "gpt-oss:20b",
        "llama3.1:8b",
        "llama3.1:70b",
        "llama2:7b",
        "llama2:13b",
        "mistral:7b",
        "codellama:7b",
        "phi3:mini",
        "gemma2:2b",
        "qwen2:7b"
    ]
    tab1, tab2 = st.tabs(["Popular Models", "Custom Model"])
    
    with tab1:
        st.write("Select from popular models:")
        cols = st.columns(3)
        for i, model in enumerate(popular_models):
            with cols[i % 3]:
                if st.button(f"{model}", key=f"download_{model}", use_container_width=True):
                    start_download(model)
    
    with tab2:
        st.write("Enter a custom model name:")
        custom_model = st.text_input(
            "Model name (e.g., llama3.1:8b):",
            placeholder="Enter model name...",
            key="custom_model_input"
        )
        
        if st.button("Download Custom Model", type="primary", disabled=not custom_model):
            if custom_model.strip():
                start_download(custom_model.strip())

def start_download(model_name):
    if st.session_state.is_downloading:
        st.warning("Another model is currently downloading. Please wait.")
        return
    
    st.session_state.is_downloading = True
    progress_container = st.empty()
    
    with progress_container.container():
        st.info(f"Downloading **{model_name}**... This may take a few minutes.")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Downloading... {i + 1}%")
            time.sleep(0.05)

    success, message = download_model(model_name)
    progress_container.empty()
    
    if success:
        st.success(message)
        st.rerun()
    else:
        st.error(message)
    
    st.session_state.is_downloading = False

def get_response(memory, user_input, llm):
    yield "generating...\n\n"
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
    try:
        for chunk in llm.stream(prompt):
            ai_response += chunk
            yield chunk
        
        memory.save_context({"input": user_input}, {"output": ai_response})
    except Exception as e:
        error_msg = f"Error generating response: {e}"
        yield error_msg
        memory.save_context({"input": user_input}, {"output": error_msg})

def create_new_chat():
    st.session_state.chat_counter += 1
    chat_id = f"chat_{st.session_state.chat_counter}"
    
    memory = ConversationBufferMemory(return_messages=False)
    
    st.session_state.chats[chat_id] = {
        "messages": [],
        "title": f"Chat {st.session_state.chat_counter}",
        "created": datetime.now().strftime("%H:%M"),
        "memory": memory
    }
    st.session_state.active_chat = chat_id
    st.rerun()

def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        if st.session_state.active_chat == chat_id:
            if st.session_state.chats:
                st.session_state.active_chat = list(st.session_state.chats.keys())[-1]
            else:
                st.session_state.active_chat = None
        st.rerun()

models = list_models()

with st.sidebar:
    st.title("Chat")
    with st.expander("Download Models", expanded=False):
        if st.button("Refresh Models", use_container_width=True):
            st.rerun()
        st.write("**Popular Models:**")
        popular_models_sidebar = ["llama3.1:8b", "mistral:7b", "phi3:mini"]
        
        for model in popular_models_sidebar:
            if st.button(f"{model}", key=f"sidebar_{model}", use_container_width=True):
                start_download(model)
        
        custom_model_sidebar = st.text_input("Custom model:", placeholder="e.g., llama2:7b", key="sidebar_custom")
        if st.button("Download", disabled=not custom_model_sidebar, use_container_width=True):
            if custom_model_sidebar.strip():
                start_download(custom_model_sidebar.strip())
    
    st.divider()
    
    if not models:
        st.warning("No models found")
        st.write("Download a model to get started!")
    else:
        if not st.session_state.model:
            st.session_state.model = models[0]

        if not st.session_state.llm and st.session_state.model:
            try:
                st.session_state.llm = OllamaLLM(model=st.session_state.model)
            except Exception as e:
                st.error(f"Error initializing LLM: {e}")
        
        selected_model = st.selectbox(
            "Model:", 
            models,
            index=models.index(st.session_state.model) 
            if st.session_state.model in models else 0
        )

        if selected_model != st.session_state.model:
            try:
                with st.spinner(f"Loading {selected_model}..."):
                    st.session_state.model = selected_model
                    print(st.session_state.model)
                    st.session_state.llm = OllamaLLM(model=selected_model)
                st.rerun()
            except Exception as e:
                st.error(f"Error switching to {selected_model}: {e}")
        
        if st.session_state.llm and st.session_state.model:
            st.success(f"{st.session_state.model}")
        else:
            st.error("LLM not initialized")
    
    if st.button("New Chat", use_container_width=True, disabled=not models):
        create_new_chat()
    
    st.divider()
    
    if st.session_state.chats:
        st.write("**Chat History:**")
        for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    chat_data["title"], 
                    key=f"select_{chat_id}",
                    use_container_width=True,
                    type="primary" if chat_id == st.session_state.active_chat else "secondary"
                ):
                    st.session_state.active_chat = chat_id
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)
    else:
        st.write("No chats yet")

print(models)
if not models:
    st.title("Welcome to Simple Chat")
    st.write("Get started by downloading a model:")
    show_download_interface()
    
elif st.session_state.active_chat and st.session_state.active_chat in st.session_state.chats:
    current_chat = st.session_state.chats[st.session_state.active_chat]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(current_chat["title"])
    with col2:
        if st.button("Download More Models"):
            st.session_state.show_download = True
            st.rerun()
    
    if st.session_state.get("show_download", False):
        with st.expander("Download Models", expanded=True):
            show_download_interface()
            if st.button("Close Download"):
                st.session_state.show_download = False
                st.rerun()

    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("Type your message..."):
        if not current_chat["messages"]:
            current_chat["title"] = " ".join(prompt.split()[:3])
        
        current_chat["messages"].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        if st.session_state.llm:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                try:
                    for chunk in get_response(current_chat["memory"], prompt, st.session_state.llm):
                        full_response += chunk
                        response_placeholder.write(full_response + "▌")
                        time.sleep(0.01)
                    
                    response_placeholder.write(full_response)
                    
                    current_chat["messages"].append({"role": "assistant", "content": full_response})
                    st.session_state.chats[st.session_state.active_chat] = current_chat
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"Error: {e}"
                    response_placeholder.write(error_msg)
                    current_chat["messages"].append({"role": "assistant", "content": error_msg})
                    
        else:
            st.error("LLM not available")

else:
    st.title("Simple Chat")
    if st.session_state.model:
        st.write(f"Using **{st.session_state.model}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Chatting", type="primary"):
                create_new_chat()
        with col2:
            if st.button("Download More Models"):
                st.session_state.show_download = True
                st.rerun()
        
        if st.session_state.get("show_download", False):
            st.divider()
            show_download_interface()
            if st.button("Close Download"):
                st.session_state.show_download = False
                st.rerun()
    else:
        st.write("Please select a model from the sidebar to start chatting.")
