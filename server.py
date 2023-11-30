import duckdb
import fastapi
import json
import streamlit as st

con = duckdb.connect('eval.db')

# Define your pages as functions
def evaluation_page():
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        margin: auto;
        display: block;
    }
    div.stButton * {
        text-align: left;
    }
    </style>""", unsafe_allow_html=True)

    # Example usage
    display_two_item_selection()

    # item = "Single Item Description"
    # question = "How would you rate this item?"
    # options = ["Option 1", "Option 2", "Option 3"]
    # display_single_item_with_question(item, question, options, is_slider=False)


def results_page():
    st.header("Results Page")
    # Your results page content here

def display_two_item_selection():
    # Random models
    result = con.execute('SELECT name FROM models ORDER BY RANDOM() LIMIT 2').fetchall()
    model_1 = result[0][0]
    model_2 = result[1][0]

    # Random task
    result = con.execute('SELECT id, prompt_ja, user_ja FROM tasks WHERE user_ja IS NOT NULL ORDER BY RANDOM() LIMIT 1').fetchall()
    task_id = result[0][0]
    prompt_ja = result[0][1]
    user_ja = result[0][2]

    # First response (random temp and run)
    result = con.execute('SELECT temp, response, id FROM responses WHERE task_id = ? AND model = ? ORDER BY RANDOM() LIMIT 1', (task_id, model_1)).fetchall()
    temp = result[0][0]
    response_1 = result[0][1]
    response_1_id = result[0][2]

    # Second response (same temp, random run)
    result = con.execute('SELECT temp, response, id FROM responses WHERE task_id = ? AND model = ? AND temp = ? ORDER BY RANDOM() LIMIT 1', (task_id, model_2, temp)).fetchall()
    response_2 = result[0][1] 
    response_2_id = result[0][2]

    # Save Details
    details = {
        'temp': float(temp),
        'task_id': task_id,
        'response_1_id': response_1_id,
        'response_2_id': response_2_id,
    }
    details = json.dumps(details)


    # Which response do you like better?
    st.header("どちらの返答がより好きですか？")

    # Prompt
    st.write("**プロンプト:**", prompt_ja)

    # User
    st.write("**ユーザー:**", user_ja)

    # Assistant
    st.write("**アシスタント:** (最初の500トークン)")


    # Results...
    def match_result(result):
        print(result)
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO matches 
            (model_1, model_2, result, updated, details)
            VALUES
            (?, ?, ?, NOW(), ?)
        """, 
            (model_1, model_2, result, details)
        )
        con.commit()
        cursor.close()

    st.button("**引き分け**", key="draw", on_click=match_result, args=['draw'])

    col1, col2 = st.columns(2)
    with col1:
        st.button('**レスポンスA**', key='win', on_click=match_result, args=['win'])
        st.markdown(response_1)
    with col2:
        st.button('**レスポンスB**', key='loss', on_click=match_result, args=['loss'])
        st.markdown(response_2)

    st.write("")
    # If it's hard to choose which is better
    # st.write("どちらが良いか選ぶのが難しい場合は:")
    # Draw


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


### Sidebar for navigation
# st.sidebar.title("Shisa / シーサー")
# selection = st.sidebar.radio("Go to", ["Evaluation", "Results"])
# selection = st.sidebar.radio("Go to", ["Evaluation"])


# Page rendering based on selection
# if selection == "Evaluation":
evaluation_page()
# elif selection == "Results":
#    results_page()
