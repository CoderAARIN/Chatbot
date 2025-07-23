import asyncio
from random import randint
from PIL import Image
from dotenv import dotenv_values
import os
import requests
from time import sleep

# Get key function to load API key from .env
def get_key(env_file, key_name):
    return dotenv_values(env_file).get(key_name)

def open_image(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_files in Files:
        image_path = os.path.join(folder_path, jpg_files)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)

        except IOError:
            print(f"Unable to open {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_image(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)} ",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)

def GenerateImage(prompt: str):
    asyncio.run(generate_image(prompt))
    open_image(prompt)

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status.strip() == "True":
            print("Generating Image....")
            GenerateImage(prompt=Prompt.strip())

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")

        else:
            sleep(1)

    except Exception as e:
        print(e)
