import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

st.set_page_config(
     page_title="KME",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': None,
         'About': "# Kyler's streamlit app. Hi!"
     }
 )

col1, col2 = st.columns([3, 1])


with col1:
    st.markdown("# Kyler Eastman, PhD")
    st.markdown('''
        Welcome to my homepage.  I'm an experienced data scientist focused on all aspects of the machine learning iteration process.   
        ''')
    
#container1 = col1.container()
#c0,c1,c2,c3 = container1.columns(4)
links = [
    '[Email](kyler.eastman@gmail.com)',
    '[Linkedin](https://www.linkedin.com/in/kylereastman/)',
    '[Google Scholar](https://scholar.google.com/citations?user=uUwIlwcAAAAJ&hl=en)',
    '[Resume](https://github.com/keastman/streamlit_public/blob/main/simple_resume_2022e.pdf)'
    ]

with col1:
    for i in range(4):
        st.markdown(links[i])

#image = Image.open('./profile_pic.png')
#col2.image(image, width=250)
with col2:
    components.html('<img src=https://raw.githubusercontent.com/keastman/streamlit_public/548c7d325cce9dce63ae9dd95ac0403ce92f1249/profile_pic.png height=400 alt="profile pic">', height=400, width=400)