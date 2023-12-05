from   glob import glob
import json
import os
import pandas as pd
from   pprint import pprint
import sqlite3
import sys

conn = sqlite3.connect('eval-2.db')
conn.execute('PRAGMA journal_mode=WAL;')

def main():
    create_schema()

    for file_path in glob('gen/*.json'):
        load_jsonfile(file_path)

def load_jsonfile(file_path):
    # Extracting the filename info
    filename = os.path.basename(file_path)
    model, temp, run = filename.replace('.json', '').split('_')
    insert_model(model)
    temp = float(temp.split('-')[1])
    run = int(run.split('-')[1])

    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        insert_gen(item, model, temp, run)


def create_schema():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS models (
            name VARCHAR PRIMARY KEY,
            path VARCHAR,
            notes VARCHAR,
            score REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT PRIMARY KEY,
            type VARCHAR,
            prompt_en VARCHAR,
            prompt_ja VARCHAR,
            user_en VARCHAR,
            user_ja VARCHAR
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INT,
            model VARCHAR,
            temp TEXT,
            run INT,
            lang VARCHAR,
            response VARCHAR,
            chat TEXT,
            UNIQUE(task_id, model, temp, run, lang)
        )
    """)
    # details should store, task id, and the responses id 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            model_1 VARCHAR,
            model_2 VARCHAR,
            result VARCHAR CHECK(result IN ('win', 'loss', 'draw')),
            updated TIMESTAMP,
            user VARCHAR,
            details TEXT
        )
    """)
    conn.commit()
    cursor.close()


def insert_model(model):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO models (name) VALUES (?)
    """, (model,))
    conn.commit()
    cursor.close()


def insert_gen(item, model, temp, run):
    cursor = conn.cursor()

    # Insert Task
    cursor.execute("""
        INSERT OR IGNORE INTO tasks (id, type, prompt_en, prompt_ja, user_en, user_ja) VALUES (?, ?, ?, ?, ?, ?)
    """, (item['task']['id'], item['task']['type'], item['task']['prompt_en'], item['task']['prompt_ja'], item['task']['user_en'], item['task']['user_ja']))

    # Insert Response
    chat = json.dumps(item['chat'])
    cursor.execute("""
        INSERT OR IGNORE INTO responses (task_id, model, temp, run, lang, response, chat) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (item['task']['id'], model, temp, run, item['lang'], item['response'], chat))
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    main()
