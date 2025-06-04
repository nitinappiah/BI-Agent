import streamlit as st
import os

st.title("Generated Source Code:")
with open("./pages/2_📊_Dashboard.py", "r") as file:
    st.code(file.read(), "python")