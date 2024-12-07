import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# モデル定義
class ChatBotModel(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super(ChatBotModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x):
        embed = self.embedding(x)
        lstm_out, _ = self.lstm(embed)
        output = self.fc(lstm_out[:, -1, :])
        return output

# トークナイザー初期化
tokenizer = Tokenizer(num_words=1000)

# ダミーデータセット
data = [
    ("こんにちは", "こんにちは！どうしましたか？"),
    ("元気ですか？", "元気ですよ！あなたは？"),
    ("ありがとう", "どういたしまして！"),
]

# データの前処理
inputs, outputs = zip(*data)
tokenizer.fit_on_texts(inputs + outputs)
input_sequences = tokenizer.texts_to_sequences(inputs)
output_sequences = tokenizer.texts_to_sequences(outputs)

max_len = max(len(seq) for seq in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_len, padding='post')
output_sequences = pad_sequences(output_sequences, maxlen=max_len, padding='post')

X_train, X_test, y_train, y_test = train_test_split(input_sequences, output_sequences, test_size=0.2)

# モデル構築と訓練
model = ChatBotModel(vocab_size=1000, embed_size=128, hidden_size=256)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

epochs = 10
for epoch in range(epochs):
    for i in range(len(X_train)):
        inputs = torch.LongTensor([X_train[i]])
        targets = torch.LongTensor([y_train[i]])

        outputs = model(inputs)
        loss = loss_fn(outputs, targets.squeeze())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

# モデル保存
torch.save(model.state_dict(), 'chatbot_model/chatbot_model.pt')
print("モデルを保存しました。")
