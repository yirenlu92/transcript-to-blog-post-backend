from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import get_clean_transcript, split_on_fourth_appearance
from da_vinci import get_blog_post_chunks_and_customer_success_quotes_from_da_vinci
import os
from dotenv import load_dotenv
import re
from prompts import initial_prompt_with_points, initial_prompt_without_points
from utilities import create_default_prompt, create_user_defined_prompt


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

    # check if prompt is just empty string
    if prompt.strip() == "":
        prompt = initial_prompt_without_points


    whole_blog_post = []


    messages=[
        {"role": "system", "content": "You are an editor, editing an interview transcript."}
    ]

    # split the transcript into chunks based on the delimiter "##"
    matches = transcript.split("##")

    # # How to extract each chunk of text between the delimiters "#QBEGIN " and "#QEND"?
    # # Regular expression pattern to match the delimiters and extract the text in between
    # pattern = r'#QBEGIN([\s\S]*?)#QEND'

    # # Find all the matches in the text
    # matches = re.findall(pattern, transcript, re.DOTALL)

    print("length of matches")
    print(len(matches))


    try:
        for match in matches:

            total_prompt = ""

            # extract the text in each section inside #PBEGIN and #PEND
            points_pattern = r'#PBEGIN (.*?) #PEND'

            # Find all the matches in the text
            points = re.findall(points_pattern, match, re.DOTALL)

            # check if prompt is not empty
            if prompt.strip() != "":
                total_prompt = create_user_defined_prompt(points, match, prompt)
            else:
                total_prompt = create_default_prompt(points, match)
                
            messages_copy = messages.copy()
            messages_copy.append({"role": "user", "content": total_prompt})

            blog_post_chunk = ""
            try:
                blog_post_chunk = get_blog_post_chunks_and_customer_success_quotes_from_da_vinci(openai_api_key, match, messages_copy)
            except Exception as e:
                print(e)
                blog_post_chunk = "ERROR!!! There was an error processing this chunk of the transcript - please manually review: \n{}".format(match)

            whole_blog_post.append(blog_post_chunk)

    except Exception as e:
        print(e)
        return "Error: {}".format(e)
    
    print("length of whole blog post array:")
    print(len(whole_blog_post))

    return "\n\n".join(whole_blog_post)

@app.route('/handle_outline', methods=['POST'])
def handle_outline():

    # Get the outline from the request
    outline = request.form['outline']

    blog_post = get_blog_post_from_outline(transcript, outline)

    # Return a response
    return blog_post

if __name__ == '__main__':
    app.run(debug=True)
