import json
import os
from retrying import retry
import openai

from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI()

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=100, wait_exponential_max=1000)
def get_chat_completion(prompt, temperature=0.7, top_p=1):
  response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=[
        {'role': 'user',
        'content': prompt}
      ],
      temperature=temperature,
      top_p=top_p,
  )
  message = response.choices[0].message
  print(message)
  return message.content


@retry(stop_max_attempt_number=3, wait_exponential_multiplier=100, wait_exponential_max=1000)
def get_chat_completion_with_image(prompt, b64_json, temperature=0.7, top_p=1):
  response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          'role': 'user',
          'content': [ prompt, {"image": b64_json, "resize": 768} ] 
        }
      ],
      temperature=temperature,
      top_p=top_p,
  )
  message = response.choices[0].message
  print(message)
  return message.content
  

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=100, wait_exponential_max=1000)
def generate_images(prompt, n=1, response_format="url", quality="hd", size="1024x1024", style="vivid"):
  response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    response_format=response_format,
    n=n,
    quality=quality,
    size=size,
    style=style,
  )
  return response


def postable_text(text, max_length=320):
  puncts = ['.', ',', ';', '--']
  posts = []

  while len(text) >= max_length:
    cut_where, cut_why = max((text.rfind(punc, 0, max_length), punc) for punc in puncts)
    if cut_where <= 0:
      cut_where = text.rfind(' ', 0, max_length)
      cut_why = ' '
    cut_where += len(cut_why)
    posts.append(text[:cut_where].rstrip() + '...')
    text = text[cut_where:].lstrip()
  posts.append(text)
  return posts
