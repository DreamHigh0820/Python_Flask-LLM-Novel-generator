from flask import Flask, redirect, request, jsonify, render_template, url_for
import openai, time
from forms import SettingsForm
from helper_functions import formatText,first_generated,iceberg_function,setting_function,setup_payoff_function,three_act_function,story_circle_function,humanize_function
from flask_login import LoginManager, login_required,current_user
from models import User, db
import requests

website_url = "https://aing-j2lus53e4q-uc.a.run.app"
app = Flask(__name__)
# Show changes made to html files without refreshing server
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///j2lus53e4q2.db'

#for google Auth

db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)


# nlp = spacy.load("en_core_web_sm"), spacy

default_api_key = ""  # Add this line

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('default_views.home',login=''))

@app.route("/", methods=["GET"])
# @login_required
def index():
    form = SettingsForm()
    saved_api_key = request.args.get("api-key", default_api_key)
    return render_template("index.html", saved_api_key=saved_api_key,form=form)

@app.route("/save-settings", methods=["POST"])
def save_settings():
    global default_api_key
    form = SettingsForm(request.form)
    if form.validate():
        default_api_key = form.api_key.data
        print(f"New API Key: {default_api_key}")  # Add this line for debugging
        return "" , 204
    else:
        # handle form validation errors
        print(form.errors)
        return "Invalid form data", 400

@app.route("/save-api-key", methods=["POST"])
def save_api_key():
    default_api_key = request.form["api-key"]
    print(f"New API Key: {default_api_key}")  # Add this line for debugging
    return "", 204

def checkapiKeyAvailable(apiKey):
    # check apikey available
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json"
    }
    url = "https://api.openai.com/v1/engines/davinci/completions"
    data = {
        "prompt": "test",
        "max_tokens": 5
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        # openai.api_key = apiKey  # Add this line
        return True
    else:
        return False

@app.route("/generate-agent", methods=["POST"])
def generate_agent():
    print("generate() called")
    openai.api_key = default_api_key
    data = request.get_json()
    prompt = data["prompt"]
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    text = response.choices[0].text.strip()
    return jsonify({"text": text})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = first_generated(data)
    generated_text = ""
    messages = [
            {"role": "system", "content": prompt},
        ]

    default_api_key = data["apiKey"]

    if checkapiKeyAvailable(default_api_key) is True:
        openai.api_key = default_api_key
    else:
        return False
    
    for index,chapter in enumerate(data['prompts']):
        messages.append({"role":"user","content":chapter})
        print(chapter)
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages
        )
        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        generated_text +=f"Chapter {index+1}\n"+response['choices'][0]['message']['content']

    print("messages====================================", messages)

    # Refine the text and add gaps between different parts of the story
    refinement_prompt = f"Refine the following text for better consistency, coherence, and add gaps between different chapters of the story:\n\n{generated_text}\n\nRefined Text:"
    refinement_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=refinement_prompt,
        max_tokens=900,
        n=1,
        stop=None,
        temperature=0.5
    )
    refined_text = refinement_response.choices[0].text.strip()
    # print("refined_text------------------------------", refined_text)
    # # Add gap agent
    # chapters = refined_text.split("Chapter ")
    # for item in chapters:
    #     if item.strip() == "":
    #         chapters.remove(item)
    # for i, text in enumerate(chapters):
    #     if i > 0:
    #         text_part_1 = chapters[i - 1]
    #         text_part_2 = text
    #         gap_prompt = f"Continue the story smoothly between:\n\n{text_part_1}\n\nand\n\n{text_part_2}\n\nRefined transition:"

    #         gap_response = openai.Completion.create(
    #             engine="text-davinci-002",
    #             prompt=gap_prompt,
    #             max_tokens=250,
    #             n=1,
    #             stop=None,
    #             temperature=0.5
    #         )
    #         gap_text = gap_response.choices[0].text.strip()
    #         chapters[i-1] = "Chapter"+ chapters[i-1]+gap_text+"\n\n"
    # combined_text = "".join(chapters)
    # print("combined_text=============================", combined_text)
    return jsonify({"text": refined_text})
    # Add story circle agent
    # story_circle_prompt = story_circle_function(data)
    story_circle_prompt = f"please write this {combined_text} as story circle"
    
    print(f"Story Circle Prompt: {story_circle_prompt}")

    # Add 3-act agent
    three_act_prompt = three_act_function(data)
    print(f"3-Act Structure Prompt: {three_act_prompt}")

    # Add Iceberg Method
    iceberg_prompt = iceberg_function(data)
    print(f"Iceberg Method Prompt: {iceberg_prompt}")

    # Add Set-up & Payoffs
    setup_and_payoff_prompt = setup_payoff_function(data)
    print(f"Set-up and Payoff Prompt: {setup_and_payoff_prompt}")

    # Add Setting Details
    setting_prompt = setting_function(data)
    print(f"Setting Prompt: {setting_prompt}")

    # Add Tone Details
    tone_prompt = (f"As a {genre} author, your task is to establish the tone of your story. The tone, or the overall mood and atmosphere, is crucial in creating an engaging and immersive experience for the reader. It helps set the emotional context and guides the reader's expectations throughout the narrative.\n\n"
                f"Keep these points in mind while crafting the tone of your story:\n\n"
                f"1. Identify the primary mood you aim to evoke, such as suspense, humor, or melancholy.\n"
                f"2. Utilize word choice, sentence structure, and pacing to reinforce the desired tone. Opt for vocabulary and phrasing that reflects the intended mood.\n"
                f"3. Ensure consistency in tone by incorporating elements like setting, character actions, and dialogue that align with the chosen mood.\n\n"
                f"Incorporate elements like setting, character actions, and dialogue to reinforce the tone. Make sure these elements are consistent with the mood you want to create.\n\n"
                f"Title: {data['title']}\n"
                f"Genre: {genre}\n"
                f"Characters: {data['characters']}\n"
                f"Plot: {data['plot']}\n\n"
                f"{data['prompt']}")
    print(f"Tone Prompt: {tone_prompt}")

    # Add Humanized Output
    humanize_text_prompt = humanize_function(data)
    print(f"Humanize Text Prompt: {humanize_text_prompt}")

    # Add editing agent
    editing_prompt = f"Please edit the following text for grammar, punctuation, and overall readability:\n\n{combined_text}\n\nEdited Text:"
    editing_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=editing_prompt,
        max_tokens=len(combined_text) + 300,  # Allow some extra tokens for edits
        n=1,
        stop=None,
        temperature=0.5
    )
    edited_text = editing_response.choices[0].text.strip()

    # Format edited text
    formatted_text = formatText(edited_text)
    return jsonify(formatted_text)

@app.route("/generate_test", methods=["POST"])
def generate_test():
    formatted_text = "<p>hello my name is yassine lahbalat</p>"
    return jsonify(formatted_text)

from default_views import default_views
from auth import auth
from stripe_view import stripe_view

app.register_blueprint(default_views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(stripe_view, url_prefix='/')
def run():
  app.run(host='0.0.0.0',port=8080)
if __name__ == "__main__":
    app.run(debug=True)
    run()
    