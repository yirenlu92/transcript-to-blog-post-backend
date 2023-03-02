import os
import openai
from dotenv import load_dotenv

text = '''
Chris (00:29):
All right. Uh, again, like I said, this'll probably be very similar to the conversation that we already had. Um, so in that spirit, if we could just start out by having you introduce yourself, name, title, and then just talk a little bit about what you do at Northern.
Dennis Rouland (00:44):
Sure. Uh, Dennis Rouland, I'm a senior director and business program leader right now. Um, I'm actually leading our Omniconnect program, which is an omnichannel, um, sort of, uh, omnichannel reimagination, I guess, at Northern Tool. Um, and, and digital transformation in omnichannel. I've been in an IT role in past, so I le- led different parts of IT for a little over six years at Northern Tool.
Chris (01:12):
Awesome. So let's, like, let's dive into, is Omnicorrect- Connect the right terminology?
Dennis Rouland (01:18):
That's our, that's our program name.
Crew (01:19):
One sec, I'm just gonna make a slight adjustment before you get too far into it.
Dennis Rouland (01:23):
Sure.
Crew (01:23):
And you're good, right about there.
Dennis Rouland (01:30):
That's the brand we've given it, Chris. So that's our program name for kind of our omnichannel, um, transformation that we're going through.
Chris (01:38):
So can you talk to me a little bit just big picture on where you're at, where you're headed, and why?
Dennis Rouland (01:45):
Yeah. So, so this transformation is, in a lot of ways it's a life cycle change for us. So we have some very old systems that we're running our business on, especially in order management. Um, this change is really to enable us as a modern retailer. Um, so we've done, we've done our best, I would say, um, to kind of, um, limp along. Limp along is the wrong word, but to, um, to build the capabilities we could with the tool set we had. Um, so this is really to get us to a future modern platform. Um, the Microsoft platform that's an evergreen platform, um, and something that we can grow in. Um, so yeah, we're really excited about it.
'''

def find_occurrences_of_interviewee(lst, word):
    return [i for i, x in enumerate(lst) if word in x]

def find_occurrences_of_speakers(lines, word, word2):
    # find all lines that contain a timestamp like 00:29
    return [i for i, x in enumerate(lines) if word in x or word2 in x]

def split_on_fourth_appearance(text, interviewee_name):
    lines = text.split('\n')
    split_lines = []
    split_index = 0
    count = 1
    interviewee_lines_indices = find_occurrences_of_interviewee(lines, interviewee_name)
    speaker_lines_indices = find_occurrences_of_speakers(lines, interviewee_name, "Yiren")
    print(speaker_lines_indices)
    # split lines into chunks of 1 interviewee responses
    while split_index < len(lines) and count + 2 < len(interviewee_lines_indices):
        # smallest index in speaker_lines_indices that is greater than interviewee_lines_indices[count]
        split_index_end = min([i for i in speaker_lines_indices if i > interviewee_lines_indices[count]])
        chunk = lines[split_index:split_index_end]
        split_lines.append('\n'.join(chunk))
        count += 1
        split_index = split_index_end

    
    # for line in lines:
    #     if speaker_name in line:
    #         count += 1
    #         if count % 5 == 0:
    #             split_lines.append('\n'.join(lines[split_index: lines.index(line) + 2]))
    #             split_index = lines.index(line) + 2
    split_lines.append('\n'.join(lines[split_index:]))
    return split_lines


def get_clean_transcript(video_id, transcript):

    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # delete file if it already exists
    if os.path.exists("blog_post_{}.txt".format(video_id)):
        os.remove("blog_post_{}.txt".format(video_id))

    # define the prompt
    instruct_prompt = "Rewrite the following text in complete, grammatical sentences:"

    clean_transcript = []

    with open("blog_post_{}.txt".format(video_id), "a") as f:

        # put them into gpt3 200 lines at a time
        for i in range(0, len(transcript), 200):

            # get the next 75 lines
            lines = transcript[i:i+75]
            # join them into a string
            lines = "".join(lines)

            # put the transcript and the prompt together
            prompt = r'{}\n\n"""\n{}\n"""'.format(instruct_prompt, lines)

            # put them into gpt3
            response = openai.Completion.create(
            model="text-curie-001",
            prompt=prompt,
            temperature=0.12,
            max_tokens=718,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            )

            clean_transcript.append(response.choices[0].text)
            
            # write the response to file
            f.write("{}\n".format(response.choices[0].text.strip()))

        return "\n".join(clean_transcript)

# def get_clean_transcript_assembly_ai(video_id, transcript):

#     load_dotenv()

#     # delete file if it already exists
#     if os.path.exists("blog_post_{}.txt".format(video_id)):
#         os.remove("blog_post_{}.txt".format(video_id))

#     # define the prompt
#     instruct_prompt = "Rewrite the following text in complete, grammatical sentences:"

#     clean_transcript = []

#     with open("blog_post_{}.txt".format(video_id), "a") as f:

#         import request

# endpoint = 'https://api.assembly.com/v2/transcript/{TRANSCRIPT ID}/paragraphs'

# headers = {'authorization': 'YOUR ASSEMBLYAI API TOKEN'}

# response = requests.get(endpoint, headers=headers)

# print(response.json())