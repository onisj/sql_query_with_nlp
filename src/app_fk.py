from flask import Flask, request, render_template
import openai
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def translate_to_sql(natural_language_query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Translate the following natural language query into SQL: {natural_language_query}",
        max_tokens=150
    )
    sql_query = response.choices[0].text.strip()
    return sql_query

def execute_sql_query(sql_query):
    connection = mysql.connector.connect(
        host='db',
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        natural_language_query = request.form['query']
        sql_query = translate_to_sql(natural_language_query)
        results = execute_sql_query(sql_query)
        return render_template('index.html', query=natural_language_query, sql_query=sql_query, results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
