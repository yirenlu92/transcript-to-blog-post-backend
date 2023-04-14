from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import get_clean_transcript, split_on_fourth_appearance
from da_vinci import get_blog_post_chunks_and_customer_success_quotes_from_da_vinci
import os
from dotenv import load_dotenv
import re


app = Flask(__name__)
CORS(app)

@app.route('/')
def health():
    return 'Hello Ren'

@app.route('/handle_youtube_video', methods=['POST'])
def handle_youtube_video():

    # Get the video URL from the request
    video_url = request.form['video_url']

    # parse out the video ID from the URL
    video_id = video_url.split('v=')[1]

    print(video_id)

    # call get_transcript.py with the video_id
    transcript = get_transcript(video_id)

    # call get_clean_transcript to get a clean transcript
    clean_transcript = get_clean_transcript(video_id, transcript)

    # Return a response
    return clean_transcript

@app.route('/handle_text_file', methods=['POST'])
def handle_text_file():

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")

    print("in the handle text file")

    # get transcript from requests 
    transcript = request.form['transcript']

    # get prompt from requests
    prompt = request.form['prompt']

    # get interviewee name from requests
    interviewee_name = request.form['interviewee_name']

    # get interviewee background
    interviewee_background = request.form['interviewee_background']

    whole_blog_post = []

    translation_prompt = """
        Please translate the following interview transcript into complete, grammatical, idiomatic American English sentences in the style of a professional translator. Do not omit details or change the meaning of the original text.
    """

    # initial_prompt = """
    # Please turn the following interview transcript into a 600-word customer success story that begins: "We spoke with(name and title at company) about their vision for how Azure OpenAI Service will transform XXX. This is that conversation as summarized by Azure OpenAI Service."

    # Stories should look and feel like they could live on the new Azure AI hub and support the messaging and value statements contained within.

    # The interview transcript is interviewing an educational provider in Taiwan that used Azure OpenAI Service for chatbot and speech assessment capabilities.

    # The interview transcript is in Chinese and is too long, so we will split it up and give it to you in chunks. Please output the corresponding section of the blog post for each input transcript portion we give you. The section should be given a subheading that corresponds to the question that Yiren Lu asked.
    # """

    initial_prompt = """

    Please edit the transcript of an interview question and answer below for clarity. If there are points listed below, make sure to hit the points listed below (but not only the points below). The output should be written in the first person, from {}'s perspective, and retain as much of the original sentences and details from the transcript as possible. Do not summarize. Do not make stuff up. Do not omit stuff.

    Points to hit: {}

    Transcript of interview question and answer: {}
    
    """

    messages=[
        {"role": "system", "content": "You are an editor, editing a Q&A for clarity."}
    ]

    # How to extract each chunk of text between the delimiters "#### Question {n} BEGIN" and "#### Question {n} END"?
    # Regular expression pattern to match the delimiters and extract the text in between
    pattern = r'#### Question \d+ BEGIN(.*?)#### Question \d+ END'

    # Find all the matches in the text
    matches = re.findall(pattern, transcript, re.DOTALL)


    try:
        for match in matches:

            section = match[1]
            # print the section
            print(section)
            print("-----")

            # extract the text in each section inside the square brackets
            parts_of_section = section.split("]")

            print(parts_of_section)

            points = ""
            transcript = ""
            if len(parts_of_section) > 1:
                points = parts_of_section[0]
                points = points.replace("[", "")
                if len(points) > 0:
                    points = points[1:]
                transcript = parts_of_section[1]
            else:
                transcript = parts_of_section[0]
            
            print(points)
            print(transcript)

            messages_copy = messages.copy()
            messages_copy.append({"role": "user", "content": initial_prompt.format(points, transcript)})

            blog_post_chunk = get_blog_post_chunks_and_customer_success_quotes_from_da_vinci(openai_api_key,section, messages_copy)

            print(blog_post_chunk)

            whole_blog_post.append(blog_post_chunk)

    except Exception as e:
        print(e)
        return "Error: {}".format(e)

    return "\n\n".join(whole_blog_post)

@app.route('/handle_outline', methods=['POST'])
def handle_outline():

    # Get the outline from the request
    outline = request.form['outline']

    blog_post = get_blog_post_from_outline(transcript, outline)

    # Return a response
    return blog_post

# if __name__ == '__main__':
#     app.run()
