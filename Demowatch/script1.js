const video = document.getElementById('videoFeed');
const canvas = document.getElementById('canvas');
const baseURL = document.getElementById('baseURL');
const instructionText = document.getElementById('instructionText');
const responseText = document.getElementById('responseText');
const intervalSelect = document.getElementById('intervalSelect');
const startButton = document.getElementById('startButton');
const dangerAlert = document.getElementById('dangerAlert');
const aiThinking = document.getElementById('aiThinking');

// --- Source mode elements ---
const modeCamera     = document.getElementById('modeCamera');
const modeUpload     = document.getElementById('modeUpload');
const uploadZone     = document.getElementById('uploadZone');
const videoFileInput = document.getElementById('videoFileInput');
const uploadFilename = document.getElementById('uploadFilename');

const alarmSound = new Audio(
    'https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3'
);

let stream;
let intervalId;
let isProcessing  = false;
let isAlarmActive = false;
let uploadedVideoURL = null;   // object URL for the uploaded file

// ---- Toggle upload zone visibility when mode changes ----
document.querySelectorAll('input[name="sourceMode"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const isUpload = modeUpload.checked;
        uploadZone.classList.toggle('visible', isUpload);
    });
});

// ---- When user picks a file, load it into the video element preview ----
videoFileInput.addEventListener('change', () => {
    const file = videoFileInput.files[0];
    if (!file) return;

    // Revoke any previous object URL to avoid memory leaks
    if (uploadedVideoURL) URL.revokeObjectURL(uploadedVideoURL);

    uploadedVideoURL = URL.createObjectURL(file);

    // Show short filename in the UI
    const shortName = file.name.length > 28
        ? file.name.slice(0, 25) + '...'
        : file.name;
    uploadFilename.textContent = shortName;
    uploadFilename.classList.add('loaded');

    // Load into video element so frames can be captured immediately
    video.src = uploadedVideoURL;
    video.loop = true;
    video.muted = true;
    video.load();
});





instructionText.value =
`SYSTEM INSTRUCTION:
Analyze the image visual data.
1. DETECT: Humans, weapons, dangerous objects.
2. REPORT: Return a list in this strict format:
   [TYPE] :: Description :: [Threat Level %]

Example:
[HUMAN] :: Male, blue shirt, sitting :: [10%]
[OBJECT] :: Black smartphone in hand :: [0%]

Do not write prose. Do not write code. Be robotic.`;


async function sendChatCompletionRequest(instruction, imageBase64URL) {
    const response = await fetch(`${baseURL.value}/v1/chat/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            max_tokens: 150,       // Reduced tokens to keep it brief
            temperature: 0.1,      // <--- IMPORTANT: Low temp stops the "stories" and code
            messages: [{
                role: 'user',
                content: [
                    { type: 'text', text: instruction },
                    { type: 'image_url', image_url: { url: imageBase64URL } }
                ]
            }]
        })
    });

    const data = await response.json();
    return data.choices[0].message.content;
}

async function initCamera() {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
}

async function initVideoSource() {
    if (modeUpload.checked) {
        // ---- VIDEO FILE MODE ----
        if (!uploadedVideoURL) {
            // Prompt the user to pick a file first
            videoFileInput.click();
            // Wait until the file has been loaded (change event fires)
            await new Promise(resolve => {
                videoFileInput.addEventListener('change', resolve, { once: true });
            });
            if (!uploadedVideoURL) throw new Error('No file selected.');
        }
        // video.src is already set by the change handler — just play
        video.srcObject = null;
        video.src = uploadedVideoURL;
        video.loop = true;
        video.muted = true;
        await video.play();
    } else {
        // ---- CAMERA MODE ----
        await initCamera();
    }
}

function captureImage() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    return canvas.toDataURL('image/jpeg', 0.8);
}

function formatResponse(text) {
    return text
        .split(/\r?\n/)
        .map(line => line.trim())
        .filter(line => line.length > 0);
}


function triggerAlarm() {
    if (!isAlarmActive) {
        isAlarmActive = true;
        video.classList.add('alarm');
        dangerAlert.style.display = 'block';

       

        alarmSound.loop = true;
        alarmSound.play();
    }
}

function stopAlarm() {
    isAlarmActive = false;
    video.classList.remove('alarm');
    dangerAlert.style.display = 'none';

 

    alarmSound.pause();
    alarmSound.currentTime = 0;
}



async function sendData() {
    if (!isProcessing) return;

    aiThinking.style.display = 'block';

    try {
        const response = await sendChatCompletionRequest(
            instructionText.value,
            captureImage()
        );

        const lines = formatResponse(response);

        // Turn ON glow when new response arrives
        responseText.classList.add("active");

        // --- CHANGE START ---
        // Clear the box so we only see the current scan results
        responseText.value = ""; 
        
        lines.forEach(line => {
            // Append the new clean lines
            responseText.value += `> ${line}\n`; 
        });
        // --- CHANGE END ---

        // Auto-scroll to bottom (optional now that we clear it, but good to keep)
        responseText.scrollTop = responseText.scrollHeight;

        const dangerousTerms = ['knife', 'gun', 'weapon', 'blade', 'firearm','fire'];
        dangerousTerms.some(term =>
            response.toLowerCase().includes(term)
        )
            ? triggerAlarm()
            : stopAlarm();

    } catch (error) {
        // Only show this if it actually fails
        responseText.value = '⚠️ CONNECTION LOST // RETRYING...';
        console.error(error);

    } finally {
        aiThinking.style.display = 'none';

        // Turn OFF glow after update
        setTimeout(() => {
            responseText.classList.remove("active");
        }, 800);
    }
}

startButton.onclick = async () => {
    isProcessing = !isProcessing;
    startButton.textContent = isProcessing ? "Stop" : "Start";
    startButton.classList.toggle('stop', isProcessing);

    if (isProcessing) {
        try {
            // Use camera OR uploaded video based on current mode
            const isUploadMode = modeUpload.checked;
            if (isUploadMode) {
                if (!uploadedVideoURL) {
                    // No file loaded yet — trigger picker then wait
                    await initVideoSource();
                } else {
                    // File already loaded; just play
                    video.srcObject = null;
                    video.src = uploadedVideoURL;
                    video.loop = true;
                    video.muted = true;
                    await video.play();
                }
            } else {
                if (!stream) await initCamera();
            }
        } catch (err) {
            console.error('Source init failed:', err);
            isProcessing = false;
            startButton.textContent = "Start";
            startButton.classList.remove('stop');
            return;
        }

        sendData();
        intervalId = setInterval(sendData, Number(intervalSelect.value));

    } else {
        clearInterval(intervalId);
        stopAlarm();

        if (modeUpload.checked) {
            // Pause the uploaded video but keep the object URL intact
            video.pause();
        } else {
            // Stop the webcam stream
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
                video.srcObject = null;
            }
        }
    }
};