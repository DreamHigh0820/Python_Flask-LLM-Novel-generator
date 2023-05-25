import re
def jaccard_similarity(a, b):
    a_set = set(a.split())
    b_set = set(b.split())
    intersection = a_set.intersection(b_set)
    union = a_set.union(b_set)
    return len(intersection) / len(union)


def gap_agent(text:str):
    # Add gaps between parts of the story to improve flow
    parts = text.split(" [Part ")
    gap_text = ""
    for i in range(1, len(parts)):
        gap_text += f"\n\n{i}. " + parts[i]
    return gap_text.strip()


def refinement_agent(text):
    # Refine the text for better consistency and coherence
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=
        f"Refine the following text for better consistency and coherence:\n\n{text}\n\nRefined Text:",
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def editing_agent(text):
    # Edit the text for grammar, punctuation, and overall readability
    doc = nlp(text)
    edited_text = ""
    for sent in doc.sents:
        edited_sent = ""
        for token in sent:
            if token.is_punct:
                edited_sent += token.text
            else:
                edited_sent += " " + token.text
        edited_text += edited_sent.strip() + " "
    return edited_text.strip()


def formatText(text):
    text = text.replace('\\"', '"')
    text = text.replace('\n', ' ')
    text = text.replace('/', '')
    text = text.replace('\\', '')
    text = text.replace("<br>", "\n")  # Replace "<br>" with newline character
    text = text.replace("  ", " ")  # Replace double spaces with single spaces
    text = text.strip()  # Remove leading/trailing white space
    text = text.replace('."',
                        '".')  # Add space before period at end of sentence
    text = text.replace('. "',
                        '".')  # Remove space before period at end of sentence
    text = text.replace('.\n"', '.\n\n"')  # Add extra newline after paragraph
    text = text.replace('. "',
                        '". ')  # Add space after period at end of sentence
    text = text.replace('." ',
                        '". ')  # Add space after period at end of sentence
    text = re.sub(r'(\w)(\n\s*\w)', r'\1 \2',
                  text)  # Fix line breaks within words
    text = re.sub(r'([^\n"])(\n)([^\n"])', r'\1 \3',
                  text)  # Fix line breaks within sentences
    text = re.sub(r'([^\n"])(\n)(")', r'\1 \3',
                  text)  # Fix line breaks before opening quotation marks
    text = re.sub(r'(\w)(")(\n\s*\w)', r'\1\2 \3',
                  text)  # Fix line breaks after opening quotation marks
    text = re.sub(r'(\w)(")([^\n"]*")([^\n"]*\n\s*\w)', r'\1\2\3 \4',
                  text)  # Fix line breaks between quoted speech
    text = re.sub(r'(\w)(")([^\n"]*")([^\n"]*\n)', r'\1\2\3\4',
                  text)  # Fix line breaks at end of quoted speech
    text = re.sub(r'(\w)(")([^\n"]*")(\n)', r'\1\2\3\4',
                  text)  # Fix line breaks after quoted speech
    text = text.replace('"', '\"')
    return text.replace('"', '\"')

def iceberg_function(data):
    return (f"You are a {data['genre']} author. Your task is to use the Iceberg Method to create a rich and immersive world for your story. The Iceberg Method consists of two main layers:\n\n"
                f"1. Surface: This is what the reader sees and experiences directly. It includes things like physical description, dialogue, and action.\n"
                f"2. Depth: This layer includes everything beneath the surface: history, culture, politics, religion, and more. It's the foundation that supports the surface and gives your world depth and complexity.\n\n"
                f"Title: {data['title']}\n"
                f"Genre: {data['genre']}\n"
                f"Characters: {data['characters']}\n"
                f"Plot: {data['plot']}\n\n"
                f"{data['prompt']}")

def setting_function(data):
    return (f"You are a {data['genre']} author. Your task is to create a vivid and immersive setting for your story. The setting can be a place, a time period, or even a world of your own creation. A strong setting can transport readers to another place and time, and make your story more engaging and memorable.\n\n"
                f"Here are some things to keep in mind as you write your story:\n\n"
                f"1. Start by establishing the basic details of your setting, such as its physical features, climate, and geography.\n"
                f"2. Consider how the setting affects the characters and the plot. Does it create obstacles for the characters to overcome, or does it provide opportunities for them to succeed?\n"
                f"3. Use sensory details to bring your setting to life. Describe the sights, sounds, smells, and textures of the setting in vivid detail.\n\n"
                f"Title: {data['title']}\n"
                f"Genre: {data['genre']}\n"
                f"Characters: {data['characters']}\n"
                f"Plot: {data['plot']}\n\n"
                f"{data['prompt']}")

def setup_payoff_function(data):
    return (f"You are a {data['genre']} author. Your task is to create a story with strong set-ups and payoffs. A set-up is a detail or event that establishes an expectation or creates a question in the reader's mind. A payoff is the resolution or answer to that question or expectation. Strong set-ups and payoffs can make your story more engaging and satisfying.\n\n"
                f"Here are some things to keep in mind as you write your story:\n\n"
                f"1. Introduce set-ups early on in your story, so that readers have time to develop questions or expectations.\n"
                f"2. Make sure your payoffs are satisfying and not predictable, but also not completely out of left field.\n"
                f"3. You can use foreshadowing, callbacks, or other narrative techniques to tie your set-ups and payoffs together and create a cohesive story.\n\n"
                f"Title: {data['title']}\n"
                f"Genre: {data['genre']}\n"
                f"Characters: {data['characters']}\n"
                f"Plot: {data['plot']}\n\n"
                f"{data['prompt']}")

def three_act_function(data):
    return (f"{data['text']} take this text and apply to it this framework 3 act structure"
                f"Act 1 - Setup:\n"
                f"1. Introduction: Introduce the protagonist, their world, and the story's central problem.\n"
                f"2. Inciting Incident: Present an event that sets the story in motion and pushes the protagonist out of their comfort zone.\n"
                f"3. First Plot Point: The protagonist makes a decision or takes action that propels them into Act 2.\n\n"
                f"Act 2 - Confrontation:\n"
                f"4. Rising Action: The protagonist faces obstacles and challenges while pursuing their goal.\n"
                f"5. Midpoint: A turning point in the story that raises the stakes and deepens the protagonist's commitment.\n"
                f"6. Second Plot Point: The protagonist experiences a major setback or crisis that leads to the story's climax.\n\n"
                f"Act 3 - Resolution:\n"
                f"7. Climax: The protagonist faces the antagonist or the story's central problem in a final confrontation.\n"
                f"8. Falling Action: Show the consequences of the climax and wrap up any loose ends.\n"
                f"9. Resolution: The protagonist achieves (or fails to achieve) their goal, and the story's central problem is resolved.\n\n")
#step 1 output story
#

def story_circle_function(data):
    return (f"You are a {data['genre']} author. Your task is to write a {data['genre']} story using the Story Circle framework, which consists of 8 key steps. Make sure your story is vivid, intriguing, and engaging by focusing on the following aspects:\n\n"
                f"1. You: Introduce the protagonist in their ordinary world.\n"
                f"2. Need: Establish the protagonist's need, desire, or goal.\n"
                f"3. Go: The protagonist enters an unfamiliar situation or new world.\n"
                f"4. Search: The protagonist faces trials, challenges, and makes discoveries.\n"
                f"5. Find: The protagonist finds what they were looking for, often with a twist.\n"
                f"6. Take: The protagonist pays a price or faces consequences for their actions.\n"
                f"7. Return: The protagonist returns to their ordinary world, changed by the experience.\n"
                f"8. Change: Show how the protagonist has grown or changed as a result of their journey.\n\n")
def humanize_function(data):
    return (f"You are a {data['genre']} author. Your task is to write in a way that feels natural and human. Here are some tips to help you humanize your text:\n\n"
                            f"1. Use contractions, like 'don't' instead of 'do not' and 'can't' instead of 'cannot'.\n"
                            f"2. Vary sentence structure and length to make the writing more natural and flowing.\n"
                            f"3. Use colloquial language and phrases to create a conversational tone.\n"
                            f"4. Add small details that show the character's personality or point of view.\n"
                            f"5. Avoid overly technical or academic language, unless it's necessary for the story.\n\n"
                            f"Title: {data['title']}\n"
                            f"Genre: {data['genre']}\n"
                            f"Characters: {data['characters']}\n"
                            f"Plot: {data['plot']}\n\n"
                            f"{data['prompt']}")

def first_generated(data):
    return (f"You are a {data['genre']} author. Your task is to write a {data['genre']} story that is vivid, intriguing, and engaging. Pay close attention to the following aspects:\n\n"
              f"1. Setting: Include time period, location, and relevant background information.\n"
              f"2. Characters: Describe the protagonist, antagonist, and other key characters in terms of their appearance, motivations, and roles in the story.\n"
              f"3. Conflict: Clearly outline the main conflict and the stakes involved.\n"
              f"4. Dialogue: Use dialogue to advance the plot, reveal character, and provide information to the reader.\n"
              f"5. Theme: Develop the central theme throughout the plot, characters, and setting.\n"
              f"6. Tone: Maintain a consistent tone that is appropriate to the genre, setting, and characters.\n"
              f"7. Pacing: Vary the pace to build and release tension, advance the plot, and create a dramatic effect.\n\n"
              f"Title: {data['title']}\n"
              f"Genre: {data['genre']}\n"
              f"Characters: {data['characters']}\n"
              f"Plot: {data['plot']}\n")
tst = """Chapter 1:

The Enchanted Forest was a place of wonder and mystery, filled with towering trees that reached to the sky. The forest floor was carpeted with lush, green moss and glittering wildflowers, and the air was thick with the scent of blooming flowers and fragrant herbs.


But it was the forest's magical properties that made it truly remarkable. The trees were alive with an energy that pulsed through the air, sending a shimmering glow across the forest floor. The leaves sparkled with tiny points of light, and the branches rustled like the whispers of secrets untold.


Elara and Prince Aldric stepped into the forest's edge, their footsteps sinking into the soft earth as they gazed around in wonder. The prince reached out a hand to touch one of the trees, marveling at the sap that dripped from its trunk. "It's incredible," he breathed.


Elara nodded in agreement, eyes scanning the Forest's edge for any sign of danger. "But we must be cautious. The Forest is full of surprises, and not all of them will be friendly."


As they began to make their way deeper into the Forest, they couldn't help but feel the energy of the forest surrounding them. It filled them with a sense of purpose, a surety that they would succeed in their quest. They just hoped their confidence wouldn't be their downfall.


Chapter 2:

Elara was a skilled archer and a fierce warrior. With piercing blue eyes and hair that shone silver in the sunlight, she was a striking figure as they moved deeper into the forest.


Her background was shrouded in mystery. No one knew what brought her to the kingdom, but she had quickly made a name for herself as one of the most skilled archers in the land. She had a sharp mind and a quick wit that complemented her strength as a warrior.


As they walked deeper into the Forest, her eyes scanned the tops of the trees for any signs of danger. She couldn't let her guard down even for a moment, not with the fate of the kingdom resting on her shoulders.


Prince Aldric watched her move with a sense of awe, marveling at the way she seemed to blend into the forest. "You're incredible," he said, breaking the silence.


Elara smirked at his compliment, but there was a hint of sadness in her eyes. "It's not just about skill, you know. It's about survival. I've had to fight for my life more times than I can count."


They walked in silence for a while, each lost in their own thoughts. But Elara couldn't help but feel a sense of responsibility for the prince. If anything were to happen to him, it would all be on her. She had to make sure they both survived this journey.


Chapter 3:

Prince Aldric was the heir to the throne, with jet-black hair and piercing green eyes that glinted in the sunlight. He was a thoughtful and kind-hearted young man, but he also had a fierce determination that drove him.


He had been raised to believe in his duty to the kingdom, and he was willing to do whatever it took to achieve their goals. When the sorceress Morwen had cursed the kingdom, he had known that he couldn't just sit back and let his people suffer.


That was why they were now making their way through the Enchanted Forest, on a quest to retrieve a magical artifact that would break the curse and restore balance to the kingdom. It was a dangerous journey, but he was willing to risk his life for his people.


As they walked deeper into the Forest, Aldric couldn't help but feel a sense of purpose. This was what he was meant to do. It was his duty to make things right, and he would do whatever it took to succeed.


But he also had a personal stake in the matter. His sister had fallen ill as a result of the curse, and he couldn't bear to see her suffer. He would do whatever it took to save her and his kingdom, even if it meant risking his own life in the process.


Elara could see the determination in his eyes, and she knew that they were in this together. They were two strangers brought together by fate, and they would have to
"""
