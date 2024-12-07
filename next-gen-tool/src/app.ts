import express from 'express';
import dotenv from 'dotenv';
import { predictionRouter } from './controllers/predictionController';

dotenv.config();

const app = express();
app.use(express.json());

app.use('/api/predict', predictionRouter);

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
