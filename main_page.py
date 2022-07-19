import streamlit as st

st.markdown("# Kyler Eastman ")
st.sidebar.markdown("# Contents")

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('''
    Welcome to my homepage.  I'm an experienced data scientist focused on all aspects of the machine learning iteration process. 
    - [kyler.eastman@gmail.com](kyler.eastman@gmail.com)
    - [linkedin](https://www.linkedin.com/in/kylereastman/)
    - [google scholar](https://scholar.google.com/citations?user=uUwIlwcAAAAJ&hl=en)

    ''')

with col2:
    st.image('./profile_pic.png', width=150)

