import streamlit as st
from PIL import Image

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("# Kyler Eastman, PhD")
    st.markdown('''
Welcome to my homepage.  I'm an experienced data scientist focused on all aspects of the machine learning iteration process.
- [Email](kyler.eastman@gmail.com)
- [Linkedin](https://www.linkedin.com/in/kylereastman/)
- [Google Scholar](https://scholar.google.com/citations?user=uUwIlwcAAAAJ&hl=en)
- [Resume](https://github.com/keastman/streamlit_public/blob/main/simple_resume_2022e.pdf)
    ''')

with col2:
    image = Image.open('./profile_pic.png')
    st.image(image, width=250)
