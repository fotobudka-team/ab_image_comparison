import json
import os

import streamlit as st

st.cache_data()


def get_project_config(project_name):
    st.write(project_name)
    project_config = json.load(open(f"./configs/{project_name}"))
    return project_config


def choose_project():
    st.title("Continue Project")

    projects = next(os.walk("./configs"))[2]
    projects = [p[:-5] for p in projects if p.endswith(".json")]
    selected_project = st.selectbox("Select project to continue", projects, index=None)

    if st.button("Start", disabled=selected_project is None, type="primary"):
        st.session_state.selected_project = selected_project
        project_config = get_project_config(selected_project + ".json")

        st.session_state["source_dir"] = project_config["input"]
        st.session_state["save_dir"] = project_config["output"] + "/annotations"
        st.session_state["to_annotate_dir"] = project_config["output"] + "/to_annotate"

        st.switch_page("annotate.py")


choose_project()
