import os

import streamlit as st

st.session_state["user"] = os.environ.get("USER")


def create_pages():
    home_page = st.Page("home.py", title="Home", icon=":material/home:", default=True)
    create_page = st.Page(
        "create_project.py", title="Create New Project", icon=":material/add_circle:"
    )
    continue_page = st.Page(
        "continue_project.py", title="Projects", icon=":material/arrow_forward:"
    )
    annotate_page = st.Page(
        "annotate.py", title="Annotate", icon=":material/data_object:"
    )
    create_pairs_page = st.Page(
        "create_pairs.py", title="Create Pairs", icon=":material/compare:"
    )

    pg = st.navigation(
        [home_page, create_page, continue_page, annotate_page, create_pairs_page]
    )
    pg.run()


create_pages()
