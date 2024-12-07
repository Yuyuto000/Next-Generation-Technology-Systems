// dataPreprocessing.ts
import * as tf from '@tensorflow/tfjs';

// データの前処理を行う関数
export const processData = (data: any): number[] => {
  // 数値データのスケーリング、正規化を行う
  const scaledData = scaleData(data);
  
  // 欠損値の補完
  const cleanedData = handleMissingValues(scaledData);
  
  // 必要に応じてさらに前処理を行う（例：特徴量の選択）
  const finalProcessedData = cleanNoise(cleanedData);
  
  return finalProcessedData;
};

// データのスケーリング（例：Min-Maxスケーリング）
const scaleData = (data: any): number[] => {
  const min = Math.min(...data);
  const max = Math.max(...data);
  
  return data.map((value: number) => (value - min) / (max - min));
};

// 欠損値処理
const handleMissingValues = (data: any): number[] => {
  // 欠損値がある場合は、0で補完する
  return data.map((value: any) => (value === null || value === undefined ? 0 : value));
};

// ノイズの除去（簡単な例として、平均値で補完）
const cleanNoise = (data: any): number[] => {
  const mean = data.reduce((acc: number, value: number) => acc + value, 0) / data.length;
  return data.map((value: number) => (value > mean * 1.5 ? mean : value)); // 1.5倍を超える値を平均で補完
};

