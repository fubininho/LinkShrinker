import requests
import streamlit as st

BACKEND_URL = 'http://localhost:5000'

st.title('Link Shortener')

option = st.selectbox('Choose an action:', ('Shorten URL', 'View Shortened Links'))

if option == 'Shorten URL':
    url = st.text_input('Enter the URL to shorten:')

elif option == 'View Shortened Links':
    st.write('Shortened Links:')

