from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from train_model import ChatBotModel, tokenizer
from database.init_db import Session, ChatHistory
import torch
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# トークナイザーとモデル
model = ChatBotModel(vocab_size=1000, embed_size=128, hidden_size=256)
model.load_state_dict(torch.load('chatbot_model/chatbot_model.pt'))
model.eval()

transformer_model_name = "gpt2"
transformer_tokenizer = AutoTokenizer.from_pretrained(transformer_model_name)
transformer_model = AutoModelForCausalLM.from_pretrained(transformer_model_name)

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
    inputs = transformer_tokenizer.encode(user_input, return_tensors='pt')
    outputs = transformer_model.generate(inputs, max_length=50, num_return_sequences=1, temperature=0.7)
    response = transformer_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
