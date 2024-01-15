import streamlit as st
from flask import Flask, render_template
from bardapi import BardCookies
import streamlit as st
from streamlit_chat import message
import speech_recognition as sr  # Added for speech recognition
import base64
from PIL import Image
import io
import webbrowser
import pyperclip

app = Flask(__name__)

@app.route("/open_html")
def open_html():
    return render_template("your_html_file.html")  # Replace with your HTML file name


#import easyocr

#arrancalo en terminal con: streamlit run main.py

cookie_dict = {
	"__Secure-1PSID": "fAhmjSQ7yRkfk3UvtOW-J9apSalcBRrP4imTtJGm1uOKhGKYdKrM4ZuHZz5o4Iy58uQPOQ.",
	"__Secure-1PSIDTS": "sidts-CjEBPVxjSvg8-3Aoh5BTiW9bZmHYYp9KTeGyAAEcOTsyyjyS77xPU8LYa2XZbI6JZxbVEAA",
	"__Secure-1PSIDCC": "ABTWhQGMAMQm-ii9w7k93ASt8UzU1JGEAq8j7va-nh39wZrjlwAofQBJ90TrKAvGDxAa55AsLjLw"
}

bard = BardCookies(cookie_dict=cookie_dict)

# message = input("Introduce lo que necesites saber: ")

# print(bard.get_answer(str(message))['content'])

st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous>""")


st.title("CalculoIA tutor")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results from speech recognition service; {0}".format(e))
        return ""

def open_external_html(url):
    webbrowser.open_new_tab(url)

def image_input():
    #uploaded_image = st.file_uploader("Sube tu imagen", type=["jpg", "jpeg", "png"])
    #if uploaded_image is not None:
    #    image = Image.open(uploaded_image)
    #    return image
    return None

if 'generate' not in st.session_state:
    st.session_state['generate'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def response_api(promot):
    message = bard.get_answer(str(promot))['content']
    return message

def user_input():
    text_input = st.text_input("Introduce lo que necesitas saber: ")
    speech_input = st.button("Hablar")  # Button for speech input

    if speech_input:
        text_input = recognize_speech()

    return text_input

def audio_input():
    uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["mp3", "wav"])
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return audio_base64

        image = Image.open(uploaded_image)
        return image
    return None

if 'generate' not in st.session_state:
    st.session_state['generate']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]


if st.button("Open External HTML"):
    html_file_path = "../Pizarra_JS-main\index.html"  # Replace with the actual path
    open_external_html(html_file_path)

#if st.button("Open HTML in New Window"):
#    html_url = app.url_for("C:\Juan\escom\quinto\avanxadas\final\Pizarra_JS-main\index.html")  # Generate the internal URL
#    js = f"window.open('{html_url}', '_blank');"  # JavaScript to open in a new window
#    st.write(js, unsafe_allow_html=True)

#if st.button("Pizarra"):
#    html_file_path = "C:\Juan\escom\quinto\avanxadas\final\Pizarra_JS-main\index.html"
#    st.components.v1.iframe(html_file_path, width=1800, height=1000)

# Clipboard image
def get_text_and_image_input():
    text_input = st.text_area("Introduce lo que necesitas saber:")
    
    # Check if an image is uploaded
    uploaded_image_2 = st.file_uploader("Sube tu imagen", type=["jpg", "jpeg", "png"])
    if uploaded_image_2 is not None:
        image = Image.open(uploaded_image_2)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        return text_input, image
    
    # Check if an image is in the clipboard
    clipboard_data = pyperclip.paste()
    if clipboard_data.startswith("data:image"):
        image = Image.open(io.BytesIO(base64.b64decode(clipboard_data.split(',')[1])))
        st.image(image, caption='Pasted Image', use_column_width=True)
        return text_input, image
    
    return text_input, None


user_text = user_input()
user_audio = audio_input()
user_image = image_input()
text_and_image_input = get_text_and_image_input()


if user_text or user_audio or user_image or text_and_image_input:
    if user_audio:
        processed_audio_text = recognize_speech()
        output = response_api(processed_audio_text)
    elif user_image:
        # Process the image, for example, you can use a computer vision library like OpenCV
        # For simplicity, let's assume the image processing step is handled
        output = "Image processing result"
    elif text_and_image_input:
        # Process the image, for example, you can use a computer vision library like OpenCV
        # For simplicity, let's assume the image processing step is handled
        output = "Image processing result"
    else:
        output = response_api(user_text)

    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)

if user_text: # or user_audio:
    if user_audio:
        # Process audio, convert it to text or any other necessary step
        # For simplicity, let's assume the audio processing step is handled
        processed_audio_text = recognize_speech()
        output = response_api(processed_audio_text)
    else:
        output = response_api(user_text)
    
    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)

if st.session_state['generate']:
    for i in range(len(st.session_state['generate']) - 1, -1, -1):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generate"][i], key=str(i))