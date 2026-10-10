/* ========================================================
   J.A.R.V.I.S. // STARK INDUSTRIES SYSTEM CLIENT JAVASCRIPT
   Handles Speech Recognition, Web Audio Visualizer, 
   OS Telemetry Polling, Arc Reactor Animations & Power State.
   ======================================================== */

let isSystemActive = true;
let isMicActive = true;
let isSpeaking = false;
let recognition = null;
let audioContext = null;
let analyser = null;
let currentAudio = null;

// DOM Elements
const arcReactor = document.getElementById('arcReactor');
const systemStateText = document.getElementById('systemStateText');
const coreLabel = document.getElementById('coreLabel');
const coreSubtext = document.getElementById('coreSubtext');
const voiceStatusText = document.getElementById('voiceStatusText');
const transcriptDisplay = document.getElementById('transcriptDisplay');
const logStream = document.getElementById('logStream');
const hudClock = document.getElementById('hudClock');
const hudDate = document.getElementById('hudDate');
const cpuVal = document.getElementById('cpuVal');
const cpuBar = document.getElementById('cpuBar');
const ramVal = document.getElementById('ramVal');
const ramBar = document.getElementById('ramBar');
const diskVal = document.getElementById('diskVal');
const diskBar = document.getElementById('diskBar');
const batVal = document.getElementById('batVal');
const batBar = document.getElementById('batBar');
const togglePowerBtn = document.getElementById('togglePowerBtn');
const micToggleBtn = document.getElementById('micToggleBtn');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettingsBtn = document.getElementById('closeSettingsBtn');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const commandForm = document.getElementById('commandForm');
const commandInput = document.getElementById('commandInput');
const clearLogsBtn = document.getElementById('clearLogsBtn');

// ================= 1. CLOCK & TELEMETRY =================

function updateClock() {
    const now = new Date();
    hudClock.textContent = now.toLocaleTimeString([], { hour12: true });
    hudDate.textContent = now.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }).toUpperCase();
}
setInterval(updateClock, 1000);
updateClock();

async function pollTelemetry() {
    try {
        const res = await fetch('/api/telemetry');
        if (res.ok) {
            const data = await res.json();
            cpuVal.textContent = `${data.cpu_percent}%`;
            cpuBar.style.width = `${data.cpu_percent}%`;

            ramVal.textContent = `${data.ram_used_gb} / ${data.ram_total_gb} GB`;
            ramBar.style.width = `${data.ram_percent}%`;

            diskVal.textContent = `${data.disk_percent}%`;
            diskBar.style.width = `${data.disk_percent}%`;

            batVal.textContent = `${data.battery_percent}%${data.battery_charging ? ' ⚡' : ''}`;
            batBar.style.width = `${data.battery_percent}%`;
        }
    } catch (e) {
        console.warn("Telemetry fetch error:", e);
    }
}
setInterval(pollTelemetry, 2500);
pollTelemetry();

// ================= 2. RADAR CANVAS ANIMATION =================

const radarCanvas = document.getElementById('radarCanvas');
const radarCtx = radarCanvas.getContext('2d');
let radarAngle = 0;

function drawRadar() {
    const w = radarCanvas.width;
    const h = radarCanvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const r = Math.min(cx, cy) - 10;

    radarCtx.clearRect(0, 0, w, h);

    // Draw concentric rings
    radarCtx.strokeStyle = 'rgba(0, 240, 255, 0.25)';
    radarCtx.lineWidth = 1;
    for (let i = 1; i <= 3; i++) {
        radarCtx.beginPath();
        radarCtx.arc(cx, cy, (r / 3) * i, 0, Math.PI * 2);
        radarCtx.stroke();
    }

    // Crosshairs
    radarCtx.beginPath();
    radarCtx.moveTo(cx - r, cy);
    radarCtx.lineTo(cx + r, cy);
    radarCtx.moveTo(cx, cy - r);
    radarCtx.lineTo(cx, cy + r);
    radarCtx.stroke();

    if (isSystemActive) {
        // Rotating radar beam
        radarAngle += 0.04;
        radarCtx.save();
        radarCtx.translate(cx, cy);
        radarCtx.rotate(radarAngle);
        
        const grad = radarCtx.createRadialGradient(0, 0, 0, 0, 0, r);
        grad.addColorStop(0, 'rgba(0, 240, 255, 0.4)');
        grad.addColorStop(1, 'rgba(0, 240, 255, 0.0)');

        radarCtx.fillStyle = grad;
        radarCtx.beginPath();
        radarCtx.moveTo(0, 0);
        radarCtx.arc(0, 0, r, 0, Math.PI / 4);
        radarCtx.closePath();
        radarCtx.fill();
        radarCtx.restore();
    }

    requestAnimationFrame(drawRadar);
}
drawRadar();

// ================= 3. AUDIO VISUALIZER FOR ARC REACTOR =================

const visualizerCanvas = document.getElementById('visualizerCanvas');
const vCtx = visualizerCanvas.getContext('2d');

function initAudioContext() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 128;
    }
    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }
}

function drawVisualizer() {
    const w = visualizerCanvas.width;
    const h = visualizerCanvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const baseRadius = 135;

    vCtx.clearRect(0, 0, w, h);

    if (analyser && (isSpeaking || isMicActive)) {
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        analyser.getByteFrequencyData(dataArray);

        // Circular frequency wave around Arc Reactor
        const numBars = 48;
        const step = (Math.PI * 2) / numBars;

        for (let i = 0; i < numBars; i++) {
            const dataIndex = Math.floor((i / numBars) * (bufferLength / 2));
            const barHeight = isSpeaking ? (dataArray[dataIndex] / 255) * 60 : 4;

            const angle = i * step;
            const x1 = cx + Math.cos(angle) * baseRadius;
            const y1 = cy + Math.sin(angle) * baseRadius;
            const x2 = cx + Math.cos(angle) * (baseRadius + barHeight + 4);
            const y2 = cy + Math.sin(angle) * (baseRadius + barHeight + 4);

            vCtx.strokeStyle = isSpeaking ? 'rgba(0, 240, 255, 0.85)' : 'rgba(0, 240, 255, 0.2)';
            vCtx.lineWidth = 3;
            vCtx.shadowBlur = isSpeaking ? 12 : 0;
            vCtx.shadowColor = '#00f0ff';
            
            vCtx.beginPath();
            vCtx.moveTo(x1, y1);
            vCtx.lineTo(x2, y2);
            vCtx.stroke();
        }
    }

    requestAnimationFrame(drawVisualizer);
}
drawVisualizer();

// ================= 4. AUDIO PLAYBACK WITH LIP-SYNC =================

function playJarvisSpeech(audioUrl) {
    if (!audioUrl) return;
    initAudioContext();

    if (currentAudio) {
        currentAudio.pause();
    }

    currentAudio = new Audio(audioUrl);
    const source = audioContext.createMediaElementSource(currentAudio);
    source.connect(analyser);
    analyser.connect(audioContext.destination);

    isSpeaking = true;
    document.body.classList.add('speaking');
    voiceStatusText.textContent = "Speaking...";

    currentAudio.onended = () => {
        isSpeaking = false;
        document.body.classList.remove('speaking');
        voiceStatusText.textContent = isSystemActive ? "Listening for 'Jarvis'..." : "Standby Mode";
    };

    currentAudio.onerror = (e) => {
        console.warn("Audio playback error:", e);
        isSpeaking = false;
        document.body.classList.remove('speaking');
    };

    currentAudio.play().catch(err => {
        console.warn("Autoplay restriction:", err);
    });
}

// ================= 5. REAL-TIME SPEECH RECOGNITION =================

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        transcriptDisplay.textContent = "Voice recognition not supported by browser. Use Chrome/Edge or manual input.";
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        if (isSystemActive && isMicActive) {
            voiceStatusText.textContent = "Listening for 'Jarvis'...";
        }
    };

    recognition.onresult = (event) => {
        if (!isSystemActive || !isMicActive || isSpeaking) return;

        let interim = '';
        let final = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final += event.results[i][0].transcript;
            } else {
                interim += event.results[i][0].transcript;
            }
        }

        if (interim) {
            transcriptDisplay.textContent = `"${interim.trim()}..."`;
            // Animate input meter
            animateMicBars();
        }

        if (final) {
            const cleanFinal = final.trim();
            transcriptDisplay.textContent = `"${cleanFinal}"`;
            handleRecognizedCommand(cleanFinal);
        }
    };

    recognition.onerror = (event) => {
        if (event.error !== 'no-speech') {
            console.warn("Speech error:", event.error);
        }
    };

    recognition.onend = () => {
        // Automatically restart listening if still online
        if (isSystemActive && isMicActive) {
            try {
                recognition.start();
            } catch (e) {}
        }
    };

    try {
        recognition.start();
    } catch (e) {
        console.warn("Recognition start error:", e);
    }
}

function animateMicBars() {
    const bars = document.querySelectorAll('#audioBars span');
    bars.forEach(bar => {
        const h = Math.floor(Math.random() * 14) + 4;
        bar.style.height = `${h}px`;
    });
    setTimeout(() => {
        bars.forEach(bar => bar.style.height = '4px');
    }, 200);
}

// ================= 6. COMMAND EXECUTION =================

async function handleRecognizedCommand(text) {
    if (!isSystemActive) return;

    // Filter out accidental background noise if it doesn't mention jarvis
    const lower = text.toLowerCase();
    const hasWakeWord = lower.includes("jarvis") || lower.startsWith("hey") || lower.startsWith("ok") || lower.startsWith("open") || lower.startsWith("play") || lower.startsWith("volume") || lower.startsWith("status");

    if (!hasWakeWord && text.split(" ").length < 2) {
        return; // Ignore random one-word background sounds
    }

    addLogEntry('user', text);
    voiceStatusText.textContent = "Processing protocol...";

    try {
        const res = await fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await res.json();
        if (data.speech) {
            addLogEntry('jarvis', data.speech, data.action);
            transcriptDisplay.textContent = `JARVIS: "${data.speech}"`;
            if (data.audio_url) {
                playJarvisSpeech(data.audio_url);
            }
        }
    } catch (err) {
        console.error("Command execution error:", err);
        addLogEntry('jarvis', "Communication uplink disrupted, sir.");
    }
}

function addLogEntry(author, text, action = null) {
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const entry = document.createElement('div');
    entry.className = `log-entry ${author}`;

    let actionBadge = action ? `<span style="color:#00f0ff;font-size:0.65rem;border:1px solid #00f0ff;padding:1px 4px;border-radius:2px;margin-left:6px;">${action.toUpperCase()}</span>` : '';

    entry.innerHTML = `
        <div class="log-meta">
            <span class="log-author">${author === 'user' ? 'STARK' : 'J.A.R.V.I.S.'} ${actionBadge}</span>
            <span class="log-time">${now}</span>
        </div>
        <div class="log-text">${text}</div>
    `;

    logStream.appendChild(entry);
    logStream.scrollTop = logStream.scrollHeight;
}

// Preset Quick Command Trigger
function triggerPreset(cmd) {
    transcriptDisplay.textContent = `"${cmd}"`;
    handleRecognizedCommand(cmd);
}

// ================= 7. POWER & SYSTEM STATE TOGGLE =================

async function togglePower() {
    isSystemActive = !isSystemActive;
    
    // Notify backend
    try {
        const res = await fetch('/api/toggle_state', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_active: isSystemActive })
        });
        const data = await res.json();
        if (data.audio_url && isSystemActive) {
            playJarvisSpeech(data.audio_url);
        }
    } catch (e) {}

    if (isSystemActive) {
        document.body.classList.remove('standby');
        systemStateText.textContent = "ONLINE // LISTENING";
        coreLabel.textContent = "ARC REACTOR: ACTIVE";
        coreSubtext.textContent = "Continuous Voice Detection Engaged";
        togglePowerBtn.textContent = "POWER: ONLINE";
        togglePowerBtn.style.borderColor = "var(--hud-cyan)";
        voiceStatusText.textContent = "Listening for 'Jarvis'...";
        transcriptDisplay.textContent = "Standing by for voice instruction...";
        if (recognition) {
            try { recognition.start(); } catch (e) {}
        }
    } else {
        document.body.classList.add('standby');
        systemStateText.textContent = "STANDBY // SLEEP";
        coreLabel.textContent = "ARC REACTOR: STANDBY";
        coreSubtext.textContent = "Power Conserved - Mic Disabled";
        togglePowerBtn.textContent = "POWER: STANDBY";
        togglePowerBtn.style.borderColor = "var(--hud-gold)";
        voiceStatusText.textContent = "Standby Mode Active";
        transcriptDisplay.textContent = "JARVIS is sleeping. Click Arc Reactor to engage.";
        if (recognition) {
            try { recognition.stop(); } catch (e) {}
        }
    }
}

arcReactor.addEventListener('click', togglePower);
togglePowerBtn.addEventListener('click', togglePower);

micToggleBtn.addEventListener('click', () => {
    isMicActive = !isMicActive;
    if (isMicActive) {
        micToggleBtn.textContent = "MIC: ACTIVE";
        micToggleBtn.style.borderColor = "var(--hud-cyan)";
        if (recognition && isSystemActive) {
            try { recognition.start(); } catch(e) {}
        }
    } else {
        micToggleBtn.textContent = "MIC: MUTED";
        micToggleBtn.style.borderColor = "var(--hud-red)";
        if (recognition) {
            try { recognition.stop(); } catch(e) {}
        }
    }
});

// Manual Text Submit
commandForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const val = commandInput.value.trim();
    if (val) {
        handleRecognizedCommand(val);
        commandInput.value = '';
    }
});

clearLogsBtn.addEventListener('click', () => {
    logStream.innerHTML = '';
});

// ================= 8. SETTINGS MODAL =================

settingsBtn.addEventListener('click', async () => {
    try {
        const res = await fetch('/api/settings');
        const data = await res.json();
        if (data.settings) {
            document.getElementById('geminiApiKeyInput').value = data.settings.gemini_api_key || '';
            document.getElementById('userNameInput').value = data.settings.user_name || 'Sir';
            document.getElementById('voiceRateSelect').value = data.settings.voice_speed || '+0%';
        }
    } catch(e) {}
    settingsModal.classList.add('open');
});

closeSettingsBtn.addEventListener('click', () => {
    settingsModal.classList.remove('open');
});

saveSettingsBtn.addEventListener('click', async () => {
    const payload = {
        gemini_api_key: document.getElementById('geminiApiKeyInput').value.trim(),
        user_name: document.getElementById('userNameInput').value.trim(),
        voice_speed: document.getElementById('voiceRateSelect').value
    };

    try {
        await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        settingsModal.classList.remove('open');
        addLogEntry('jarvis', "System settings and protocols updated, sir.");
    } catch(e) {
        alert("Failed to save settings.");
    }
});

// Startup Initialization
window.addEventListener('DOMContentLoaded', () => {
    initSpeechRecognition();
    // Pre-cache introductory audio
    fetch('/api/status').then(r => r.json()).then(st => {
        if (!st.is_active) {
            togglePower();
        }
    });
});
