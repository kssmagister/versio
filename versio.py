import streamlit as st
import pandas as pd
import random

# Function to load the Excel file from the user's input
def load_data(file):
    return pd.read_excel(file)

# Initialize global variables
data = None

# Function to display the current sentence and vocabulary
def display_sentence(index):
    sentence = data.at[index, "satz"]
    vocabulary = data.at[index, "vok"]
    st.markdown(f'<p style="font-size: 24px;"><b>Sentence:</b> {sentence}</p>', unsafe_allow_html=True)
    st.markdown(f'*Vocabulary: {vocabulary}*')

# Function to display the input boxes for other columns
def display_input_boxes(index):
    subj_input = st.text_input("Subjekt", key=f"subj_input_{index}")
    praed_input = st.text_input("Prädikat", key=f"praed_input_{index}")
    akkobj_input = st.text_input("Akkusativobjekt", key=f"akkobj_input_{index}")
    datobj_input = st.text_input("Dativobjekt", key=f"datobj_input_{index}")
    adv_input = st.text_input("Adverbiale", key=f"adv_input_{index}")
    return subj_input, praed_input, akkobj_input, datobj_input, adv_input

# Function to check the inputs against the correct values
def check_inputs(index, subj, praed, akkobj, datobj, adv):
    correct_subj = data.at[index, "subj"]
    correct_praed = data.at[index, "praed"]
    correct_akkobj = data.at[index, "akkobj"]
    correct_datobj = data.at[index, "datobj"]
    correct_adv = data.at[index, "adv"]

    is_correct = (subj.strip() == correct_subj and
                  praed.strip() == correct_praed and
                  akkobj.strip() == correct_akkobj and
                  datobj.strip() == correct_datobj and
                  adv.strip() == correct_adv)

    return is_correct

# Streamlit app
def main():
    global data

    st.title("VERSIO")

    st.markdown("VERSIO is an app designed for analyzing basic German sentence structures and translating them into Latin.")

    # Add text and links to the sidebar
    st.sidebar.markdown("#### Additional Information")
    st.sidebar.markdown("1. [Vorlage der Excel-Datei](https://www.dropbox.com/scl/fi/ddjqy3hddilau3098ps10/pensum2.xlsx?rlkey=bt04i9fnefegouqlbic76nb68&dl=0)")
    st.sidebar.markdown("2. Wenn ein Satzglied leer bleibt, \"ka\" einfügen.")
    st.sidebar.markdown("3. Bei Adjektiven die Wortfolge des deutschen Satzes übernehmen, also: schönes Haus -> pulchra domus, NICHT domus pulchra.")

    # File uploader in the sidebar to allow users to upload their Excel file
    file = st.sidebar.file_uploader("Upload your Excel file", type=["xls", "xlsx"])

    # Initialize the session state for the app
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
        st.session_state.correct_count = 0
        st.session_state.user_inputs = {}

    if file is not None:
        # Load the Excel file using the load_data function, but don't use st.cache_data here
        data = load_data(file)

        # Move to the next sentence if the "Next" button is clicked
        if st.button("Next"):
            st.session_state.current_index = random.randint(0, len(data) - 1)
            st.session_state.user_inputs = {}  # Reset user inputs for the new sentence

        # Display the current sentence and vocabulary
        display_sentence(st.session_state.current_index)

        # Use st.form to separate the input box interactions from the rest of the app
        with st.form(key='my_form'):
            subj, praed, akkobj, datobj, adv = display_input_boxes(st.session_state.current_index)

            # Store the user inputs for the current sentence
            st.session_state.user_inputs = {
                "subj": subj.strip(),
                "praed": praed.strip(),
                "akkobj": akkobj.strip(),
                "datobj": datobj.strip(),
                "adv": adv.strip(),
            }

            # Check if the inserted text is correct
            if st.form_submit_button(label="Check"):
                is_correct = check_inputs(st.session_state.current_index, subj, praed, akkobj, datobj, adv)

                if is_correct:
                    st.write("Correct!")
                    st.session_state.correct_count += 1
                else:
                    st.write("Incorrect! Es hat noch (einen) Fehler.")

        st.write(f"Score: {st.session_state.correct_count} / {st.session_state.current_index + 1}")

if __name__ == "__main__":
    main()
