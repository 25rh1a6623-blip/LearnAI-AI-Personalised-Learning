from pathlib import Path
import pandas as pd
DATA=Path("data/scores.csv")
DEFAULT={"Python":72,"Mathematics":58,"DBMS":76,"AI/ML":64,"Data Structures":70}
def load_scores():
    if DATA.exists():
        d=pd.read_csv(DATA); return dict(zip(d.subject,d.score))
    return DEFAULT.copy()
def save_scores(s):
    DATA.parent.mkdir(exist_ok=True)
    pd.DataFrame({"subject":list(s),"score":list(s.values())}).to_csv(DATA,index=False)
def recommendations(s):
    out=[]
    for sub,score in sorted(s.items(),key=lambda x:x[1]):
        if score<50: p="HIGH"; plan="Revise fundamentals, learn one concept at a time and solve 10 easy questions daily."
        elif score<70: p="MEDIUM"; plan="Review weak concepts, solve 15 mixed questions and retake a quiz."
        else: p="LOW"; plan="Maintain revision and attempt advanced problems or mini-projects."
        out.append({"subject":sub,"score":score,"priority":p,"plan":plan})
    return out
def study_plan(s):
    w=min(s,key=s.get); strong=max(s,key=s.get)
    return [(f"Day {i}",task) for i,task in enumerate([
        f"Revise {w} fundamentals.","Practise 15 questions from "+w,
        "Learn a new concept and make notes.","Revise medium-strength subjects.",
        f"Take a {w} quiz and analyse mistakes.",f"Build/practise something in {strong}.",
        "Full revision and self-assessment."],1)]
def quiz_for(sub):
    d={"Python":("Which keyword defines a function?",["func","def","function","define"],"def"),
    "Mathematics":("What is 2 + 3 × 4?",["20","14","24","9"],"14"),
    "DBMS":("Which command retrieves data?",["GET","SELECT","FETCH","READ"],"SELECT"),
    "AI/ML":("Which is supervised learning?",["K-Means","Linear Regression","PCA","Apriori"],"Linear Regression"),
    "Data Structures":("Which follows LIFO?",["Queue","Stack","Array","Graph"],"Stack")}
    return d[sub]
def timetable(s,hours):
    w=min(s,key=s.get)
    return [(f"Day {i}",f"{round(hours*.5,1)}h {w} + {round(hours*.3,1)}h revision + {round(hours*.2,1)}h quiz") for i in range(1,8)]
