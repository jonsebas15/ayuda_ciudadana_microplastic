import { Router }  from 'express'
import {AI} from '../controllers/ai.js'


const router = Router()


/* router.post('/task', postplastic); */
router.post('/Ai', AI);
export default router;