from revChatGPT.revChatGPT import Chatbot
import json
import os
from dotenv import load_dotenv


# define the prompt
write_outline_prompt = r"""Please edit this interview transcript into sections of a 1500-word technical blog post. The technical blog post should use as much detail from the transcript as possible. The sections should have subheadings and should cover:

"""
write_blog_post_prompt = "ok, can you now please write a couple sections of a technical blog post, following the outline below. Please include as much detail from the interview transcript as possible."
        

class ChatBot:

    def __init__(self):
        load_dotenv()
        self.config = {"Authorization": "{}".format(os.getenv("OPENAI_API_KEY"))}
        self.chatbot = Chatbot(self.config, None)
    
    def get_blog_post_chunks_from_chat_gpt(self,transcript):
        prompt = '{}\n\n"""\n{}\n"""'.format(write_outline_prompt,transcript)

        try:
            resp = self.chatbot.get_chat_response(prompt, output="text") # Sends a request to the API and returns the response by OpenAI
        except Exception as e:
            print(e)
            return "Error: {}".format(e)
        return resp['message'] # The message sent by the response

    def get_blog_post_from_outline(self, transcript, outline):
        prompt = '{}\n\n"""\n{}\n"""\n\n"""\n{}\n"""'.format(write_blog_post_prompt,outline, transcript)
        print(prompt)
        resp = self.chatbot.get_chat_response(prompt, output="text") # Sends a request to the API and returns the response by OpenAI\
        return resp['message'] # final blog post
