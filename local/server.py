import duckdb
import fastapi
import streamlit as st

# Define your pages as functions
def evaluation_page():
    st.header("Evaluation Page")
    # Your evaluation page content here

    # Example usage
    item1 = "Item 1 Description"
    item2 = "Item 2 Description"
    display_two_item_selection(item1, item2)

    item = "Single Item Description"
    question = "How would you rate this item?"
    options = ["Option 1", "Option 2", "Option 3"]
    display_single_item_with_question(item, question, options, is_slider=False)

def results_page():
    st.header("Results Page")
    # Your results page content here

def display_two_item_selection(item1, item2):
    st.header("Select Your Preferred Item")
    col1, col2 = st.columns(2)
    with col1:
        st.write(item1)
        if st.button('Select Item 1'):
            st.write("You selected Item 1")
    with col2:
        st.write(item2)
        if st.button('Select Item 2'):
            st.write("You selected Item 2")

def display_single_item_with_question(item, question, options, is_slider):
    st.header("Item Evaluation")
    st.write(item)
    st.write(question)
    if is_slider:
        rating = st.slider("Rate the item:", 1, 5)
        st.write(f"Rating: {rating}")
    else:
        answer = st.selectbox("Choose an answer:", options)
        st.write(f"You selected: {answer}")

# Sidebar for navigation
st.sidebar.title("Shisa / シーサー")
selection = st.sidebar.radio("Go to", ["Evaluation", "Results"])

# Page rendering based on selection
if selection == "Evaluation":
    evaluation_page()
elif selection == "Results":
    results_page()



def test():
    '''
    ---

    db:
    * models
    * tasks
    * responses

    * evals
      * instructions

    load:
    * load tasks
    * add models
    * create generations


    evals frontend:
    * Pick A/B ranking

# pykoi - cool but realtime
    https://www.ycombinator.com/launches/JA8-cambioml-the-private-engineer-for-ml-scientists-at-large-enterprises
    https://github.com/CambioML/pykoi/blob/main/example/comparator/demo_model_comparator_cpu_openai.ipynb
# 

    '''
    pass
