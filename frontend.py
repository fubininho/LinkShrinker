import requests
import streamlit as st
import pandas as pd
from link import Link
import webbrowser

BACKEND_URL = 'http://127.0.0.1:5000'


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

def render_shorten_input():
    url = st.text_input('Enter the URL to shorten:')
    if st.button('Shorten'):
        if url:
            link = shorten_url(url)
            shortened_link = f'{BACKEND_URL}/{link.shortened_link}'
            st.success(f'Shortened URL: [{shortened_link}](http://{link.shortened_link})', icon='🤩')
        else:
            st.warning('Please enter a URL.')

def delete_link(shortened_link):
    requests.delete(f'{BACKEND_URL}/links?shortened_link={shortened_link}')


def render_link_table():
    links = get_links()
    if links:
        data = []
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f'Encurtado')
        with col2:
            st.write(f'Original')
        with col3:
            st.write(f'Ações')
        for link in links:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f'[short.ly/{link.shortened_link}]({BACKEND_URL}/{link.shortened_link})')
            with col2:
                st.write(f'[http://{link.original_link}](http://{link.original_link})')
            with col3:
                 if st.button("delete", key=link.shortened_link):
                    delete_link(link.shortened_link)
                    st.experimental_rerun()

    

option = st.selectbox('Choose an action:', ('Shorten URL', 'View Statistics', 'View Logs'))

if option == 'Shorten URL':
    st.title('Link Shortener')
    render_shorten_input()
    render_link_table()
elif option == 'View Statistics':
    response = requests.get(f'{BACKEND_URL}/stats?number_of_clicks=true')
    data = response.json()
    st.write('Number of Clicks:')
    st.write(pd.DataFrame(data))


elif option == "View Logs":
    response = requests.get(f'{BACKEND_URL}/stats?number_of_clicks=false')
    data = response.json()
    st.write('Logs:')
    st.write(pd.DataFrame(data))