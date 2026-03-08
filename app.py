from dotenv import load_dotenv
load_dotenv() ##load all the environement variables 

import streamlit as st 
import os 
import sqlite3
import google.generativeai as genai

## configure our API key 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

dangerous = ["drop","delete","update","insert"]

##Function to load google gemini model and provide a sql query as response 
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content([prompt, question])
    return response.text 

## Function to retrieve queries from the sql database 
## une fois qu'on a la requette sql , on doit maintenant l'executer dans la base de donnees 

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    curs.execute(sql)
    rows = curs.fetchall()
    conn.commit()
    conn.close()
    
    return rows 

## Define a prompt 

prompt = """
You are an expert in converting English questions to SQL queries.
The SQL database has the name STUDENT and has the following columns:
NAME, CLASS, SECTION, MARKS.

Example 1:
How many entries of records are present?
The SQL command will be:
SELECT COUNT(*) FROM STUDENT;

Example 2:
Tell me all the students studying in Data Science class?
The SQL command will be:
SELECT * FROM STUDENT WHERE CLASS="Data Science";

Also the SQL code should not have ''' at the beginning or end.
"""

## Streamlit App

st.set_page_config(page_title="AiRound assistant.")
st.title("🤖 AiRound Agent ")

st.markdown(
"""
Ask questions about your database in **natural language**.\n
I will convert them into SQL queries.
"""
)

icone_col, input_col = st.columns([1, 8])

with icone_col:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=60)

with input_col:
    with st.form(key="query_form", clear_on_submit=False):
        question = st.text_input(
            "",
            placeholder="Ask your database a question...",
            label_visibility="collapsed"
        )
        submit = st.form_submit_button("Run")

if submit:
    # by default , the submit button is false, and if a user clicks on it, it becomes True.
    with st.spinner("Working..."):
        response = get_gemini_response(question, prompt)
        # Nettoyage du markdown généré par Gemini
        response = response.replace("```sql", "").replace("```", "").strip()
        print(response)
        if any(word in response.lower() for word in dangerous):
            st.error("Dangerous SQL query blocked ! ")
        else:
            data = read_sql_query(response, "student.db")
            st.subheader("The response is ")
            st.table(data)

