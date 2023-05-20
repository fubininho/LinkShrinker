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
    selected_link = None  # Initialize selected_link as None
    if links:
        data = [[f'<a href="{BACKEND_URL}/{link.shortened_link}" target="_blank">{BACKEND_URL}/{link.shortened_link}</a>',
                 link.original_link] for link in links]
        df = pd.DataFrame(data, columns=['Shortened Link', 'Original Link'])
        st.write('Shortened Links:')
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        delete_clicked = st.button("Select a link to be Deleted")
        if delete_clicked:
            selected_link = st.selectbox("Select a link to delete", links, format_func=lambda link: link.shortened_link)
            if selected_link:
                delete_response = requests.delete(f'{BACKEND_URL}/links?shortened_link={selected_link.shortened_link}')
                if delete_response.status_code == 200:
                    st.success(f"Link {selected_link.shortened_link} deleted successfully.")
                    links.remove(selected_link)
                    selected_link = None  # Reset selected_link to None after successful deletion
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to delete link {selected_link.shortened_link}.")
    else:
        st.write('No shortened links available.')

