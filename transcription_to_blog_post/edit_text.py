import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.Edit.create(
  model="text-davinci-edit-001",
  input=r"""number one is the obvious one to me which is not reusing code. There's an idea of - i'm going to work in a notebook. data scientists love notebooks right it becomes super iterative you can go really fast. you're building features a lot of times in like pandas and python so you're writing code in a slightly abstracted language but you're often operating on a sample of data in that notebook and you'll make a couple of quick features you maybe throw them into like a correlation analysis see if they're related to your target.

that notebook was the handoff point we were seeing for a lot of these teams. They would say, oh i checked that notebook into git someone else can use it now -- and it's completely unrealistic because the next data scientist comes along and they can't get the context they need from what's in a notebook to actually trust and reuse those features. Even if they do want to reuse the features, the data is not there at all. The data was typically extracted from some other data lake or data warehouse into the notebook in the first place.

so doing something like you know refreshing your feature values became a whole process that wasn't answered for in the kind of development life cycle.

the second one emerged after we worked with a lot of users on kind of that those early prototypes it was around the idea of trust. it's the idea that even if I do have someone's code, even if I see the feature values and have access to them you know in a tool that i could reuse, why should i trust them? Data science is not inherently very collaborative, it\'s just an exercise that we often do by ourselves. So it was very foreign to our users that they might just use their colleagues features without ever talking to them about it.""",
  instruction="Rewrite this to summarize the main points."
)

print(response)


