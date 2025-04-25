const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/new-endpoint', (req, res) => {
    const { field1, field2 } = req.body;

    // Basic validation
    if (!field1 || !field2) {
        return res.status(400).json({ error: 'Field1 and Field2 are required.' });
    }

    // Process the request here
    // For example, save to database or perform some operations

    res.status(200).json({ message: 'Data received successfully', data: { field1, field2 } });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});