import streamlit as st
import requests

st.title(""" 💊 Drug & Smile 💊 """)

req = ""

with st.form("my_form"):
    st.write("Test your molecules")
    model = st.radio('Select a model', ('Random Forest', 'GNN', 'Logistic Regression'))
    uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])
    submitted = st.form_submit_button("Submit")

    if submitted:

        params = {"model_name" : model}
        if uploaded_file is not None:
            files = {'file':uploaded_file.getvalue()}
            response_parquet = requests.post(f"http://127.0.0.1:8080/loaddata", data=params,files=files)
            if response_parquet.status_code == 200:
                st.write(response_parquet.json()["message"])
            else:
                st.write("Error submission parquet file")

st.write("Results bellow")
