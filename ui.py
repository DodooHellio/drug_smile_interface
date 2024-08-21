import streamlit as st
import pandas as pd

st.markdown(""" 💊 Drug & Smile 💊 """)

direction = st.radio('Select a model', ('Random Forest', 'GNN', 'Logistic Regression'))

st.write(f'model selected ➤ {direction} ')


st.set_option('deprecation.showfileUploaderEncoding', False)

"""
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data) """
