import requests
import streamlit as st
import pandas as pd
from link import Link
import webbrowser

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
            shortened_link = f'{BACKEND_URL}/{link.shortened_link}'
            st.success(f'Shortened URL: [{shortened_link}]({link.original_link})')
        else:
            st.warning('Please enter a URL.')

elif option == 'View Shortened Links':
    links = get_links()
    if links:
        data = [[f'<a href="{link.original_link}" target="_blank">{BACKEND_URL}/{link.shortened_link}</a>',
                 link.original_link] for link in links]
        df = pd.DataFrame(data, columns=['Shortened Link', 'Original Link'])
        st.write('Shortened Links:')
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.write('No shortened links available.')

