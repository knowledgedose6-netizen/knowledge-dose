/* ================= KD AI GRAMMAR SYSTEM ================= */

console.log(
'✅ Grammar system loaded successfully'
);


/* ================= ELEMENTS ================= */

const grammarBtn =
document.getElementById(
'grammarBtn'
);

const chatMessages =
document.getElementById(
'chatMessages'
);


/* ================= LOADER ================= */

function showGrammarLoader(){

    const loader = document.createElement(
        'div'
    );

    loader.className =
    'ai-message grammar-loader';

    loader.id =
    'grammarLoader';

    loader.innerHTML = `

        <div class="typing-dots">

            <span></span>
            <span></span>
            <span></span>

        </div>

        <p>

            📝 KD AI is fixing grammar...

        </p>

    `;

    chatMessages.appendChild(
        loader
    );

    scrollBottom();

}


/* ================= REMOVE LOADER ================= */

function removeGrammarLoader(){

    const loader =
    document.getElementById(
    'grammarLoader'
    );

    if(loader){

        loader.remove();

    }

}


/* ================= GRAMMAR FIX ================= */

async function fixGrammar(){

    try{

        if(

            latestAIResponse === ''

        ){

            alert(
            'Generate blog first'
            );

            return;

        }

        showGrammarLoader();

        const response =
        await fetch(

            '/chatbot/grammar-blog/',

            {

                method:'POST',

                headers:{

                    'Content-Type':
                    'application/json',

                    'X-CSRFToken':
                    csrfToken

                },

                body:JSON.stringify({

                    content:
                    latestAIResponse

                })

            }

        );

        const data =
        await response.json();

        removeGrammarLoader();

        if(data.response){

            latestAIResponse =
            data.response;

            addAIMessage(`

                <div class="grammar-result">

                    <h2>

                        📝 Grammar Corrected

                    </h2>

                    <div class="grammar-content">

                        ${data.response}

                    </div>

                </div>

            `);

            speakNotification(
                'Grammar correction completed'
            );

        }

        else{

            addAIMessage(`

                <div class="error-message">

                    ❌ Grammar correction failed

                </div>

            `);

        }

    }

    catch(error){

        console.log(
        error
        );

        removeGrammarLoader();

        addAIMessage(`

            <div class="error-message">

                ❌ Grammar system error

            </div>

        `);

    }

}


/* ================= BUTTON EVENT ================= */

if(grammarBtn){

    grammarBtn.onclick = ()=>{

        fixGrammar();

    };

}


/* ================= AI VOICE NOTIFICATION ================= */

function speakNotification(message){

    try{

        const speech =
        new SpeechSynthesisUtterance(
            message
        );

        speech.lang = 'en-US';

        speech.rate = 1;

        speech.pitch = 1;

        window.speechSynthesis.speak(
            speech
        );

    }

    catch(error){

        console.log(
        'Voice notification failed'
        );

    }

}


/* ================= SCROLL ================= */

function scrollBottom(){

    if(chatMessages){

        chatMessages.scrollTop =

        chatMessages.scrollHeight;

    }

}


/* ================= SUCCESS LOG ================= */

console.log(
'🚀 KD AI Grammar Module Ready'
);