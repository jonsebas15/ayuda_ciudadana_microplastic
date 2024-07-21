import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
    user: 'qwuhbjku',
    password:'BWpiUtOmaW0GP7-z6kztOw_87js52yZT',
    host:'rogue.db.elephantsql.com',
    port:'5432',
    database:'qwuhbjku',
});

export default pool;