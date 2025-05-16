import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from email_chain import Chain
from my_portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(chain, portfolio, clean_text):
    st.title("Email generator")
    url_input = st.text_input("Enter an URL:", value = "")
    submit_button = st.button("submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = chain.extract_job_details(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = chain.write_email(job, links)
                st.code(email, language = 'markdown')
        except Exception as e:
            st.error(f"An error occured: {e}")

if __name__ == "__main__":
    chain = Chain()
    my_portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Email Generator")
    create_streamlit_app(chain, my_portfolio, clean_text)