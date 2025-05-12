import app from './app';

const PORT: number = parseInt(process.env.PORT as string, 10) || 8080;

app.listen(PORT, () => {
  console.log(`nodejs-pubsub-tutorial listening on port ${PORT}`);
});
