const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { exec } = require('child_process'); // Used to call the Python script
const path = require('path'); // To handle paths more easily
const app = express();

app.use(cors());
app.use(bodyParser.json());

// Define the path to your Python executable
const pythonPath = 'C:\\path\\to\\your\\venv\\Scripts\\python.exe'; // Update this path

app.post('/predict', (req, res) => {
    const { text } = req.body;

    if (!text) {
        return res.status(400).json({ error: 'Text input is required.' });
    }

    // Call the Python script
    exec(`${pythonPath} ${path.join(__dirname, 'predict.py')} "${text}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            console.error(`stderr: ${stderr}`); // Log the stderr for debugging
            return res.status(500).json({ error: 'Failed to make prediction.' });
        }

        // Output from the Python script will be in stdout
        const result = stdout.trim(); // Remove any extra whitespace
        res.json({ result });
    });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
