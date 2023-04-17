import openai
import os

def get_blog_post_chunks_and_customer_success_quotes_from_da_vinci(openai_api_key, transcript, messages):

    openai.api_key = openai_api_key

    # verbatim_prompt
    verbatim_prompt = r"""
    Please rewrite this portion of a transcript. Be sure to keep as much of the original sentences, turns of phrase, examples, and sentence structure as possible.

    portion of a transcript:
    """

    verbatim_prompt_long = r"""
    Please rewrite this portion of an interview transcript into a section of a blog post, with headings. Be sure to keep as much of the original sentences, turns of phrase, examples, and sentence structure as possible. Do not summarize. Do not repeat yourself. Do not omit details.

    For example:

    input:
    '''
    Yiren Lu
    Can you tell me about your transition from engineering to product?

    Emily Zhao
    People, whereas the engineering to product transition is not super uncommon. And it's definitely something that a lot of engineers will think about.  And so I think that topic generally appeals to a broader audience.  But my case is a little bit unique because I had had that product experience already when I was evaluating the transition from engineering into product.  So, at the time, I think this was is 2015.  No, sorry, this was 2018.  And I had been an engineer at Airbnb for a few years.  I was an Android engineer specifically.  And that's kind of interesting because as an Android engineer, you can either be like a framework specialist, like very technical, and much more of a specialist really going deep in that domain, or you can be a product generalist.  So you just build lots of features and you think about what features would be really great, or you can go and become a manager.  Those are basically the career paths available as an Android engineer.  And I was very much in the product domain, probably because of my experience in product.  But it's a very tricky space to be because it is hard to be so good at that, that people keep promoting you versus someone who just really knows Kotlin or really knows some of these open source frameworks and things like that. 
    '''

    output:
    '''
    Motivation to transition into product from engineering

    In 2015, I had already been an Android engineer at Airbnb for a few years. As an Android engineer, you can either be a framework specialist - someone very technical, or you can be a product generalist. As a product generalist, you just lots of features and you think about what features would be great. Those were basically the career paths available as an Android engineer. And I was very much in the product domain, probably because of my experience in product. But it was a very tricky space to be so good that people would keep promoting you, vs. someone who just really knows Kotlin.
    '''

    input:
    """


    # define the prompt
    write_outline_prompt = r"""
    Please rewrite this portion of a transcript. Each question should be turned into a subheading. Please rewrite each answer as complete, grammatical, concise sentences. Do not summarize. Do not repeat yourself. Do not omit details.

    For example, this is one portion of the transcript:

    '''
    Speaker 1 (03:24):
    Um, with kind of like all these different siloed systems, what some of the challenges were that you were running up against. Um, and then, you know, if it makes sense, how, how the, the Omniconnect is going to, uh, resolve a lot of those.

    Speaker 2 (03:37):
    Yeah, sure. Um, so we did in the past pick sort of a best in breed solution, um, for, for different areas. And the challenge with that is how we integrate them. Um, how do we build customer journeys that are frictionless, um, when we've got sort of a patchwork of systems in place? Um, I think that's what we're looking to change. You know, going to the Microsoft platform as a platform solution that is connected, um, that you know, we spend, we've spent a lot of our time working on integrations in the past, which you know, in, in a, a lot of these scenarios we won't have to do that in the future. They're interconnected, it's an interconnected solution.
    '''

    This is how it should be rewritten:

    '''
    What were some of the challenges you were running up against? How is omniconnect going to resolve them?

    In the past, we did pick a best-in-breed solution for different areas. The challenge with that was how to integrate them. How do we build customer journeys that are frictionless when we've got a patchwork of systems in place? That's what we are looking to change. In  the past, we've spenr a lot of our time working on integrations. In the future, with Microsoft's platform, we won't have to do that because it's an interconnected solution.
    '''

    Now please rewrite this portion of a transcript:
    """

    # ren interview prompt
    interview_prompt = r"""
    Please rewrite this portion of a transcript. Each question should be turned into a subheading. Please rewrite each answer as complete, grammatical, concise sentences. Do not summarize. Do not repeat yourself. Do not omit details.

    For example, this is one portion of the transcript:

    '''
    Speaker 1
    gonna ask you next because like, how did you have a good sense of what was the appropriate price for you to say yes to or like, how did you even negotiate in a situation like this? Yeah,

    Speaker 2
    you really, you just have to figure out like, how much does this company value at? Like, what are they like comparing it to? And so for envoy, they really cared about acquiring our team, first and foremost, and then they're happy about acquiring customers, but it was really like very much like the team that they most cared about. But it's not like a what we did was considered more of a strategic acquisition rather than an aqua hire. An Aqua hire would be more like, like a company in a dip totally different space, acquire as a team. And then there's like, no customers, no revenue, that kind of thing. So that would just be like a pure Aqua hire. So we were like a strategic acquisition, but like, we like we weren't big enough to be like a merger. Like it would not make sense for them to incorporate and take our entity into ours because it'd be so much paperwork. So instead, what it looks like is like it's like okay, you get a they basically buy the right to hire our entire team from the investors. And so that's like the due consideration. And so then that was a combination of equity and cash and then separate from what the investors get the the team got a really good offers. And then on top of those offers, they got retention bonuses. So this is how companies are allowed to give you out of band compensation offers, because our offers are in band for our levels, but then we get an additional chunk of money and equity on top of that, that separate as part of the acquisition. So that's how they're able to bring in highly compensated individuals, even though there's still like fit into the existing leveling system. Makes sense? And then
    '''

    This is how it should be rewritten:
    
    '''
    How did you get a sense of what a good price was? How did you even negotiate in a situation like this?

    You really just have to figure out how much does this company value you at? What are they comparing you to? And so for Envoy, they really cared about acquiring our team, first and foremost. They were happy about acquiring customers, but it was really the team that they most cared about. Although what we did was considered more of a strategic acquisition rather than an aqui-hire. An acqui-hire would be more like a company in a totally different space, acquired as a team. There's no customers, no revenue. 
    
    We were a strategic acquisition, but we weren't big enough to be a merger. It would not make sense for them to incorporate and take our entity into theirs because it'd be so much paperwork. So instead, what it looked like was that they bought the right to hire our team from our investors. So that was the due consideration to the investors, in a combination of equity and cash. Then separate from what the investors got, the team got really good offers. And then on top of those offers, they got retention bonuses. This is how companies are allowed to give you out of band compensation offers: our offers were in band for our levels, but then we got an additional chunk of money and equity on top of that as part of the acquisition.
    '''

    Now please rewrite this portion of a transcript:

    """

    # define alternative prompt
    clean_prompt = r"""
    Please edit this transcript for clarity. Do not summarize. Do not omit details. Do not make stuff up.
    """

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.1,
    messages=messages
    )

    print("completion", completion)


    return completion.choices[0].message["content"]