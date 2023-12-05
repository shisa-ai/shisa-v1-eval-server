import sqlite3
import fastapi
import json
import random
import streamlit as st

# https://console.cloud.google.com/apis/credentials?project=augmxnt
# https://developers.google.com/identity/oauth2/web/guides/get-google-api-clientid
GOOGLE_CLIENT_ID = '8130903055-566cf38vgvpkik9ahkj386g19lhje6q2.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

conn = sqlite3.connect('eval-3.db')
conn.row_factory = sqlite3.Row

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

def display_two_item_selection():
    cursor = conn.cursor()
    # Select only shisa-mega-7b-v1.2 and shisa-mega-dpo-7b-v1.1 
    cursor.execute("SELECT name FROM models WHERE name in ('shisa-mega-7b-v1.2', 'shisa-mega-dpo-7b-v1.1') ORDER BY RANDOM()")
    rows = cursor.fetchall()
    model_1 = rows[0]['name']
    model_2 = rows[1]['name']

    # Random task
    row = cursor.execute('SELECT * FROM tasks ORDER BY RANDOM() LIMIT 1').fetchone()
    task = {key: row[key] for key in row.keys()}
    # st.write(task)

    # Decide if Japanese or English
    if not task['user_ja']:
        lang_choice = 'en'
    elif not task['user_en']:
        lang_choice = 'ja'
    else:
        lang_choice = random.choice(['en', 'ja'])
        lang_choice = 'en'


    # First response (random temp and run)
    row = cursor.execute("SELECT * FROM responses WHERE task_id = ? AND model = ? AND lang = ? ORDER BY RANDOM() LIMIT 1", (task['id'], model_1, lang_choice)).fetchone()
    # try:
    response_1 = {key: row[key] for key in row.keys()}
    # except:
    #    st.rerun()
    lang = response_1['lang']
    # st.write(lang)

    # Second response (same temp, random run)
    row = conn.execute('SELECT temp, response, id FROM responses WHERE task_id = ? AND model = ? AND temp = ? AND lang = ? ORDER BY RANDOM() LIMIT 1', (task['id'], model_2, response_1['temp'], response_1['lang'])).fetchone()
    response_2 = {key: row[key] for key in row.keys()}

    # Save Details
    details = {
        'temp': response_1['temp'],
        'task_id': task['id'],
        'response_1_id': response_1['id'],
        'response_2_id': response_2['id'],
        'lang': response_1['lang']
    }
    details = json.dumps(details)


    # Results...
    def match_result(result):
        print(f'{model_1} vs {model_2}: {result}')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO matches 
            (model_1, model_2, result, updated, details)
            VALUES
            (?, ?, ?, CURRENT_TIMESTAMP, ?)
        """, 
            (model_1, model_2, result, details)
        )
        conn.commit()
        cursor.close()

    if lang == 'en':
        local = {
            "header": "Which response do you like better?",
            "instructions": "Pick either A, B, or Draw. If both answers are bad, you can pick the less bad one, or if both are equally bad, pick Draw. You can also reload the page to just skip to the another one if you're not sure or don't want to answer.",
            "prompt": f"**Prompt:** {task['prompt_en']}",
            "user": f"**User:** {task['user_en']}",
            "assistant": f"**Assistant:** (Long answers may be truncated)",
            "draw": "**Draw**",
            "a": "**Select A**",
            "b": "**Select B**",
        }
    else:
        local = {
            "header": "どちらの返答がより好きですか？",
            "instructions": "A、B、または引き分けのいずれかを選んでください。どちらの答えも良くない場合は、よりマシな方を選ぶか、同じくらい悪い場合は引き分けを選んでください。確信がない場合や答えたくない場合は、ページを再読み込みして別の質問に進むこともできます。",
            "prompt": f"**プロンプト:** {task['prompt_ja']}",
            "user": f"**ユーザー:** {task['user_ja']}",
            "assistant": f"**アシスタント:** (長い回答は切り捨てられる場合があります)",
            "draw": "**引き分け**",
            "a": "**レスポンスA**",
            "b": "**レスポンスB**",
        }
        
    # Which response do you like better?
    st.header(local['header'])
    st.write(local['instructions'])
    st.write(local['prompt'])
    st.write(local['user'])
    st.write(local['assistant'])
    st.write(f"Temp: {response_1['temp']}")
    
    st.button(local['draw'], key="draw", on_click=match_result, args=['draw'])

    col1, col2 = st.columns(2)
    with col1:
        st.button(local['a'], key='win', on_click=match_result, args=['win'])
        st.markdown(response_1['response'])
    with col2:
        st.button(local['b'], key='loss', on_click=match_result, args=['loss'])
        st.markdown(response_2['response'])

    # st.write("")
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
