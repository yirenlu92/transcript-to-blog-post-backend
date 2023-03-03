from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import get_clean_transcript, split_on_fourth_appearance
from da_vinci import get_blog_post_chunks_and_customer_success_quotes_from_da_vinci
import os
from dotenv import load_dotenv


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

    # get interviewee name from requests
    interviewee_name = request.form['interviewee_name']

    # get interviewee background
    interviewee_background = request.form['interviewee_background']

    whole_blog_post = []

    initial_prompt = """
    I would like you to take an interview transcript where Yiren Lu is interviewing {} on her experience transitioning from software engineering to product management, and rewrite it in complete, grammatical, idiomatic American English sentences in the style of a blog post.

    Some addition context about {}'s professional background:

    {}

    The blog post should be written in the first person, from {}'s perspective, and retain as much of the original sentences and details from the transcript as possible. It should not say things like "Yiren Lu asked me...". You might have re-organize the text so that the chronology makes sense.
    
    Since the transcript is too long to fix in your context window, we will split it up and give it to you in chunks. Please output the corresponding section of the blog post for each input transcript portion we give you. The section should be given a subheading that corresponds to the question that Yiren Lu asked.
    """

    messages=[
        {"role": "system", "content": "You are a journalist transcribing using an interview to write a blog post."},
        {"role": "user", "content": initial_prompt.format(interviewee_name, interviewee_name, interviewee_background, interviewee_name)},
    ]

    # split the transcript into sections
    sections = split_on_fourth_appearance(transcript, interviewee_name)

    # add a progress bar

    try:
        for section in sections:
            print(section)
            messages_copy = messages.copy()
            messages_copy.append({"role": "user", "content": "Here is a chunk of the transcript:\n\n{}".format(section)})

            blog_post_chunk = get_blog_post_chunks_and_customer_success_quotes_from_da_vinci(openai_api_key,section, messages_copy)

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
