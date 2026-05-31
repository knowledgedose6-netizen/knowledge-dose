/* ================= KD AI TYPING SYSTEM ================= */

console.log(
'⌨️ Typing animation system loaded'
);


/* ================= ELEMENTS ================= */

const typingContainer =
document.getElementById(
'typingContainer'
);

const chatMessages =
document.getElementById(
'chatMessages'
);


/* ================= SHOW TYPING ================= */

function showTyping(){

    if(!typingContainer) return;

    typingContainer.classList.remove(
        'hidden'
    );

    typingContainer.innerHTML = `

        <div class="typing-wrapper">

            <div class="typing-dots">

                <span></span>
                <span></span>
                <span></span>

            </div>

            <div class="typing-text">

                🤖 KD AI is generating a
                professional blog...

            </div>

        </div>

    `;

    scrollTypingBottom();

}


/* ================= HIDE TYPING ================= */

function hideTyping(){

    if(!typingContainer) return;

    typingContainer.classList.add(
        'hidden'
    );

}


/* ================= ADVANCED AI TYPING ================= */

function typeWriterEffect(

    element,

    html,

    speed = 2

){

    let index = 0;

    const interval = setInterval(()=>{

        element.innerHTML =

        html.substring(
            0,
            index
        );

        index++;

        scrollTypingBottom();

        if(index > html.length){

            clearInterval(
                interval
            );

        }

    },speed);

}


/* ================= SCROLL ================= */

function scrollTypingBottom(){

    if(chatMessages){

        chatMessages.scrollTop =

        chatMessages.scrollHeight;

    }

}


/* ================= LOADING STATES ================= */

function showAIThinking(){

    if(!typingContainer) return;

    typingContainer.classList.remove(
        'hidden'
    );

    typingContainer.innerHTML = `

        <div class="thinking-box">

            <div class="thinking-icon">

                🧠

            </div>

            <div class="thinking-text">

                KD AI is analyzing your
                request intelligently...

            </div>

        </div>

    `;

}


function showImageLoading(){

    if(!typingContainer) return;

    typingContainer.classList.remove(
        'hidden'
    );

    typingContainer.innerHTML = `

        <div class="thinking-box">

            <div class="thinking-icon">

                🖼

            </div>

            <div class="thinking-text">

                Generating premium AI images...

            </div>

        </div>

    `;

}


/* ================= SUCCESS MESSAGE ================= */

function showTypingSuccess(){

    if(!typingContainer) return;

    typingContainer.classList.remove(
        'hidden'
    );

    typingContainer.innerHTML = `

        <div class="success-box">

            ✅ Blog generated successfully

        </div>

    `;

    setTimeout(()=>{

        hideTyping();

    },1500);

}


/* ================= ERROR MESSAGE ================= */

function showTypingError(message='Something went wrong'){

    if(!typingContainer) return;

    typingContainer.classList.remove(
        'hidden'
    );

    typingContainer.innerHTML = `

        <div class="error-box">

            ❌ ${message}

        </div>

    `;

    setTimeout(()=>{

        hideTyping();

    },2500);

}


/* ================= SUCCESS LOG ================= */

console.log(
'🚀 KD AI Typing System Ready'
);