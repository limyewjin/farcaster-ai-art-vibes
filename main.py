from datetime import datetime
import os
from farcaster import Warpcast
import imgbbpy
from dotenv import load_dotenv
from io import BytesIO
import base64
import requests

import openai_api

def UrlToBytes(url):
  response = requests.get(url)
  return BytesIO(response.content)


load_dotenv()

warpcast_client = Warpcast(mnemonic=os.environ.get("FARCASTER_MNEMONIC"))
print(f"Warpcast client healthcheck: {warpcast_client.get_healthcheck()}")

imgbbpy_client = imgbbpy.SyncClient(os.environ.get("IMGBB_API_KEY"))

date = (datetime.now().strftime("%a %b %-d, %Y"))
prompt = f'Today is {date}. Provide a short image prompt for a good morning post which we will send to DALL-E to generate. Do not generate people in these images.'
print(prompt)
completion = openai_api.get_chat_completion(prompt, temperature=0.7).strip()
print("OpenAI completion: '%s'" % completion)

image = openai_api.generate_images(completion).data[0]
image_prompt = prompt
if image.revised_prompt: image_prompt = image.revised_prompt
b = UrlToBytes(image.url)
b.seek(0)
b64_json = base64.b64encode(b.getvalue()).decode()

post = openai_api.get_chat_completion_with_image(f"Today is {date}. The image prompt sent to DALL-E is '{image_prompt}'. Write a post of length at most 320 bytes to accompany this image.", b64_json)
print(f"Image URL: {image.url}")
print(f"Post: {post}")

imgbb_image = imgbbpy_client.upload(url=image.url)
print(imgbb_image)

response = warpcast_client.post_cast(text=post, embeds=[imgbb_image.url])
print(response)
