#/usr/bin/python3
from PyPDF2 import PdfReader
from contextlib import redirect_stderr, redirect_stdout
from llama_cpp import Llama
import time
import requests
from bs4 import BeautifulSoup
import os
import subprocess
user = subprocess.run("whoami", text=True, stdout=subprocess.PIPE).stdout.strip()
huge_number = "cd /home/" + user + "/.cache/huggingface/hub/models--bartowski--gemma-2-2b-it-GGUF/snapshots && ls"
hugenumber = subprocess.run(huge_number, text=True, shell=True, stdout=subprocess.PIPE).stdout.strip()
model_file = "cd /home/" + user + "/.cache/huggingface/hub/models--bartowski--gemma-2-2b-it-GGUF/snapshots/" + hugenumber + "&& ls"
modelfile = subprocess.run(model_file, text=True, shell=True, stdout=subprocess.PIPE).stdout.strip().split("\n")
if any("Q8" in f for f in modelfile):
    chosen_file = "gemma-2-2b-it-Q8_0.gguf"
else:
    chosen_file = "gemma-2-2b-it-Q4_K_M.gguf"
modelpath = "/home/" + user + "/.cache/huggingface/hub/models--bartowski--gemma-2-2b-it-GGUF/snapshots/" + hugenumber + "/" + chosen_file
try:
    trashfile = "cat /home/" + user + "/.trash.txt"
    subprocess.run(trashfile, text=True, shell=True, stdout=subprocess.PIPE).stdout.strip()
except FileNotFoundError:
    creatrash = "cd /home/" + user + " && touch .trash.txt"
    subprocess.run(creatrash, text=True, shell=True, stdout=subprocess.PIPE).stdout.strip()
trashdir = ("/home/" + user + "/.trash.txt")
with open(trashdir, "w") as trash:
    with redirect_stderr(trash), redirect_stdout(trash):
        model = Llama(model_path=modelpath, verbose=False, n_ctx=32000)
default_prompt = "You are a friendly tutor for a class 6 student. Explain answers to the student in simple words. Your name is gemma. Dont introduce yourself unless you are asked to. Never ever make responses above 200 tokens even when asked to!. talk to the student as if you were friends. End responses with questions that the student may have. When you are quizzing the student, check if the students answers are correct and if it isn't correct, explain to them why it isn't. If you want to search something from the web, reply with the word html followed by the thing you want to search, this response should only contain the word html and the thing you want to search"
speech = False
tts_model = ""  
sentence = []
chat_history = [
{"role": "user", "content": default_prompt},
{"role": "assistant", "content": "Ok, understood"}
]
while True:
    question = input("You: ")
    if question.lower() == "clear":
        os.system("clear")
        question = input("You: ")
    elif question.lower() == "exit":
        exit()
    elif question.lower() == "quiz":
        time.sleep(1)
        print("Switching to Quiz Mode")
        time.sleep(2)
        print("Current mode: Quiz")
        time.sleep(1)
        print("Current Subject: BS ( Basic Science ) ")
        time.sleep(1)
        pagen = input("Enter a page to ask questions from (7 - 94): ")
        int(pagen)
        while not pagen.isdigit() or int(pagen) > 94 or int(pagen) < 7:
            pagen = input("Please enter a valid page number(7 - 96): ")
            int(pagen)
        reader = PdfReader("Science.pdf")
        page = reader.pages[int(pagen) - 1]
        text = page.extract_text()
        page1 = reader.pages[int(pagen) - 2]
        text1 = page.extract_text()
        page2 = reader.pages[int(pagen)]
        pagen1 = pagen + 1
        pagen2 = pagen - 1
        chat_history.append({"role": "user", "content": "This is an automated System Response: The user has switched to Quiz mode. The subject is Basic Science. The page number to ask questions from is " + pagen + ". Keep asking questions one by one until the user exits quiz mode. Here are all the text in page number" + pagen + ": \n" + text + "For clarity/ better referencing when asking questions, here are the text from the previous page(" + str(pagen2) + " too:\n " + text1 + "Heres the text from the next page(" + str(pagen1) + ") too: \n" + text2} )
        output = model.create_chat_completion(chat_history)
        response = output['choices'][0]['message']['content']
        response = response.replace("*", "")
        chat_history.append({"role": "assistant", "content": response})         
        print("AI: " + response) 
    elif question.lower() == "configure":
        question = None
        name = input("Name: ")
        tname = input("Tutor Name: ")
        print("Teaching style: ")
        print("[1] Short and quick answers")
        print("[2] Detailed and long answers")
        style = input("Choose a teaching style (1 or 2): ")
        if style == "1":
            style = "Respond to the student's questions with short and quick answers."
        elif style == "2":
            style = "Respond to the student's questions with long and detailed answers."
        else:
            print("Invalid Teaching Style")
            time.sleep(1)
            print("Setting teaching style to default: Short and quick answers")
            style = "Respond to the student's questions with short and quick answers"
        print("Quiz difficulty: ")
        print("[1] Easy")
        print("[2] Medium")
        print("[3] Hard")
        difficulty = input("Choose Quiz difficulty (1,2 or 3): ")
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
        print("Tone: ")
        print("[1] Professional")
        print("[2] Fun and Silly")
        tone = input("Choose a Tone (1 or 2): ")
        tone.strip()
        if tone == "1":   
            tone = "Answer the students question in a professional way"
        elif tone == "2":
            tone = "Answer the students question in a fun and silly way"
        else:
            print("Invalid Tone")
            time.sleep(1)
            print("Setting tone to default tone: Professional")
            tone = "Answer the students question in a professional way"
        print("Response type: ")
        print("[1] Text only")
        print("[2] Voice only")
        print("[3] Text & Voice")
        output = input(" Choose a response type(1,2 or 3): ")
        if output == "2" or "3":
            print("Choose a TTS model for speech: ")
            print("[1] pyttsx3: Robotic Voice")
            print("[2] Dia-1.6B: Realistic Human-like Voice")
            tts = input("Choose a model(1 or 2): ")
            if tts == "2":
                print("Warning!: Dia-1.6B consumes lots of hardware and can result in a bad experience.")
                print("Note: Using Dia-1.6B requires it to be installed.")
                confirm = input("Are you sure (y/n): ")
                if confirm == "y":
                    speech = True
                    tts_model = "Dia-1.6B"
                    emoji = "Never use emojis in responses"
                elif confirm == "n":
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
                        emoji = "Never use emojis in responses"
            elif tts == "1":
                speech = True
                tts_model = "pyttsx3"
                emoji = "Never ever use emojis in responses"
            elif output == "1":
                speech = False
                emoji = "Use emojis in responses"
        prompt = "This is an automated System Response: You are a friendly tutor for a class 6 student." + style + ". Your name is " + tname + ". The student's name is " + name + ". Don't introduce yourself unless you are asked to. Talk to the student as if you were best friends." + tone + "." + emoji + ". End responses with questions that the student may have. When you are quizzing the student, check if the students answers are correct and if it isn't correct, explain to them why it isn't." + difficulty
        chat_history[0]['content'] = prompt
    elif question == "":
        while question == "":
            print("Invalid input: No text found")
            question = input("You:")
    else:

        chat_history.append({"role": "user", "content": question})
        output = model.create_chat_completion(chat_history)
        response = output['choices'][0]['message']['content']
        response = response.replace("*", "")
        if "html: " in response:
            time.sleep(4)
            response = response.replace("html: ", "")
            response = response.replace("\n", "")
            search = requests.get("https://duckduckgo.com/q=" + response)
            html = search.text
            print(soup)
            paragraph = soup.find_all('p')
            print(paragraph)  
        print("\n")
        print("AI: " + response)
        chat_history.append({"role": "assistant", "content": response})

