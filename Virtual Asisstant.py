import openai
import pyttsx3
import speech_recognition as sr
import time
import os 
from gtts import gTTS
# Melakukan Set API KEY 
openai.api_key = "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"
# inisialisasi engine transkrip teks ke kalimat pembicaraab
engine = pyttsx3.init()

def menerjemahkan_audio_ke_teks(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source2:
        audio = recognizer.record(source2)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Waktu habis silahkan ulangi lagi")

def mendapatkan_respon(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()      

def main():
    while True:
        # Menunggu user untuk memanggil 
        print("Katakan 'Wonder' untuk memulai pertanyaan")
        with sr.Microphone() as source2:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source2,phrase_time_limit = 5)
            recognizer.adjust_for_ambient_noise(source2, duration=0.2)
            try:
             transkripsi = recognizer.recognize_google(audio, language='id-ID')
             if transkripsi.lower() == "wonder":
                 filename =  "input.wav"
                       
                 print("Tanyakan pertanyaan mu ....")
                 with sr.Microphone()as source2:
                     recognizer = sr.Recognizer()
                     source2.pause_threshold = 1
                     audio = recognizer.listen(source2, phrase_time_limit = None, timeout = None) 
                     with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                    
                  #Transkrip audio ke teks 
                 text = menerjemahkan_audio_ke_teks(filename)
                 if text:
                  print(f"You said: {text}")    

                # Generate respon memakai GPT-3
                 response = mendapatkan_respon(text)
                 print(f"GPT-3 Mengatakan : {response}")

                # Transkrip ke indonesia 
                 tts = gTTS(text=response, lang="id")
                 tts.save("sample.mp3")

                # Membaca respon menggunakan text-to-speech library
                 speak_text(response)
            except  Exception as e:
                 print("Ada error yang tidak diketahui: {}".format(e))

if __name__ == "__main__":
    main()