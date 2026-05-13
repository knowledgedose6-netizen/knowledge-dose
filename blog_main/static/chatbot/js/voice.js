const voiceBtn =
document.getElementById('voiceBtn');

const voiceStatus =
document.getElementById('voiceStatus');

const aiSpeakingStatus =
document.getElementById('aiSpeakingStatus');

let recognition;

let isListening = false;

if(

    'webkitSpeechRecognition'
    in window

){

    recognition =
    new webkitSpeechRecognition();

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.lang = 'en-US';

}

/* START LISTENING */

voiceBtn.onclick = ()=>{

    if(!isListening){

        startListening();

    }

    else{

        stopListening();
    }

}

function startListening(){

    isListening = true;

    voiceStatus.classList.remove(
    'hidden'
    );

    recognition.start();
}

function stopListening(){

    isListening = false;

    voiceStatus.classList.add(
    'hidden'
    );

    recognition.stop();
}

/* RESULT */

recognition.onresult = (event)=>{

    const transcript =
    event.results[0][0].transcript;

    userInput.value = transcript;

    stopListening();

    sendMessage();
}

/* END */

recognition.onend = ()=>{

    voiceStatus.classList.add(
    'hidden'
    );

    isListening = false;
}

/* ERROR */

recognition.onerror = ()=>{

    voiceStatus.classList.add(
    'hidden'
    );

    isListening = false;

    alert(
    'Microphone access denied'
    );
}

/* AI SPEAK */

function speakMessage(message){

    aiSpeakingStatus.classList.remove(
    'hidden'
    );

    const speech =
    new SpeechSynthesisUtterance();

    speech.text = message;

    speech.lang = 'en-US';

    speech.rate = 1;

    speech.pitch = 1;

    speech.volume = 1;

    speech.onend = ()=>{

        aiSpeakingStatus.classList.add(
        'hidden'
        );
    }

    window.speechSynthesis.speak(
    speech
    );
}

/* STOP SPEAKING */

function stopSpeaking(){

    window.speechSynthesis.cancel();

    aiSpeakingStatus.classList.add(
    'hidden'
    );
}

/* AI WELCOME */

window.onload = ()=>{

    setTimeout(()=>{

        speakMessage(

        'Welcome to KnowledgeDose Blogging Platform. I am KD AI. How can I help you today?'

        );

    },1500);
}