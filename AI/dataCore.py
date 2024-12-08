import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# データをロードする関数
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

# データの前処理を行う関数
def preprocess_data(data):
    if 'target' not in data.columns:
        print("Error: 'target' column is missing from the dataset.")
        return None, None, None, None
    
    X = data.drop('target', axis=1)
    y = data['target']
    
    # スケーリング（標準化）
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

# ランダムフォレストモデルを定義する関数
def define_model():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    return model

# モデルを訓練する関数
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

# モデルの予測と評価を行う関数
def predict_and_evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    
    # 精度の計算
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    
    # 混同行列と分類レポート
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)
    
    print("Confusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(cr)
    
    return accuracy

# 深層学習モデルを定義する関数
def define_deep_learning_model(input_shape):
    model = Sequential()
    model.add(Dense(128, input_dim=input_shape, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # 二値分類
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model

# 深層学習モデルを訓練する関数
def train_deep_learning_model(model, X_train, y_train, epochs=10, batch_size=32):
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    return model, history

# モデルを保存する関数
def save_model(model, model_name='model.h5'):
    model.save(model_name)
    print(f'Model saved as {model_name}')

# モデルをロードする関数
def load_model(model_name='model.h5'):
    model = tf.keras.models.load_model(model_name)
    return model

# ハイパーパラメータのチューニングを行う関数
def tune_hyperparameters(model, X_train, y_train, param_grid):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)
    grid_search.fit(X_train, y_train)
    
    print("Best Parameters:", grid_search.best_params_)
    print("Best Score:", grid_search.best_score_)
    
    return grid_search.best_estimator_

# 新しいデータに対して推論を行う関数
def make_inference(model, new_data):
    prediction = model.predict(new_data)
    prediction_class = (prediction > 0.5).astype(int)  # 二値分類の場合
    return prediction_class

# TensorBoard用のコールバックを定義する関数
def log_with_tensorboard(log_dir='logs'):
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
    return tensorboard_callback

# TensorBoardで訓練する関数
def train_with_tensorboard(model, X_train, y_train, epochs=10, batch_size=32, log_dir='logs'):
    tensorboard_callback = log_with_tensorboard(log_dir)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, callbacks=[tensorboard_callback])
    return model, history
