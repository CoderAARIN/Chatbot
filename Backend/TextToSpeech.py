import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

# Asynchronous function to save text to audio
async def TextToAudioFile(text):
    file_path = r"Data\speech.mp3"

    if os.path.exists(file_path):
        os.remove(file_path)

    # Create the communicate object for text-to-speech conversion
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')

    # Save the speech to a file asynchronously
    await communicate.save(r'Data\speech.mp3')


# Function to play the audio using pygame
def PlayAudio():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    except Exception as e:
        print(f"Error in playing audio: {e}")


# Main TTS function to combine text-to-speech and audio playback
async def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Run the async function to convert text to speech
            await TextToAudioFile(Text)

            # Play the audio after saving the speech file
            PlayAudio()

            return True
        except Exception as e:
            print(f"Error in TTS: {e}")
        finally:
            try:
                func(False)
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")


# Function to break text into manageable parts for TTS
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(Data) > 4 and len(Text) > 250:
        asyncio.run(TTS("".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func))
    else:
        asyncio.run(TTS(Text, func))


if __name__ == "__main__":
    while True:
        text = input("Enter your text: ")
        TTS(text)  # Run TextToSpeech function asynchronously