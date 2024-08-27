import streamlit as st
import requests
import pandas as pd
from PIL import Image
import base64




st.title(""" 💊 Drug & Smile 💊 """)


with open('images/wagon.png', "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Step 3: CSS for positioning the image
st.markdown(
    f"""
    <style>
    .image-container {{
        position: fixed;
        top: 100px;
        right: 100px;
        z-index: 1000;
    }}
    </style>
    <div class="image-container">
        <img src="data:image/png;base64,{encoded_image}" width="100">
    </div>
    """,
    unsafe_allow_html=True
)


req = ""

with st.form("my_form"):
    st.write("Test your molecules")
    model = st.radio('Select a model', ('Random Forest', 'GNN', 'Logistic Regression'))
    uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])
    submitted = st.form_submit_button("Submit")

    if submitted:

        params = {"model_name" : model}
        if uploaded_file is not None:
            st.balloons()

            files = {'file':uploaded_file.getvalue()}
            response_parquet = requests.post(f"http://127.0.0.1:8010/predict", data=params,files=files)
            if response_parquet.status_code == 200:
                st.write(response_parquet.json())
            else:
                st.write("Error submission parquet file")
        else :
            st.warning("*parquet file missing*")


if submitted:
    if uploaded_file is not None:
        st.write("Molecules to test : ")
        df = pd.read_parquet(uploaded_file)
        st.dataframe(df)
