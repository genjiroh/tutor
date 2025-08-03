#/usr/bin/python3
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
#Importing required libraries 

from contextlib import redirect_stderr, redirect_stdout
from llama_cpp import Llama
import pyttsx3

import time

import requests

from bs4 import BeautifulSoup

import os

engine = pyttsx3.init()

#----------------------------------------------------------------------------------------------------
# Loading model -
#----------------------------------------------------------------------------------------------------

with open("/home/faisal/Trash/trash.txt", "w") as trash:

    with redirect_stderr(trash), redirect_stdout(trash):

        model = Llama(model_path="/home/faisal/.cache/huggingface/hub/models--bartowski--gemma-2-2b-it-GGUF/snapshots/855f67caed130e1befc571b52bd181be2e858883/gemma-2-2b-it-Q8_0.gguf", verbose=False, n_ctx=32000)

default_prompt = "You are a friendly tutor for a class 6 student. Explain answers to the student in simple words. Your name is gemma. Dont introduce yourself unless you are asked to. Never ever make responses above 200 tokens even when asked to!. talk to the student as if you were friends. End responses with questions that the student may have. When you are quizzing the student, check if the students answers are correct and if it isn't correct, explain to them why it isn't. If you want to search something from the web, reply with the word html followed by the thing you want to search, this response should only contain the word html and the thing you want to search"

speech = False

tts_model = ""  

sentence = []


#----------------------------------------------------------------------------------------------------
# Setting up default chat_history 
#----------------------------------------------------------------------------------------------------

chat_history = [
{"role": "user", "content": default_prompt},

{"role": "assistant", "content": "Ok, understood"}

]



#----------------------------------------------------------------------------------------------------
#Main loop 
#----------------------------------------------------------------------------------------------------

while True:

    question = input("You: ")
    
#----------------------------------------------------------------------------------------------------
    # Configure tutor settings
#----------------------------------------------------------------------------------------------------
    
    if question.lower() == "configure":
                
        question = None
    
#----------------------------------------------------------------------------------------------------
        # Student Name
#----------------------------------------------------------------------------------------------------
    
        name = input("Name: ")
    
#----------------------------------------------------------------------------------------------------
        # Tutor Name
#----------------------------------------------------------------------------------------------------
    

        tname = input("Tutor Name: ")
    
#----------------------------------------------------------------------------------------------------
        # Teaching Style
#----------------------------------------------------------------------------------------------------
    
        print("Teaching style: ")
        
        print("[1] Short and quick answers")
        
        print("[2] Detailed and long answers")
        
        style = input("Choose a teaching style (1 or 2): ")
    
#----------------------------------------------------------------------------------------------------
        # Configuring Style prompt based on input
#----------------------------------------------------------------------------------------------------
    
        if style == "1":
        
            style = "Respond to the student's questions with short and quick answers"
        
        elif style == "2":
        
            style = "Respond to the student's questions with detailed and long answers"
        
        else:
        
            print("Invalid Teaching Style")
        
            time.sleep(1)
        
            print("Setting teaching style to default: Short and quick answers")
        
            style = "Respond to the student's questions with short and quick answers"
    
#----------------------------------------------------------------------------------------------------
        # Quiz difficulty
#----------------------------------------------------------------------------------------------------
    
        print("Quiz difficulty: ")
        
        print("[1] Easy")
        
        print("[2] Medium")
        
        print("[3] Hard")
        
        difficulty = input("Choose Quiz difficulty (1,2 or 3): ")
        
        difficulty.strip()
    
#----------------------------------------------------------------------------------------------------
        # Condifuring difficulty prompt based on input
#----------------------------------------------------------------------------------------------------
    
        if difficulty == "1":
        
            difficulty = "The quiz questions you ask the student should be easy"
        
        elif difficulty == "2":
        
            difficulty = "The quiz questions that you ask the student shouldn't be too hard or too easy"
        
        elif difficulty == "3":
        
            difficulty = "The quiz questions that you ask the student should be hard"
        
        else:
        
            print("Invalid Difficulty")
        
            time.sleep(1)
        
            print("Setting difficulty to default: Medium")
        
            difficulty = "The quiz questions that you ask the student shouldn't be too hard or too easy"
    
#----------------------------------------------------------------------------------------------------
        # Tone
#----------------------------------------------------------------------------------------------------
    
        print("Tone: ")
        
        print("[1] Professional")
        
        print("[2] Fun and Silly")
        
        tone = input("Choose a Tone (1 or 2): ")
        
        tone.strip()
    
#----------------------------------------------------------------------------------------------------
        # Configuring Tone based on input
#----------------------------------------------------------------------------------------------------
    
        if tone == "1":
        
            tone = "Answer the students question in a professional way"
        
        elif tone == "2":
        
            tone = "Answer the students question in a fun and silly way"
        
        else:
        
            print("Invalid Tone")
        
            time.sleep(1)
        
            print("Setting tone to default tone: Professional")
        
            tone = "Answer the students question in a professional way"
    
#----------------------------------------------------------------------------------------------------
        # Response Type
#----------------------------------------------------------------------------------------------------
    
        print("Response type: ")
        
        print("[1] Text only")
        
        print("[2] Voice only")
        
        print("[3] Text & Voice")
        
        output = input(" Choose a response type(1,2 or 3): ")
    
#----------------------------------------------------------------------------------------------------
        # Asking for TTS model if they chose an option that contains speech
#----------------------------------------------------------------------------------------------------
    
        if output == "2" or "3":
        
            print("Choose a TTS model for speech: ")
        
            print("[1] pyttsx3: Robotic Voice")
        
            print("[2] Dia-1.6B: Realistic Human-like Voice")
        
            tts = input("Choose a model(1 or 2): ")
    
#----------------------------------------------------------------------------------------------------
            # Warning user about hardware consumption when using Dia-1.6B
#----------------------------------------------------------------------------------------------------
    
            if tts == "2":
        
                print("Warning!: Dia-1.6B consumes lots of hardware and can result in a bad experience.")
        
                print("Note: Using Dia-1.6B requires it to be installed. It will be installed automatically if it isn't")
    
#----------------------------------------------------------------------------------------------------
                # Asking for confirmation
#----------------------------------------------------------------------------------------------------
    
                confirm = input("Are you sure (y/n): ")

                if confirm == "y":
        
                    speech = True
        
                    tts_model = "Dia-1.6B"
        
                elif confirm == "n":
    
#----------------------------------------------------------------------------------------------------
                    # Re-asking model-
#----------------------------------------------------------------------------------------------------
    
                    print("Choose a TTS model for speech: ")
        
                    print("[1] pyttsx3: Robotic Voice")
        
                    print("[2] Dia-1.6B: Realistic Human-like Voice")
        
                    tts = input("Choose a model(1 or 2): ")
        
                    if tts == "1":
        
                        speech = True
        
                        tts_model = "pyttsx3"

                        emoji = "Never ever use emojis in responses"                   
        
                    if tts == "2":
        
                        speech = True
        
                        tts_model = "Dia-1.6B"
            elif tts == "1":

                speech = True

                tts_model = "pyttsx3"

                emoji = "Never ever use emojis in responses"
#----------------------------------------------------------------------------------------------------
        # Changing prompt based on the overall configuration
#----------------------------------------------------------------------------------------------------
    
        prompt = "You are a friendly tutor for a class 6 student." + style + ". Your name is " + tname + ". The student's name is " + name + ". Don't introduce yourself unless you are asked to. Talk to the student as if you were best friends." + tone + "." + emoji + ". End responses with questions that the student may have. When you are quizzing the student, check if the students answers are correct and if it isn't correct, explain to them why it isn't." + difficulty
    
#----------------------------------------------------------------------------------------------------
        # Changing the prompt only from chat_history
#----------------------------------------------------------------------------------------------------
    
        chat_history[0]['content'] = prompt
    
#----------------------------------------------------------------------------------------------------
    # Checking if question is nothing to avoid spamming and glitching the AI
#----------------------------------------------------------------------------------------------------
    
    if question == "":
    
#----------------------------------------------------------------------------------------------------
        # Asking for a valid input until it gives one
#----------------------------------------------------------------------------------------------------
    
        while question == "":
    
            print("Invalid input: No text found")
    
            question = input("You:")
    
#----------------------------------------------------------------------------------------------------
    # Appending the user's question to chat_history
#----------------------------------------------------------------------------------------------------
    
    chat_history.append({"role": "user", "content": question})
    
#----------------------------------------------------------------------------------------------------
    # Feeding the chat_history into the model
#----------------------------------------------------------------------------------------------------
    
    output = model.create_chat_completion(chat_history)
    
#----------------------------------------------------------------------------------------------------
    # Removing unwanted stuff from the response
#----------------------------------------------------------------------------------------------------
    
    response = output['choices'][0]['message']['content']
    
#----------------------------------------------------------------------------------------------------
    # Removing * because python doesn't bold words based on these asterisks
#----------------------------------------------------------------------------------------------------
    
    response = response.replace("*", "")

#----------------------------------------------------------------------------------------------------
    # Checking for html: in response to trigger web search feature
#----------------------------------------------------------------------------------------------------
    
    if "html: " in response:
    
        print(response)
    
        time.sleep(4)
        
#----------------------------------------------------------------------------------------------------
        # Cleaning the response to only get the thing the AI wants to search
#----------------------------------------------------------------------------------------------------   
        response = response.replace("html: ", "")
    
        response = response.replace("\n", "")
        
#----------------------------------------------------------------------------------------------------
        # Using requests to search the response on duckduckgo by setting the query to the cleaned response
#----------------------------------------------------------------------------------------------------

        search = requests.get("https://duckduckgo.com/q=" + response)
    
        html = search.text
    
        soup = BeautifulSoup(html, 'html')
    
        print(soup)
    
        paragraph = soup.find_all('p')
    
        print(paragraph)  
    
    print("\n")
#----------------------------------------------------------------------------------------------------
    # Printing AI response
#----------------------------------------------------------------------------------------------------

    print("AI: " + response)

#----------------------------------------------------------------------------------------------------
    # Checking if TTS is enabled and which model is being used
#----------------------------------------------------------------------------------------------------
    if speech == True and tts_model == "pyttsx3":
#----------------------------------------------------------------------------------------------------
        # Trying to remove emojis using multiple ways
#----------------------------------------------------------------------------------------------------
        for word in response:
            sentence.append(word)
        if "😊" in sentence:
            sentence.remove("😊")
        for word in sentence:
            if word != "😊" or "😊" not in word:
                engine.say(word)
                engine.runAndWait()
            else:
                continue

#----------------------------------------------------------------------------------------------------
    # Appending the AI's response to chat_history
#----------------------------------------------------------------------------------------------------
    chat_history.append({"role": "assistant", "content": response})

