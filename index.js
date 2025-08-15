const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.post('/', (req, res) => {
    const request = req.body;

    if (request.request.type === 'LaunchRequest') {
        return res.json(buildResponse("Welcome! Ask me to generate a picture."));
    }

    if (request.request.type === 'IntentRequest') {
        const intentName = request.request.intent.name;

        if (intentName === "GeneratePictureIntent") {
            const subject = request.request.intent.slots.subject.value || "something";
            return res.json(buildResponse(`Okay! Generating a picture of ${subject}.`));
        }
    }

    return res.json(buildResponse("Sorry, I didn't understand that."));
});

function buildResponse(output) {
    return {
        version: "1.0",
        response: {
            outputSpeech: {
                type: "PlainText",
                text: output
            },
            shouldEndSession: true
        }
    };
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
