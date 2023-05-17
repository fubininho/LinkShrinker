import requests
import streamlit as st
import pandas as pd
from link import Link

BACKEND_URL = 'http://localhost:5000'


def shorten_url(url):
    response = requests.post(f'{BACKEND_URL}/shorten', json={'url': url})
    data = response.json()
    short_link = data['short_link']
    link = Link(url, short_link)
    return link


def get_links():
    response = requests.get(f'{BACKEND_URL}/links')
    data = response.json()
    links = []
    for short_link, original_url in data.items():
        link = Link(original_url, short_link)
        links.append(link)
    return links


st.title('Link Shortener')

option = st.selectbox('Choose an action:', ('Shorten URL', 'View Shortened Links'))

if option == 'Shorten URL':
    url = st.text_input('Enter the URL to shorten:')
    if st.button('Shorten'):
        if url:
            link = shorten_url(url)
            st.success(f'Shortened URL: {BACKEND_URL}/{link.shortened_link}')
        else:
            st.warning('Please enter a URL.')

elif option == 'View Shortened Links':
    links = get_links()
    if links:
        df = pd.DataFrame([[link.shortened_link, link.original_link] for link in links], columns=['Shortened Link', 'Original Link'])
        st.write('Shortened Links:')
        st.dataframe(df)
    else:
        st.write('No shortened links available.')

