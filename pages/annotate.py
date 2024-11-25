import datetime
import json
import os
import random

import streamlit as st
import streamlit_shortcuts as sts


def switch_if_no_project_selected():
    if "selected_project" not in st.session_state:
        st.switch_page("continue_project.py")


def get_number_of_files(directory):
    return len(os.listdir(directory))


def stop_if_no_more_pairs(num_possible_ann):
    if num_possible_ann == 0:
        st.write("No annotations available. Please create some pairs.")
        if st.button("Create pairs", type="primary"):
            st.switch_page("create_pairs.py")
        st.stop()


def save_annotation(pair_data, img, pair_name, pair_path):
    pair_data["annotation"] = 0 if img == "img_a" else 1
    pair_data["author"] = st.session_state["user"]
    pair_data["date"] = str(datetime.datetime.now())
    with open(os.path.join(st.session_state.save_dir, pair_name), "w") as f:
        json.dump(pair_data, f)
    os.remove(pair_path)


def annotate():
    st.title(f"Project {st.session_state.selected_project}")

    to_annotate = get_number_of_files(st.session_state.to_annotate_dir)
    stop_if_no_more_pairs(to_annotate)

    st.write(f"There is :green[{to_annotate}] pairs to annotate.")

    pair_name = random.choice(os.listdir(st.session_state.to_annotate_dir))
    pair_path = os.path.join(st.session_state.to_annotate_dir, pair_name)

    with open(pair_path) as f:
        pair_data = json.load(f)
        img_a = st.session_state.source_dir + "/" + pair_data["img_a"]
        img_b = st.session_state.source_dir + "/" + pair_data["img_b"]

    col1, col2 = st.columns(2)
    with col1:
        st.image(img_a, width=300)
        if sts.button("A", shortcut="ArrowLeft", hint=True, on_click=None):
            save_annotation(pair_data, "img_a", pair_name, pair_path)
            st.rerun()

    with col2:
        st.image(img_b, width=300)
        if sts.button("B", shortcut="ArrowRight", hint=True, on_click=None):
            save_annotation(pair_data, "img_b", pair_name, pair_path)
            st.rerun()


annotate()
