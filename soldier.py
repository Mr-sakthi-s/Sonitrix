import os
import speech_recognition as sr
import pyttsx3
from groq import Groq
from dotenv import load_dotenv

# 1. Load variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def speak(text):
    """Initializes a fresh engine instance to avoid driver conflicts."""
    print(f"Assistant: {text}")
    
    # Use 'sapi5' for Windows; use 'espeak' or leave empty for Linux/Mac
    try:
        engine = pyttsx3.init('sapi5') 
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except:
        # Fallback for non-windows systems
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

def free_voice_assistant():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Adjust for ambient noise to make silence detection more accurate
    # dynamic_energy_threshold helps in different room environments
    recognizer.dynamic_energy_threshold = True 
    
    with sr.Microphone() as source:
        print("\n[Adjusting for background noise...]")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[Listening... Speak now. The AI will stop when you stop talking.]")
        
        try:
            # listen() will automatically detect the end of a phrase based on silence
            audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            print("[Recording stopped, processing...]")
        except Exception as e:
            print(f"Listening error: {e}")
            return

    # Save the captured audio to a temporary WAV file
    with open("temp_input.wav", "wb") as f:
        f.write(audio_data.get_wav_data())

    try:
        # STT (Groq Whisper)
        print("Transcribing...")
        with open("temp_input.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("temp_input.wav", file.read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            )
        
        if not transcription.strip():
            print("Did not hear anything.")
            return

        print(f"You said: {transcription}")

        # LLM (Groq Llama)
        print("Thinking...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content":
                "You are a trained surveillance soldier reporting to your commanding officer. "
                "Speak naturally like a real field soldier. "
                "Be respectful, calm, and direct. "
                "Keep responses short and tactical. "
                "No jokes. No casual talk. No explanations unless necessary. "
                "Report observations clearly and wait for further instructions."},
                {"role": "user", "content": transcription}
            ],
            model="llama-3.3-70b-versatile",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # TTS output
        speak(response_text)

    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    print("--- Voice Assistant Ready ---")
    while True:
        input("Press Enter to start talking...")
        free_voice_assistant()