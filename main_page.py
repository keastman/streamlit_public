import streamlit as st
import numpy as np
import streamlit.components.v1 as components

import os
links = {
    'email':'mailto:/kyler.eastman@gmail.com)',
    'linkedin':'https://www.linkedin.com/in/kylereastman/',
    'google_scholar':'https://scholar.google.com/citations?user=uUwIlwcAAAAJ&hl=en',
    'resume':'https://github.com/keastman/streamlit_public/blob/main/simple_resume_2022e.pdf',
}

image_links = {
    'email':'icons/email.webp',
    'linkedin':'icons/linkedin.png',
    'google_scholar':'icons/google_scholar.jpeg',
    'resume':'icons/resume.webp',
}

def display_image(link,alt_text,image_link,width=50,height=50,
                  base_url='https://github.com/keastman/streamlit_public/raw/main/'):        
    temp_html = '''<a href="%s" target="_blank"> <img alt="%s" src="%s" width=%s height=%s>''' %(
        link,alt_text,base_url+image_link,width,height)
    components.html(temp_html,width=width+10,height=height+10)

st.set_page_config(
     page_title="KME",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Report a bug': None,
         'About': "# Kyler's streamlit app. Hi!"
     }
 )


c1 = st.columns([3,1,1,1,1])

c1[0].markdown("### Kyler Eastman, PhD")    

for i,l in enumerate(links):
    with c1[i+1]:
        display_image(links[l],l,image_links[l])
        
c2 = st.columns([2,1])


# with c2[1]:
#     display_image('','','profile_pic.png',324,420)      

