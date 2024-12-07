from flask import Flask, request, jsonify
from train_model import ChatBotModel, tokenizer
from database.init_db import Session, ChatHistory
from database.knowledge_base import fetch_pubmed, save_to_db, get_knowledge_by_category
import torch
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# トークナイザーとモデル
model = ChatBotModel(vocab_size=1000, embed_size=128, hidden_size=256)
model.load_state_dict(torch.load('chatbot_model/chatbot_model.pt'))
model.eval()

# データベースセッション
session = Session()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    input_seq = tokenizer.texts_to_sequences([user_input])
    input_seq = pad_sequences(input_seq, maxlen=10, padding='post')

    inputs = torch.LongTensor(input_seq)
    outputs = model(inputs)
    predicted_idx = torch.argmax(outputs, dim=1).item()

    response = tokenizer.sequences_to_texts([[predicted_idx]])[0]

    # データベースに保存
    chat_entry = ChatHistory(user_message=user_input, bot_response=response)
    session.add(chat_entry)
    session.commit()

    return jsonify({'response': response})

@app.route('/generate', methods=['POST'])
def generate_response():
    user_input = request.json.get('message')
    # PubMedを利用して、関連する知識を取得
    knowledge_data = fetch_pubmed(user_input)
    save_to_db(knowledge_data, category="medical")
    
    # PubMedから得たデータを表示
    return jsonify({'response': knowledge_data})

@app.route('/get_knowledge', methods=['GET'])
def get_knowledge():
    category = request.args.get('category')
    knowledge_data = get_knowledge_by_category(category)
    return jsonify({'knowledge': knowledge_data})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
CORS(app)

import os
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'build'), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'build'), path)
