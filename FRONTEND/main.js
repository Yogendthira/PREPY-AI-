// URL Parameters and Session Data
const urlParams = new URLSearchParams(window.location.search);
const prepType = urlParams.get('type') || 'interview';
const mode = urlParams.get('mode') || 'superman';

let sessionData = null;
let conversationHistory = [];
let recognition;
let isMicMuted = false;
let isAiSpeaking = false;
let isRecognitionActive = false;
let silenceTimer = null;
let currentTranscript = '';

// Turn counting logic
let turnCount = 0;
const MAX_TURNS = 5;

// Load session data from localStorage
try {
    const stored = localStorage.getItem('prepySession');
    if (stored) {
        const session = JSON.parse(stored);
        sessionData = session.sessionData;
        conversationHistory = session.history || [];
        turnCount = Math.floor(conversationHistory.length / 2);
    }
} catch (e) {
    console.error('Session load error:', e);
}

// Set session title
document.getElementById('sessionTitle').textContent = prepType === 'interview' ? 'PREPY Pvt Ltd Interview' : 'Hackathon Prep';

// Mode configuration
const modeImages = { 'superman': 'SUPERMAN MODE.png', 'batman': 'BATMAN MODE.png', 'hulk': 'HULK MODE.png' };
const modeNames = { 'superman': 'INTERVIEWER AGENT SUPERMAN', 'batman': 'INTERVIEWER AGENT BATMAN', 'hulk': 'INTERVIEWER AGENT HULK' };

document.getElementById('characterImage').src = modeImages[mode];
document.getElementById('evaluatorLabel').textContent = `AI - ${modeNames[mode]}`;

const mouthVideo = document.getElementById('mouthVideo');
const messageInput = document.getElementById('messageInput');

// ========================================
// CAMERA
// ========================================
async function initCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        const userVideo = document.getElementById('userWebcam');
        userVideo.srcObject = stream;

        console.log("Camera started...");

        if (!isMicMuted) {
            setTimeout(() => startListening(), 500);
        }

    } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Could not access camera. Please allow camera permissions.");
    }
}

window.addEventListener('load', initCamera);

// ========================================
// SPEECH RECOGNITION
// ========================================
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        console.log("Speech recognition started");
        isRecognitionActive = true;
        if (!isMicMuted) {
            messageInput.placeholder = "Listening... (Speak now)";
            document.getElementById('micBtn').style.backgroundColor = '#4caf50'; // Solid green to indicate listening
        }
    };

    recognition.onend = () => {
        console.log("Speech recognition ended");
        isRecognitionActive = false;
        document.getElementById('micBtn').style.backgroundColor = ''; // Reset color

        // Auto-restart if it shouldn't be stopped
        if (!isMicMuted && !isAiSpeaking) {
            console.log("Auto-restarting speech recognition...");
            setTimeout(() => startListening(), 300);
        } else if (isAiSpeaking) {
            messageInput.placeholder = "AI Speaking...";
        } else {
            messageInput.placeholder = "Mic Muted";
        }
    };

    recognition.onresult = (event) => {
        if (isMicMuted || isAiSpeaking) return;

        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }

        if (finalTranscript) {
            currentTranscript += finalTranscript + ' ';
            console.log("Final transcript:", finalTranscript);
        }

        // Update input box with what we have so far
        const displayText = (currentTranscript + interimTranscript).trim();
        if (displayText) {
            messageInput.value = displayText;
        }

        // Reset silence timer
        if (silenceTimer) clearTimeout(silenceTimer);

        // Wait for 2 seconds of silence before sending
        if (currentTranscript.trim() || interimTranscript.trim()) {
            silenceTimer = setTimeout(() => {
                if (currentTranscript.trim()) {
                    console.log("Silence detected, sending message...");
                    messageInput.value = currentTranscript.trim();
                    sendMessage();
                    currentTranscript = '';
                }
            }, 2000);
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        isRecognitionActive = false;
        document.getElementById('micBtn').style.backgroundColor = '';

        if (event.error === 'not-allowed') {
            isMicMuted = true;
            updateMicButtonUI();
            messageInput.placeholder = "Mic permission denied";
            alert("Microphone access denied. Please allow microphone access in your browser settings.");
        } else if (event.error === 'no-speech') {
            // Just restart if no speech detected
            if (!isMicMuted && !isAiSpeaking) {
                setTimeout(() => startListening(), 200);
            }
        } else if (event.error === 'network') {
            console.log("Network error, retrying...");
            setTimeout(() => startListening(), 1000);
        }
    };
} else {
    alert("Your browser does not support speech recognition. Please use Chrome or Edge.");
}

function startListening() {
    if (recognition && !isMicMuted && !isAiSpeaking && !isRecognitionActive) {
        try {
            recognition.start();
        } catch (e) {
            // Ignore error if already started
            if (e.message.indexOf('already started') === -1) {
                console.error("Recognition start error:", e);
            }
            isRecognitionActive = true;
        }
    }
}

function stopListening() {
    if (recognition) {
        try {
            recognition.stop();
        } catch (e) {
            console.error("Recognition stop error:", e);
        }
        isRecognitionActive = false;
    }
    if (silenceTimer) {
        clearTimeout(silenceTimer);
        silenceTimer = null;
    }
}

// ========================================
// TEXT-TO-SPEECH & ANIMATION
// ========================================
let selectedVoice = null;

function loadVoices() {
    const voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
        // Try to find a specific consistent voice
        selectedVoice = voices.find(voice =>
            voice.name.includes('Microsoft Mark') ||
            voice.name.includes('Google US English') ||
            (voice.lang.includes('en') && voice.name.includes('Male'))
        ) || voices.find(voice => voice.lang.includes('en'));

        console.log("Voice selected:", selectedVoice ? selectedVoice.name : "Default");
    }
}

// Load voices immediately and also wait for the event
loadVoices();
if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = loadVoices;
}

function speakText(text, isLastMessage = false) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();

        // Ensure voices are loaded if selectedVoice is still null
        if (!selectedVoice) loadVoices();

        const utterance = new SpeechSynthesisUtterance(text);

        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }

        utterance.pitch = 1.0; // Reset pitch to normal for more natural sound
        utterance.rate = 1.0;  // Reset rate to normal

        utterance.onstart = () => {
            isAiSpeaking = true;
            stopListening();
            startMouthAnimation();
            messageInput.placeholder = "AI Speaking...";
        };

        utterance.onend = () => {
            isAiSpeaking = false;
            stopMouthAnimation();

            if (isLastMessage) {
                endSession();
            } else {
                startListening();
            }
        };

        utterance.onerror = () => {
            isAiSpeaking = false;
            stopMouthAnimation();
            startListening();
        };

        window.speechSynthesis.speak(utterance);
    } else {
        startMouthAnimation();
        setTimeout(() => {
            stopMouthAnimation();
            if (isLastMessage) endSession();
        }, 3000);
    }
}

function startMouthAnimation() {
    mouthVideo.play();
    mouthVideo.style.opacity = '1';
}

function stopMouthAnimation() {
    mouthVideo.pause();
    mouthVideo.style.opacity = '0';
}

// ========================================
// UI CONTROLS
// ========================================
document.getElementById('micBtn').addEventListener('click', function () {
    isMicMuted = !isMicMuted;
    updateMicButtonUI();

    const video = document.getElementById('userWebcam');
    if (video.srcObject) {
        video.srcObject.getAudioTracks().forEach(track => track.enabled = !isMicMuted);
    }

    if (isMicMuted) {
        stopListening();
        messageInput.placeholder = "Mic Muted";
    } else {
        startListening();
    }
});

function updateMicButtonUI() {
    const btn = document.getElementById('micBtn');
    if (isMicMuted) {
        btn.classList.add('muted');
        btn.style.backgroundColor = ''; // Ensure no active color when muted
        btn.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 11h-1.7c0 .74-.16 1.43-.43 2.05l1.23 1.23c.56-.98.9-2.09.9-3.28zm-4.02.17c0-.06.02-.11.02-.17V5c0-1.66-1.34-3-3-3S9 3.34 9 5v.18l5.98 5.99zM4.27 3L3 4.27l6.01 6.01V11c0 1.66 1.33 3 2.99 3 .22 0 .44-.03.65-.08l2.99 2.99c-1.08.75-2.36 1.2-3.74 1.2-3.48 0-6.3-2.82-6.3-6.3H4c0 3.91 2.86 7.17 6.67 7.93V21h2.5v-2.28c.91-.18 1.77-.52 2.55-.98l2.85 2.85 1.27-1.27L4.27 3z"/></svg>`;
    } else {
        btn.classList.remove('muted');
        btn.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>`;
    }
}

document.getElementById('cameraBtn').addEventListener('click', function () {
    this.classList.toggle('off');
    const video = document.getElementById('userWebcam');
    if (video.srcObject) {
        video.srcObject.getVideoTracks().forEach(track => track.enabled = !track.enabled);
    }
});

document.getElementById('endBtn').addEventListener('click', function () {
    if (confirm('Are you sure you want to end the session?')) {
        endSession();
    }
});

function endSession() {
    // Save conversation history to sessionStorage for review dashboard
    sessionStorage.setItem('conversationHistory', JSON.stringify(conversationHistory));

    // Save session metadata
    if (sessionData) {
        sessionStorage.setItem('sessionMetadata', JSON.stringify({
            prepType: sessionData.prep_type || 'interview',
            jobRole: sessionData.job_role || 'Candidate'
        }));
    }

    localStorage.removeItem('prepySession');
    window.location.href = 'reviewdashboard.html';
}

// ========================================
// CHAT LOGIC
// ========================================
const chatArea = document.getElementById('chatArea');
if (conversationHistory.length > 0) {
    chatArea.innerHTML = '';
    conversationHistory.forEach(msg => {
        const div = document.createElement('div');
        div.className = msg.role === 'assistant' ? 'message ai-message' : 'message user-message';
        div.innerHTML = `<p><strong>${msg.role === 'assistant' ? 'AI' : 'You'}:</strong> ${msg.content}</p>`;
        chatArea.appendChild(div);
    });
    chatArea.scrollTop = chatArea.scrollHeight;

    const lastMsg = conversationHistory[conversationHistory.length - 1];
    if (lastMsg && lastMsg.role === 'assistant') {
        speakText(lastMsg.content);
    }
}

// Timer
let seconds = 0;
setInterval(() => {
    seconds++;
    document.getElementById('timer').textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
}, 1000);

function showLoading() {
    const loaderDiv = document.createElement('div');
    loaderDiv.id = 'loader-bubble';
    loaderDiv.style.display = 'flex';
    loaderDiv.style.justifyContent = 'center'; // Center the loader
    loaderDiv.style.padding = '20px';
    loaderDiv.style.width = '100%';
    loaderDiv.innerHTML = `
        <video autoplay loop muted playsinline style="width: 250px; height: 250px; object-fit: contain; border-radius: 8px;">
            <source src="LOADER.mp4" type="video/mp4">
        </video>
    `;
    chatArea.appendChild(loaderDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function hideLoading() {
    const loader = document.getElementById('loader-bubble');
    if (loader) loader.remove();
}

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('messageInput').addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });

async function sendMessage() {
    const msg = messageInput.value.trim();
    if (!msg) return;

    stopListening();

    const div = document.createElement('div');
    div.className = 'message user-message';
    div.innerHTML = `<p><strong>You:</strong> ${msg}</p>`;
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
    messageInput.value = '';

    conversationHistory.push({ role: 'user', content: msg });
    showLoading();

    turnCount++;

    // Check if this is the last turn
    // Check if this is the last turn
    const isFinalTurn = turnCount >= MAX_TURNS;

    try {
        const res = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: msg,
                history: conversationHistory,
                system_prompt: sessionData?.system_prompt || '',
                extracted_text: sessionData?.extracted_text || '',
                is_final_turn: isFinalTurn
            })
        });

        const data = await res.json();
        hideLoading();

        if (data.success) {
            const aiDiv = document.createElement('div');
            aiDiv.className = 'message ai-message';
            aiDiv.innerHTML = `<p><strong>AI:</strong> ${data.message}</p>`;
            chatArea.appendChild(aiDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
            conversationHistory = data.history;

            speakText(data.message, turnCount >= MAX_TURNS);
        } else {
            throw new Error(data.error || 'API Error');
        }
    } catch (error) {
        hideLoading();
        const errDiv = document.createElement('div');
        errDiv.className = 'message ai-message';
        errDiv.innerHTML = `<p><strong>Error:</strong> ${error.message}</p>`;
        chatArea.appendChild(errDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
        startListening();
    }
}
