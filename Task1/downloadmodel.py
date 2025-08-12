import subprocess

def download_model(model_name):
    print(f"Downloading model '{model_name}' Please wait.")
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        print(f"Model '{model_name}' downloaded successfully")
    except subprocess.CalledProcessError:
        print(f"Failed to download '{model_name}'. Make sure Ollama is installed and running.")
