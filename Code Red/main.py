import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from visio_audio.speech_module import process_audio

print("VISIO Audio Test Started...")

while True:
    text, intent = process_audio(3)

    if text:
        print("Speech:", text)
        print("Intent:", intent)
        print("------")
