# from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    # retrieve the available transcripts
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

    f = open("transcript_{}.txt".format(video_id), "w")

    text = []
    for sentence in transcript:
        text.append(sentence["text"])
        f.write("{}\n".format(sentence['text']))

    f.close()

    print(text)
    
    return text