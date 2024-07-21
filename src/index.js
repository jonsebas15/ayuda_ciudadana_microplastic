import express from 'express';
import morgan from 'morgan';
import cors from 'cors'
import tasksroutes from './routes/routes.js'

const app = express();

app.use(cors({
    origin: 'http://localhost:3000',
    credentials: true
}))
app.use(morgan('dev'));
app.use(express.json());
app.use(tasksroutes)


app.listen(4000)
console.log("server port 4000")