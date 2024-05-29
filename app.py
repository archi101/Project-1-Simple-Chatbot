from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Initialize the ChatBot
chatbot = ChatBot('BasicBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Basic Functionality: Greeting and Farewell Messages
greetings = ["hello", "hi", "hey"]
farewells = ["bye", "goodbye", "see you"]

# Remembering previous interactions
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

questions = ["What's your name?", "How can I help you today?", "Do you need assistance with something specific?"]
question_counter = 0

@app.route('/get_response', methods=['POST'])
def get_response():
    global question_counter
    user_input = request.json.get('message')
    conversation_history.append(user_input)

    if question_counter < len(questions):
        response = questions[question_counter]
        question_counter += 1
    else:
        if any(greeting in user_input.lower() for greeting in greetings):
            response = "Hello! How can I assist you today?"
        elif any(farewell in user_input.lower() for farewell in farewells):
            response = "Goodbye! Have a great day!"
        else:
            try:
                response = chatbot.get_response(user_input).text
            except:
                response = "I'm sorry, I didn't understand that. Can you please rephrase?"

    conversation_history.append(response)
    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=True)
