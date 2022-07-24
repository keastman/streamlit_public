import streamlit as st
from PIL import Image
import numpy as np
import streamlit.components.v1 as components
#import fit_utils as fu
import os
links = {
    'email':'mailto:/kyler.eastman@gmail.com)',
    'linkedin':'https://www.linkedin.com/in/kylereastman/)',
    'google_scholar':'https://scholar.google.com/citations?user=uUwIlwcAAAAJ&hl=en',
    'resume':'https://github.com/keastman/streamlit_public/blob/main/simple_resume_2022e.pdf',
    'profile_pic':'https://github.com/keastman/streamlit_public/raw/main/profile_pic.png'
    
}

image_links = {
    'email':'icons/email.webp',
    'linkedin':'icons/linkedin.png',
    'google_scholar':'icons/google_scholar.png',
    'resume':'icons/resume.webp',
    'profile_pic':'profile_pic.png'
}

def display_image(link,alt_text,image_link,width=100,height=100,base_url='https://github.com/keastman/streamlit_public/raw/main/'):        
    temp_html = '''<a href="%s"> <img alt="%s" src="%s" width=%s height=%s>''' %(link,alt_text,base_url+image_link,width,height)
    components.html(temp_html,width=width,height=height)

st.set_page_config(
     page_title="KME",
     layout="wide",
     initial_sidebar_state="collapsed",
     menu_items={
         'Report a bug': None,
         'About': "# Kyler's streamlit app. Hi!"
     }
 )

st.markdown("## Kyler Eastman, PhD")
cols = st.columns([1,1,1,1,1])

    
#c = st.container()
for i,l in enumerate(links):
    with cols[i]:
        display_image(links[l],l,image_links[l],base_url='file:///Users/kylereastman/Dropbox/Projects/streamlit_public/')
        #display_image(links[l],l,image_links[l])
        
# with col2:
#     components.html('<img src=https://github.com/keastman/streamlit_public/raw/main/profile_pic.png height=400 alt="profile pic">', height=400, width=400)
# components.html('<img src=https://github.com/keastman/streamlit_public/raw/main/profile_pic.png height=400 alt="profile pic">', height=400, width=400)
        x
        
# #components.html('<img src=file://./icons/google_scholar.jpeg height=100>')
# components.html('<img src=https://github.com/keastman/streamlit_public/raw/main/icons/aiga_mail-512.webp height=100>')
# #components.html('<img src=https://github.com/keastman/streamlit_public/raw/main/icons/hd-linkedin-square-black-icon-#transparent-background-11640440466zdofrsi3gy.png height=100>')
# #components.html('<img src=https://github.com/keastman/streamlit_public/raw/main/icons/resume.jpeg height=100>')
# with col2:
#     components.html('<img src=https://github.com/keastman/streamlit_public/raw/main/profile_pic.png height=400 alt="profile pic">', height=400, width=400)
    
