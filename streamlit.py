import streamlit as st
import speech_recognition as sr
import pyttsx3
import pandas as pd
import pymysql.cursors
import csv
import numpy as np
import time

displayText = []
# Create placeholders for question and answer
# qa_placeholder = st.empty()

# Function to create the database if it doesn't exist
def create_database():
    connection = pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='Piyu#9263',
        database='haka',
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS haka")
        connection.commit()
    connection.close()

# Call the function to create the database
create_database()

# Connect to the MySQL database
connection = pymysql.connect(
    host='localhost',
        port=3307,
        user='root',
        password='Piyu#9263',
        database='haka',
    cursorclass=pymysql.cursors.DictCursor
)

# Function to create the table if it doesn't exist
def create_table():
    with connection.cursor() as cursor:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS question_answers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question VARCHAR(255),
            answer VARCHAR(255)
        )
        """
        cursor.execute(create_table_sql)
        connection.commit()

# Call the function to create the table
create_table()

# Function to insert data into the MySQL database
def insert_question_answer(question, answer):
    with connection.cursor() as cursor:
        DB_table_name = 'question_answers'
        insert_sql = "INSERT INTO " + DB_table_name + " (question, answer) VALUES (%s, %s)"
        rec_values = (question, answer)
        cursor.execute(insert_sql, rec_values)
        connection.commit()

# Function to fetch data from MySQL
def fetch_data():
    with connection.cursor() as cursor:
        cursor.execute("SELECT question, answer FROM question_answers")
        data = cursor.fetchall()
    return data

# Define function to convert text to speech
def speak(text):
    engine = pyttsx3.init()
    # engine.say(text)
    engine.runAndWait()

# Define function to play video and get audio input
def play_video_and_get_audio(video_path, video_placeholder):
    video_placeholder.video(video_path)
    # st.video(video_path, start_time=0, autoplay=True, loop=False, format='video/mp4', width=None, height=None, key=None)
    # st.video(video_path, format="video/mp4", start_time=0,  subtitles=None, end_time=None, loop=False)

def get_audio(question):
    global displayText
    displayText = []
    recognizer = sr.Recognizer()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    vID=1
    vName="siri"
    engine.setProperty('voice',voices[vID].id)

    st.write(f'Question : {question}')
    # displayText.append(f'Question : {question}')

    with sr.Microphone() as source:
        # speak("Listening")
        engine.say("Listening...")
        st.write("Listening...")
        # displayText.append("Listening...")
        
        engine.runAndWait()
        recognizer.pause_threshold=1
        recognizer.energy_threshold=800
        audio = recognizer.listen(source)
        try:
            # label["text"] = "Recognising..."
            query = recognizer.recognize_google(audio, language='en-in')
            # speak("You said " + query)
            engine.say("You said " + query)
            st.write("You said " + query)
            # displayText.append("You said " + query)
            
            engine.runAndWait()
        except Exception as e:
            # print(e)
            # speak("Say that again please....")
            engine.say("Say that again please....")
            st.write("Say that again please....")
            # displayText.append("Say that again please....")            
            engine.runAndWait()
            return None
        
        return query

    # # speak(question)
    # st.write(question)
    # recognizer = sr.Recognizer()

    # with sr.Microphone() as source:
    #     st.write("Speak now...")
    #     recognizer.adjust_for_ambient_noise(source)
    #     audio = recognizer.listen(source)

    # try:
    #     text = recognizer.recognize_google(audio)
    #     return text
    # except sr.UnknownValueError:
    #     st.write("Sorry, I couldn't understand your audio.")
    # except sr.RequestError as e:
    #     st.write("Error:", e)

# def updateQueAns(que,ans):


def main():
    global displayText
    # displayText = []
    st.title("Avatar Interviewing")
    # for msg in displayText:
    #     st.write(displayText)
    # st.set_page_config(page_title="Grammar Type Checker", page_icon=":memo:")
#     problems = ["Tell me about your self",
# "What was your percentage in last semester ?",
# "Whats the project you have done ? ",
# "Why should we hire you ?",
# "Do you have any experiance for the same role ?",
# "can you describe any challenging project you worked on and how you over come it ?",
# "How do you handle stress in pressure ?",
# "What do you know about our compony and our industrie ?",
# "Where do see yourself in five years ?",
# "Why did you leave your last job ?"]
    
    # Load custom CSS
    st.markdown(
        f"""
        <style>
        {open("st.css").read()}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create placeholder for video
    video_placeholder = st.empty()
    # qa_placeholder = st.empty()
    
    
    chat_placeholder = st.empty()  # Placeholder for chat messages
    
    # videos = ["q0.mp4", "q1.mp4", "q2.mp4", "q3.mp4", "q4.mp4","q4.mp4","q5.mp4","q6.mp4","q7.mp4","q8.mp4","q9.mp4"]
    videos = ["q0.mp4", "q1.mp4", "q2.mp4"]
    idx=0
    # df = pd.DataFrame(columns=['Question','Answer'])
    # st.write(df)
    problems = ["Tell me about your self",
            "What was your percentage in last semester ?",
            "Whats the project you have done ? "]
    answers = []

    for video_path in videos:
        # displayText=[]
        play_video_and_get_audio(video_path, video_placeholder)
        # displayText.append(problems[idx])
        # qa_placeholder.write(problems[idx])
        user_response = None
        while user_response == None:
            user_response = get_audio(problems[idx])
        # qa_placeholder.write(user_response)
        
        # time.sleep(2)
        # qa_placeholder.empty()
        # displayText.append(user_response)
        answers.append(user_response)
        # st.write("User's response: ", user_response)
        
        # # Append user response to the chat
        # chat_placeholder.text(f"User: {user_response}")
        # df = df.append({'Question': problems[idx], 'Answer': user_response}, ignore_index=True)

        user_response = None
        idx+=1

    answers = answers[:len(answers)]
    for question, answer in zip(problems, answers):
         insert_question_answer(question, answer)

    
    df = pd.DataFrame({'Question': problems, 'Answer': answers})

    st.write(df)
    # df.to_excel("Output.csv","w")




    
if __name__ == "__main__":
    main()