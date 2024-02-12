import os
import speech_recognition as sr
import streamlit as st
import google.generativeai as ai

os.environ['GOOGLE_API_KEY'] = "AIzaSyBsf1Cq_V6zrb9LHgb-AiCN_luZi3zBYk0"
ai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = ai.GenerativeModel('gemini-pro')

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source, timeout=5)
        try:
            recognized_text = recognizer.recognize_google(audio_data)
            st.write(f"Recognized text: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            st.warning("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
    
    return ""

def main():
    st.title("Speech Recognition with Streamlit")
# Use st.session_state to persist session-specific state
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

    with st.expander("Speech Recognition"):
        st.title("Welcome to Shaili's GPT")
        st.info("Click the button and start speaking!")

        if st.button("Start Recording", key=1):
            st.session_state.recognized_text = recognize_speech()
            st.text_area("Enter your question", st.session_state.recognized_text)

    if st.button("Ask Shaili") and st.session_state.recognized_text:
        response = model.generate_content(st.session_state.recognized_text)
        st.success(response.text)

if __name__ == "__main__":
    main()