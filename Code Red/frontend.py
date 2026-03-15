import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import streamlit as st

from visio_audio.stt import speech_to_text
from visio_audio.intent import detect_intent
from visio_audio.alarm import trigger_alarm


st.set_page_config(
    page_title="CODE RED AI SYSTEM",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 CODE RED AI Control Panel")

st.write("Voice Controlled Security System")


if st.button("🎤 Start Listening"):

    with st.spinner("Listening..."):

        text = speech_to_text()

        intent = detect_intent(text)

    st.success(f"You said: {text}")
    st.info(f"Detected Intent: {intent}")

    if intent == "danger":

        trigger_alarm()

        st.error("🚨 THREAT DETECTED - ALARM TRIGGERED")