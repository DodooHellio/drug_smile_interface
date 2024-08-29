import streamlit as st
import requests
import pandas as pd
from PIL import Image
import base64
import json
from io import BytesIO
# from rdkit import Chem
# from rdkit.Chem import Draw

# def from_smile_to_viz(mol):
#     img = Draw.MolToImage(mol)
#     return img


st.title(""" 💊 Drug & Smile 💊 """)

def base64_to_pil(img_base64):
    img_data = base64.b64decode(img_base64)
    img = Image.open(BytesIO(img_data))
    return img

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
        df.index = range(1,6)

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
                result_predict['molecule_image'] = result_predict['molecule_image'].apply(base64_to_pil)
                result_predict['BRD4'] = [1, 0, 0, 0, 0]
                result_predict['HSA'] = [0, 1, 0, 0, 0]
                result_predict['sEH'] = [0, 0, 1, 0, 0]

                result_predict.index = range(1,6)

                st.write("**Prediction** : ")
                st.write(result_predict[["molecule_smiles", "BRD4", "HSA", "sEH"]])

                for _ in range(2):
                    st.text("")

                col3, col4 = st.columns([1, 2])

                # result_predict['molecule_image'] = result_predict['molecule_smiles'].apply(lambda x: from_smile_to_viz(Chem.MolFromSmiles(x)))
                df = result_predict

                # Création du tableau
                col3, col4 , col5= st.columns(3)
                # Titres des colonnes
                with col3:
                    st.markdown("<p style='text-align: center; font-size:17px; font-weight: bold;'>Molecule ID</p>", unsafe_allow_html=True)
                with col4:
                    st.markdown("<p style='text-align: center; font-size:17px;font-weight: bold;'>Graphic representation</p>", unsafe_allow_html=True)
                with col5:
                    st.markdown("<p style='text-align: center; font-size:17px;font-weight: bold;'>Result</p>", unsafe_allow_html=True)

                st.markdown("<hr style='margin: 0; padding: 0;'>", unsafe_allow_html=True)

                for i, row in df.iterrows():
                    col3, col4 , col5= st.columns(3)

                    with col3: # Molecule ID
                        for _ in range(5):
                            st.text("")
                        # st.write(f'Molecule n°{i}')
                        st.markdown(f"<div style='display: flex; font-size:17px; justify-content: center; align-items: center; height: 100%;'><p>Molecule n°{i}</p></div>", unsafe_allow_html=True)

                    with col4: # Graphic representation
                        st.image(row['molecule_image'], width=200)

                    with col5: # Result
                        for _ in range(5):
                            st.text("")
                        if df.iloc[i-1]['BRD4']+df.iloc[i-1]['HSA']+df.iloc[i-1]['sEH'] == 0:
                            st.markdown(f"<p style='text-align: center; font-size:17px;'>Molecule n°{i} can't be used</p>", unsafe_allow_html=True)
                        else :
                            if df.iloc[i-1]['BRD4'] == 1:
                                st.markdown(f"<p style='text-align: center; font-size:17px;'>Molecule n°{i} could play a role in:</p>", unsafe_allow_html=True)

                                st.markdown("<p style='text-align: center; font-size:17px;font-weight: bold;'>reducing cancer progression</p>", unsafe_allow_html=True)
                            elif df.iloc[i-1]['HSA'] == 1:
                                st.markdown(f"<p style='text-align: center; font-size:17px;'>Molecule n°{i} may be:</p>", unsafe_allow_html=True)
                                st.markdown("<p style='text-align: center; font-size:17px;font-weight: bold;'>absorbed by the blood</p>", unsafe_allow_html=True)
                            elif df.iloc[i-1]['sEH'] == 1:
                                st.markdown(f"<p style='text-align: center; font-size:17px;'>Molecule n°{i} could play a role in:</p>", unsafe_allow_html=True)
                                st.markdown("<p style='text-align: center; font-size:17px;font-weight: bold;'>reducing diabetes progression</p>", unsafe_allow_html=True)

                    st.markdown("<hr style='margin: 0; padding: 0;'>", unsafe_allow_html=True)

            else:
                st.write("Error submission parquet file")
    else :
        st.warning("*parquet file missing*")
