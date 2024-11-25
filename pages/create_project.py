import json
import os

import streamlit as st


def directory_selector(key, folder_path="./data"):
    directories = next(os.walk(folder_path))[1]
    selected_dir = st.selectbox(f"Select {key} directory", directories, key=key)
    return os.path.join(folder_path, selected_dir)


def count_files(folder_path):
    return len(os.listdir(folder_path))


def validate_output_directory():
    if os.path.exists("./data/" + st.session_state.output_dir):
        st.error(
            f"The directory {st.session_state.output_dir} already exists. Please choose another name."
        )
        st.session_state.output_directory_exists = True
    else:
        st.session_state.output_directory_exists = False


def validate_project_name():
    if os.path.exists("./configs/" + st.session_state.project_name + ".json"):
        st.error(
            f"The project {st.session_state.project_name} already exists. Please choose another name."
        )
        st.session_state.project_name_exists = True
    else:
        st.session_state.project_name_exists = False


def create_project_config(project_name, input_directory, output_directory):
    config = {
        "name": project_name,
        "input": input_directory,
        "output": "./data/" + output_directory,
    }

    os.makedirs("./configs/", exist_ok=True)
    os.makedirs("./data/" + output_directory + "/annotations", exist_ok=True)
    os.makedirs("./data/" + output_directory + "/to_annotate", exist_ok=True)
    json.dump(config, open("./configs/" + project_name + ".json", "w"))

    st.success(
        f'Project {project_name} created successfully! You can find it in the "Projects" tab.'
    )

    st.session_state.output_dir = ""
    st.session_state.project_name = ""


def create_project():
    if "output_dir" not in st.session_state or st.session_state.output_dir == "":
        st.session_state["output_directory_exists"] = True
    if "project_name" not in st.session_state or st.session_state.project_name == "":
        st.session_state["project_name_exists"] = True

    st.title("Create New Project")

    # Select project name
    project_name = st.text_input(
        "Set project name", "", on_change=validate_project_name, key="project_name"
    )

    # select input directory
    input_directory = directory_selector(key="input_dir")
    num_images = count_files(input_directory)
    st.write(
        f"You selected :green[{input_directory}] with :green[{num_images}] images. You can get up to :green[{num_images * (num_images - 1) // 2}] pairs"
    )

    # select output folder
    output_directory = st.text_input(
        "Create output directory",
        "",
        on_change=validate_output_directory,
        key="output_dir",
    )
    st.button(
        "Create",
        disabled=st.session_state.get("output_directory_exists", False)
        or st.session_state.get("project_name_exists", False),
        on_click=lambda: create_project_config(
            project_name, input_directory, output_directory
        ),
        type="primary",
    )


create_project()
