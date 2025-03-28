import streamlit as st

st.title("タイトル")

st.write("本文")

st.sidebar.write("サイドバー")

tabs = st.tabs(["タブ1", "タブ2", "タブ3"])

with tabs[0]:
    st.write("タブ1の内容")
