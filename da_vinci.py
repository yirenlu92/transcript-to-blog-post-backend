import openai
import os

def get_blog_post_chunks_and_customer_success_quotes_from_da_vinci(openai_api_key, transcript, messages):

    openai.api_key = openai_api_key
    result = None
    tries = 0

    # retry the request if it fails
    while tries < 3:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0.2,
                messages=messages
            )
            result = completion.choices[0].message["content"]
            tries = 3
        except error as err:
            print(f"Error: {err}")
            tries += 1
            raise err

    return result