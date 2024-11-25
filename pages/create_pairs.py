import json
import os
import random

import streamlit as st


def switch_if_no_project_selected():
    if "selected_project" not in st.session_state:
        st.switch_page("continue_project.py")


def toast_if_created_new_pairs():
    if "created_new_pairs" in st.session_state:
        st.toast(f"{st.session_state.created_new_pairs} pairs created successfully!")
        del st.session_state.created_new_pairs


def get_number_of_files(directory):
    return len(os.listdir(directory))


def stop_if_no_more_pairs(num_possible_ann, num_to_ann, num_annotated):
    if num_possible_ann == 0:
        st.write(
            f"All possible pairs creted, in which :green[{num_to_ann} waiting to be annotated] and :green[{num_annotated} already annotated]. Start anotating now."
        )
        if st.button("Anotate", type="primary"):
            st.switch_page("annotate.py")
        st.stop()


def create_new_pairs(num_pairs_to_create):
    images = os.listdir(st.session_state.source_dir)
    existing_pairs = os.listdir(st.session_state.to_annotate_dir) + os.listdir(
        st.session_state.save_dir
    )

    def get_valid_pair():
        while True:
            pair = random.sample(images, 2)
            pair.sort()
            pair_annotation = f'{pair[0].split(".")[0]}_{pair[1].split(".")[0]}.json'
            if pair_annotation not in existing_pairs:
                return pair, pair_annotation

    text = "Generating pairs. Please wait."
    progress_bar = st.progress(0.0, text=text)

    for i in range(num_pairs_to_create):
        pair, annotation_name = get_valid_pair()
        annotation = {
            "img_a": pair[0],
            "img_b": pair[1],
            "annotation": None,
            "author": None,
            "date": None,
        }
        json.dump(
            annotation,
            open(f"{st.session_state.to_annotate_dir}/{annotation_name}", "w"),
        )
        existing_pairs.append(annotation_name)
        progress_bar.progress((i + 1) / num_pairs_to_create, text=text)

    progress_bar.empty()


def create_pairs():
    switch_if_no_project_selected()
    toast_if_created_new_pairs()

    st.title(f"Create pairs for project {st.session_state.selected_project}")

    num_to_ann = get_number_of_files(st.session_state.to_annotate_dir)
    num_annotated = get_number_of_files(st.session_state.save_dir)
    num_possible_ann = get_number_of_files(st.session_state.source_dir)
    num_possible_ann = (
        num_possible_ann * (num_possible_ann - 1) // 2 - num_to_ann - num_annotated
    )

    stop_if_no_more_pairs(num_possible_ann, num_to_ann, num_annotated)

    st.write(
        f"You have :green[{get_number_of_files(st.session_state.to_annotate_dir)} pairs to annotate]. You can get up to :green[{num_possible_ann} new pairs]."
    )
    num_pairs_to_create = st.number_input(
        "Number of pairs to create",
        min_value=1,
        max_value=num_possible_ann,
        value=1,
        key="num_pairs",
    )

    if st.button("Create pairs"):
        create_new_pairs(num_pairs_to_create)
        st.session_state.created_new_pairs = num_pairs_to_create
        st.rerun()


create_pairs()
