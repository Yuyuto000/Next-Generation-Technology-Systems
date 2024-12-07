// predictionModel.ts
import * as tf from '@tensorflow/tfjs';

// 仮の予測モデル
export const predictionModel = {
  predict: async (data: number[]): Promise<number> => {
    // データが正規化されていると仮定し、簡単な線形回帰モデルを用いて予測を行う
    
    // モデルの準備：ここでは単純な線形回帰を例にします
    const model = await buildModel();
    
    // 入力データをTensorに変換
    const inputTensor = tf.tensor2d([data], [1, data.length]);
    
    // 予測を実行
    const prediction = model.predict(inputTensor) as tf.Tensor;
    
    // 結果を取得し、予測値を返す
    return prediction.dataSync()[0]; // 単一の予測値を取得
  }
};

// モデルを構築する関数（ここでは単純な線形回帰モデル）
const buildModel = async () => {
  const model = tf.sequential();
  
  // 入力層（特徴量数に応じてユニット数を変更）
  model.add(tf.layers.dense({ units: 64, activation: 'relu', inputShape: [10] }));
  
  // 隠れ層
  model.add(tf.layers.dense({ units: 32, activation: 'relu' }));
  
  // 出力層（単一の出力）
  model.add(tf.layers.dense({ units: 1 }));
  
  // モデルのコンパイル
  model.compile({ optimizer: 'adam', loss: 'meanSquaredError' });
  
  // モデルの訓練（仮のデータで訓練）
  await trainModel(model);
  
  return model;
};

// モデルの訓練（ここでは仮のデータを使う）
const trainModel = async (model: tf.LayersModel) => {
  // 仮のデータ：実際には学習データセットを用意する必要があります
  const xs = tf.tensor2d([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]);
  const ys = tf.tensor2d([[15]]);
  
  // 訓練実行
  await model.fit(xs, ys, { epochs: 100 });
};
