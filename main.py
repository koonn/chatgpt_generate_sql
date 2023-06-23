import openai
import os

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


def main():
    # データベースオブジェクトを作成
    db = SQLDatabase.from_uri(
        database_uri=db_url,
        include_tables=tables,
        )

    # チャットモデルの作成
    llm = ChatOpenAI(model='gpt-3.5-turbo')

    # db_chainの作成
    db_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        verbose=True
        )
    
    db_chain.run("顧客データは何件あるか教えてください。")


if __name__ == '__main__':
    main()