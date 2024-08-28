import streamlit as st
import requests
import pandas as pd
from PIL import Image
import base64
from rdkit import Chem
from rdkit.Chem import Draw

def from_smile_to_viz(mol):
    img = Draw.MolToImage(mol)
    return img


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

if submitted:
    if uploaded_file is not None:
        df = pd.read_parquet(uploaded_file)

        st.write(f"You uploaded {df.shape[0]} **molecules** to test : ")
        st.dataframe(df["molecule_smiles"])
    else :
        st.warning("*parquet file missing*")



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
                result_predict['BRD4'] = [1, 0, 0, 0, 0]
                result_predict['HSA'] = [0, 1, 0, 0, 0]
                result_predict['sEH'] = [0, 0, 1, 0, 0]

                st.write("**Prediction** : ")
                st.write(result_predict[["molecule_smiles", "BRD4", "HSA", "sEH"]])

                for _ in range(10):
                    st.text("")

                st.write("**Summary** : ")

                col3, col4 = st.columns([1, 2])

                result_predict['molecule_image'] = result_predict['molecule_smiles'].apply(lambda x: from_smile_to_viz(Chem.MolFromSmiles(x)))

                #df = result_predict[['id', 'molecule_smiles', 'molecule_image', 'protein_name', 'binds']]
                df = result_predict
                for i, row in df.iterrows():
                    col3, col4 = st.columns(2)

                    with col3:
                        st.image(row['molecule_image'], caption=df.iloc[i]['molecule_smiles'], width=200)

                    with col4:
                        if df.iloc[i]['BRD4']+df.iloc[i]['HSA']+df.iloc[i]['sEH'] == 0:
                            st.write(f"Ne sert à rien")
                        else :
                            st.write(f"Binds to the protein: {row['protein_name']}")

                    st.write("---")



            else:
                st.write("Error submission parquet file")
    else :
        st.warning("*parquet file missing*")
