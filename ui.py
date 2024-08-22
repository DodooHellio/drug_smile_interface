import streamlit as st
import pandas as pd

st.markdown(""" 💊 Drug & Smile 💊 """)



with st.form("my_form"):
    st.write("Test your molecules")
    model = st.radio('Select a model', ('Random Forest', 'GNN', 'Logistic Regression'))

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("model selected ➤", model)
        st.write("uploaded_file", uploaded_file)

st.write("Results bellow")
