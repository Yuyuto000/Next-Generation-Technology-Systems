import { Router } from 'express';
import { makePrediction } from '../services/predictionService';

export const predictionRouter = Router();

predictionRouter.post('/', async (req, res) => {
  const { data } = req.body;
  if (!data) {
    return res.status(400).json({ error: 'No data provided for prediction.' });
  }

  try {
    const prediction = await makePrediction(data);
    return res.status(200).json({ prediction });
  } catch (error) {
    return res.status(500).json({ error: 'Error in making prediction' });
  }
});
