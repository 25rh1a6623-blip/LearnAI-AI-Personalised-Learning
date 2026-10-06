import requests
def ollama_available():
    try:return requests.get("http://localhost:11434/api/tags",timeout=1.5).ok
    except:return False
def ask_ai(q,subject,level):
    if ollama_available():
        try:
            p={"model":"llama3.2","prompt":f"You are a friendly college tutor. Level:{level}. Subject:{subject}. Explain with examples. Question:{q}","stream":False}
            r=requests.post("http://localhost:11434/api/generate",json=p,timeout=90)
            if r.ok:return r.json().get("response","")
        except:pass
    return f"""### 💡 Demo Tutor
**Subject:** {subject}
**Question:** {q}
1. Start with the basic definition.
2. Understand a simple example.
3. Practise the concept.
4. Test yourself.
Install Ollama and run `ollama pull llama3.2` for live local AI."""
