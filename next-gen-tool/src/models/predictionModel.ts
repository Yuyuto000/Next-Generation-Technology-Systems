import { processData } from '../utils/dataPreprocessing';
import { predictionModel } from '../models/predictionModel';

export const makePrediction = async (data: any) => {
  try {
    const processedData = processData(data);
    const prediction = await predictionModel.predict(processedData);
    return prediction;
  } catch (error) {
    throw new Error('Error during prediction');
  }
};
