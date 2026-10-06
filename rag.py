from pathlib import Path
import json,re
DB=Path("documents/index.json")
def load():
    return json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else {}
def add_document(name,text):
    d=load(); d[name]=[x.strip() for x in re.split(r"\n{2,}|(?<=[.!?])\s+",text) if x.strip()]
    DB.parent.mkdir(exist_ok=True); DB.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
def search_documents(q):
    terms=set(re.findall(r"\w+",q.lower())); hits=[]
    for name,chunks in load().items():
        for c in chunks:
            score=sum(t in c.lower() for t in terms)
            if score:hits.append((score,name,c))
    hits.sort(reverse=True)
    return [f"**{n}** — {c}" for _,n,c in hits[:5]]
