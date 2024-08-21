import streamlit as st

st.markdown(""" 💊 Drug & Smile 💊 """)

direction = st.radio('Select a model', ('Random Forest', 'GNN', 'Logistic Regression'))

st.write(direction)

if direction == 'top':
    st.write('🔼')
elif direction == 'right':
    st.write('▶️')
elif direction == 'bottom':
    st.write('🔽')
else:
    st.write('◀️')
