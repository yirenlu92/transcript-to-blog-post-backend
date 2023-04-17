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

    print(transcript)

    print("after parsing the transcript")

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

    initial_prompt_with_points = """

    Please edit the portion of an interview transcript below for clarity. If there are points listed below, make sure to hit the points listed (but not only the points below). 
    
    The edit should retain as many of the original sentences and details from the transcript as possible and be in question and answer form. Do not summarize. Do not make stuff up. Do not omit stuff.

    Points:
    {}

    Transcript:
    {}

    """

    initial_prompt_without_points = """

    Please edit the portion of an interview transcript below for clarity. If there are points listed below, make sure to hit the points listed (but not only the points below). 
    
    The edit should retain as many of the original sentences and details from the transcript as possible and be in question and answer form. Do not summarize. Do not make stuff up. Do not omit stuff.

    Transcript:
    {}

    """

    messages=[
        {"role": "system", "content": "You are an editor, editing a Q&A for clarity."}
    ]

    # How to extract each chunk of text between the delimiters "#QBEGIN " and "#QEND"?
    # Regular expression pattern to match the delimiters and extract the text in between
    pattern = r'#QBEGIN([\s\S]*?)#QEND'

    # Find all the matches in the text
    matches = re.findall(pattern, transcript, re.DOTALL)

    print("length of matches")
    print(len(matches))


    try:
        for match in matches:

            # extract the text in each section inside #PBEGIN and #PEND
            points_pattern = r'#PBEGIN (.*?) #PEND'

            # Find all the matches in the text
            points = re.findall(points_pattern, match, re.DOTALL)

            # check if points is only empty strings or if points is empty
            if all(not point.strip() for point in points) or len(points) == 0:
                # dont include points in prompt
                total_prompt = initial_prompt_without_points.format(match)
            

            # include points in prompt
            points = "\n".join(points)
            total_prompt = initial_prompt_with_points.format(points, match)
        

            messages_copy = messages.copy()
            messages_copy.append({"role": "user", "content": total_prompt})

            blog_post_chunk = get_blog_post_chunks_and_customer_success_quotes_from_da_vinci(openai_api_key, match, messages_copy)

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
