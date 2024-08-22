require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const axios = require('axios');

const app = express();
app.use(express.json());

const THINGSPEAK_API_KEY = process.env.THINGSPEAK_API_KEY;
const EMAIL_USER = process.env.EMAIL_USER;
const EMAIL_PASS = process.env.EMAIL_PASS;

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: EMAIL_USER,
        pass: EMAIL_PASS
    }
});

function sendEmail() {
    const mailOptions = {
        from: EMAIL_USER,
        to: 'chakraborty.nabanita05@gmail.com',
        subject: 'Motion Detected at Door',
        html: `
            <p>Motion detected at the door. Do you want to open the door?</p>
            <p>
                <a href="https://smart-home-automation.onrender.com/open">Yes</a> or 
                <a href="https://smart-home-automation.onrender.com/close">No</a>
            </p>
        `
    };

    transporter.sendMail(mailOptions, function(error, info) {
        if (error) {
            console.log(error);
        } else {
            console.log('Email sent: ' + info.response);
        }
    });
}

async function updateThingSpeak(status) {
    try {
        const response = await axios.post(`https://api.thingspeak.com/update`, null, {
            params: {
                api_key: THINGSPEAK_API_KEY,
                field2: status  
            }
        });
        console.log('Updated ThingSpeak:', response.data);
    } catch (error) {
        console.error('Error updating ThingSpeak:', error);
    }
}

app.get('/open', (req, res) => {
    console.log("open");
    
    updateThingSpeak(1);  
    res.send('Door Opened');
});

app.get('/close', (req, res) => {
    console.log("close");
    updateThingSpeak(0);  
    res.send('Door Closed');
});

app.post('/motion-detected', (req, res) => {
    sendEmail();
    res.send('Email sent!');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
