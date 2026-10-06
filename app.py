import streamlit as st
import pandas as pd
from utils.core import load_scores,save_scores,recommendations,study_plan,quiz_for,timetable
from utils.ai_tutor import ask_ai,ollama_available
from utils.documents import extract_text
from utils.rag import add_document,search_documents

st.set_page_config(page_title="LearnAI",page_icon="🎓",layout="wide")
st.title("🎓 LearnAI — AI-Powered Personalised Learning")
st.caption("A personalised learning platform for students")

if "scores" not in st.session_state: st.session_state.scores=load_scores()

with st.sidebar:
    st.header("👩‍🎓 Student Profile")
    name=st.text_input("Name","Pavani")
    sid=st.text_input("Student ID","25RH1A6623")
    branch=st.selectbox("Branch",["AIML-A","CSE","ECE","EEE","Other"])
    level=st.selectbox("Level",["Beginner","Intermediate","Advanced"])
    st.divider()
    st.write("AI:", "🟢 Ollama" if ollama_available() else "🟡 Demo mode")

tabs=st.tabs(["🏠 Dashboard","🎯 Learning Plan","🤖 AI Tutor","📚 Notes & RAG","📝 Quiz","🗓️ Timetable"])

with tabs[0]:
    s=st.session_state.scores
    overall=round(sum(s.values())/len(s))
    a,b,c,d=st.columns(4)
    a.metric("Overall",f"{overall}%"); b.metric("Subjects",len(s))
    c.metric("Strongest",max(s,key=s.get)); d.metric("Needs Focus",min(s,key=s.get))
    st.subheader("📊 Performance")
    st.bar_chart(pd.DataFrame({"Score":s}))
    st.subheader("✏️ Update Scores")
    for subject in s:
        s[subject]=st.slider(subject,0,100,int(s[subject]),key="score_"+subject)
    if st.button("💾 Save Performance"):
        save_scores(s); st.success("Saved! Recommendations updated.")

with tabs[1]:
    st.subheader("🎯 Personalised Recommendations")
    for x in recommendations(st.session_state.scores):
        st.markdown(f"### {x['subject']} — {x['priority']} Priority")
        st.write(f"Score: **{x['score']}%**")
        st.write(x["plan"])
    st.subheader("📅 7-Day Learning Plan")
    for day,task in study_plan(st.session_state.scores): st.write(f"**{day}:** {task}")

with tabs[2]:
    st.subheader("🤖 AI Tutor")
    subject=st.selectbox("Subject",list(st.session_state.scores),key="tutor_sub")
    q=st.text_area("Question",placeholder="Explain neural networks simply...")
    if st.button("Ask AI",type="primary"):
        if q.strip():
            with st.spinner("Thinking..."): st.markdown(ask_ai(q,subject,level))
        else: st.warning("Enter a question.")

with tabs[3]:
    st.subheader("📚 Upload Study Material")
    up=st.file_uploader("PDF or DOCX",type=["pdf","docx"])
    if up:
        text=extract_text(up); add_document(up.name,text)
        st.success("Material added to knowledge base.")
        st.text_area("Preview",text[:5000],height=220)
    q=st.text_input("Search your uploaded notes")
    if q:
        results=search_documents(q)
        for r in results: st.info(r)
        if not results: st.warning("No matching content found.")

with tabs[4]:
    st.subheader("📝 Adaptive Quiz")
    subject=st.selectbox("Subject",list(st.session_state.scores),key="quiz_sub")
    q,opts,ans=quiz_for(subject)
    st.write("**"+q+"**")
    choice=st.radio("Answer",opts)
    if st.button("Check Answer"):
        st.success("Correct! 🎉") if choice==ans else st.error(f"Correct answer: {ans}")

with tabs[5]:
    st.subheader("🗓️ Personalised Timetable")
    hours=st.slider("Daily study hours",1,8,3)
    for day,task in timetable(st.session_state.scores,hours): st.write(f"**{day}:** {task}")
