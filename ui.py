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
    selection = st.radio('Select a model', ('Raw Features', 'Binary Vectors', 'Graphs'))
    uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])

    col1, col2 = st.columns(2)

    with col1:
        submitted = st.form_submit_button(label="Submit")

    with col2:
        predict_button = st.form_submit_button(label='Predict')


    # if submitted:
    #     if selection == "Raw Features":
    #         model = "Support Vector Machine"
    #     elif selection == "Binary Vectors":
    #         model = "Logistic Regression"
    #     elif selection == "Graphs":
    #         model = "GNN"

    #     params = {"model_name" : model}
    #     if uploaded_file is not None:


    #         files = {'file':uploaded_file.getvalue()}
    #         response_parquet = requests.post(f"http://127.0.0.1:8010/predict", data=params,files=files)
    #         if response_parquet.status_code == 200:
    #             result_predict =pd.read_json(response_parquet.json())
    #         else:
    #             st.write("Error submission parquet file")
    #     else :
    #         st.warning("*parquet file missing*")


if submitted:
    if uploaded_file is not None:
        df = pd.read_parquet(uploaded_file)

        st.write(f"You uploaded {df.shape[0]} **molecules** to test : ")
        st.dataframe(df["molecule_smiles"])


if predict_button:
    if uploaded_file is not None:
        st.balloons()

        if selection == "Raw Features":
            model = "Support Vector Machine"
        elif selection == "Binary Vectors":
            model = "Logistic Regression"
        elif selection == "Graphs":
            model = "GNN"

        params = {"model_name" : model}
        if uploaded_file is not None:

            files = {'file':uploaded_file.getvalue()}
            response_parquet = requests.post(f"http://127.0.0.1:8010/predict", data=params,files=files)
            if response_parquet.status_code == 200:
                result_predict =pd.read_json(response_parquet.json())
                st.write("*Prediction : *")
                st.write(result_predict[["molecule_smiles", "BRD4", "HSA", "sEH"]])
            else:
                st.write("Error submission parquet file")
        else :
            st.warning("*parquet file missing*")
