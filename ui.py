import streamlit as st
import pandas as pd
import requests

st.title(""" 💊 Drug & Smile 💊 """)

req = ""

with st.form("my_form"):
    st.write("Test your molecules")
    model = st.radio('Select a model', ('Random Forest', 'GNN', 'Logistic Regression'))

    uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        #st.write("model selected ➤", model)
        #st.write("uploaded_file", uploaded_file)

        response_model = requests.post("http://127.0.0.1:8080/model", json={"selected_model":model})
        if response_model.status_code == 200:
            st.write("model selected ➤" , response_model.json()["model"])
        else:
            st.write("Error submission model")

        if uploaded_file is not None:
            files = {'file':uploaded_file.getvalue()}

            response_parquet = requests.post("http://127.0.0.1:8080/predict", files=files)
            if response_model.status_code == 200:
                st.write(response_parquet.json())
            else:
                st.write("Error submission parquet file")



st.write("Results bellow")
