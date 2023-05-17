import requests
import streamlit as st

BACKEND_URL = 'http://localhost:5000'

def shorten_url(url):
    response = requests.post(f'{BACKEND_URL}/shorten', json={'url': url})
    data = response.json()
    return data['short_link']

def get_links():
    response = requests.get(f'{BACKEND_URL}/links')
    data = response.json()
    return data

st.title('Link Shortener')

option = st.selectbox('Choose an action:', ('Shorten URL', 'View Shortened Links'))

if option == 'Shorten URL':
    url = st.text_input('Enter the URL to shorten:')
    if st.button('Shorten'):
        if url:
            short_link = shorten_url(url)
            st.success(f'Shortened URL: {BACKEND_URL}/{short_link}')
        else:
            st.warning('Please enter a URL.')

elif option == 'View Shortened Links':
    links = get_links()
    st.write('Shortened Links:')
    for short_link, original_url in links.items():
        st.write(f'- [{short_link}]({original_url})')

