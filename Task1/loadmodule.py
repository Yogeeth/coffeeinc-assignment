from langchain_ollama import OllamaLLM
import ollama
from downloadmodel import download_model
def view(model):
    models=[]
    for m in model:
        print("Model:", m['model'])
        print("Modified at:", m['modified_at'])
        print("Digest:", m['digest'])
        print("Size:", m['size'])
        print("Format:", m['details']['format'])
        print("Family:", m['details']['family'])
        print("Parameter size:", m['details']['parameter_size'])
        print("Quantization level:", m['details']['quantization_level'])
        print("-" * 30)
        models.append(m['model'])
    return models


def load_module():
    
    print('Available Models.....')
    models=view(ollama.list()['models'])
    while True:
        ask=input("Would you Like to download more : (Yes/No)")
        if ask.lower().replace(' ','')=="yes":
            down_model=input("Enter the model (mistral, llama3, gemma:2b) : ")
            if down_model in ["mistral", "llama3", "gemma:2b"]:
                download_model(down_model)
                models.append(down_model)
                print(f'🔥🔥🔥 You have successfully downloaded {down_model}')
                models=view(ollama.list()['models'])
            else:
                print('Choose Model Properly')
            
        elif ask.lower().replace(' ','')=="no":
            print('We are Moving Ahead\n')
            break
        else:
            pass
    
    choose=input(f'choose the model (1,{len(models)}) :')
    return  [OllamaLLM(model=models[int(choose)-1]),models[int(choose)-1]]