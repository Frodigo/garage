import express, { Request, Response } from 'express';

const app = express();

app.use(express.json());

interface PubSubMessage {
  teamA: string;
  teamB: string;
  score: string;
}

interface PubSubRequest extends Request {
  body: {
    message?: {
      data: string; // Base64 encoded string
    };
  };
}

app.post('/', (req: PubSubRequest, res: Response) => {
  try {
    console.log(req.body)
    if (!req.body || !req.body.message || !req.body.message.data) {
      throw new Error('No Pub/Sub message received');
    }

    console.log(`Received message: ${req.body.message.data}`);
    const dataBuffer = Buffer.from(req.body.message.data, 'base64');
    console.log(`Decoded message: ${dataBuffer.toString()}`);
    const message: PubSubMessage = JSON.parse(dataBuffer.toString());
    const { teamA, teamB, score } = message;

    if (!teamA || !teamB || !score) {
      throw new Error('Missing required fields');
    }

    const summary = `The match between ${teamA} and ${teamB} ended with a score of ${score}.`;

    console.log(summary);
    res.status(204).send();
  } catch (error) {
    console.error(`error: ${(error as Error).message}`);
    res.status(400).send(`Bad Request: ${(error as Error).message}`);
  }
});

export default app;
