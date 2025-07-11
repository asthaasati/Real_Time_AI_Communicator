import streamlit as st
from ai_engine import get_ai_response
from vosk_stt import record_audio, transcribe_audio
from tts_engine import speak

st.set_page_config(page_title="AI Voice Assistant", layout="centered")
st.title("🧠🎙️ AI Voice Assistant")

# Input mode toggle
input_mode = st.radio("Choose Input Mode:", ("🎤 Microphone", "📝 Text"), horizontal=True)

user_text = ""

if input_mode == "🎤 Microphone":
    if st.button("Start Recording"):
        with st.spinner("🎙️ Recording... Please speak"):
            record_audio()  # records to input.wav
            user_text = transcribe_audio("audio/input.wav")
            st.success("✅ Recording complete")
        st.markdown(f"**You (voice):** {user_text}")
else:
    user_text = st.text_area("Type your message here:", placeholder="Hello, how are you?")
    if st.button("Send") and user_text.strip() == "":
        st.warning("Please enter a message.")

# Only run if user provided input
if user_text:
    with st.spinner("🤖 Thinking..."):
        ai_reply = get_ai_response(user_text)

    if input_mode == "🎤 Microphone":
        st.markdown("**AI (voice):**")
        speak(ai_reply)  # generates output.mp3
        audio_file = open("audio/output.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
    else:
        st.markdown("**AI (text):** " + ai_reply)
