import openai
import os
import re

import streamlit as st

from langchain import SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI 


# .envファイルから、OpenAI API keyを読み込む
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']


# データベースに接続
db_name = 'chinook.db'
db_url = 'sqlite:///' + db_name
tables = ['albums', 'artists', 'customers', 'employees', 'genres', 'invoice_items', 'invoices', 'media_types', 'playlists', 'playlist_track', 'tracks']

# データベースオブジェクトを作成
db = SQLDatabase.from_uri(
    database_uri=db_url,
    include_tables=tables,
    )


def main(question: str):
    # チャットモデルの作成
    llm = ChatOpenAI(model='gpt-3.5-turbo')

    # db_chainの作成
    db_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        verbose=True,
        return_intermediate_steps=True
        )
    
    response = db_chain(question)
    
    st.header('回答')
    st.write(response['result'])

    st.header('実行したSQLクエリ')
    st.code(get_query(response=response))


def get_query(response: dict) -> str:
    '''intermediate_stepsから、SQLクエリ部分を取得する関数'''
    # input部分を取得
    intermediate_steps = response['intermediate_steps']
    input = intermediate_steps[0]['input']

    # SQLクエリ部分を取得
    query = re.split('SQLQuery:|SQLResult:', input)[1]

    return query


if __name__ == '__main__':
    # タイトル
    st.title('Chincookデータベースの分析ツール')

    # メイン部分: 質問の入力と送信、結果の表示
    with st.form(key='question_form'):
        question = st.text_input(label='質問を入力してください。')
        submitted = st.form_submit_button(label='送信')
        if submitted:
            main(question=question)