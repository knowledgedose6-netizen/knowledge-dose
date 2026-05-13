const sendBtn =
document.getElementById('sendBtn');

const userInput =
document.getElementById('userInput');

const chatMessages =
document.getElementById('chatMessages');

const typingContainer =
document.getElementById('typingContainer');

const clearChatBtn =
document.getElementById('clearChatBtn');

const quickButtons =
document.querySelectorAll('.quick-btn');

let latestAIResponse = '';

let latestAIData = {};


/* QUICK BUTTONS */

quickButtons.forEach(button=>{

    button.onclick = ()=>{

        userInput.value =
        button.dataset.prompt;

        sendMessage();
    }

});


/* SEND */

sendBtn.onclick = ()=>{

    sendMessage();

}


/* ENTER */

userInput.addEventListener(
'keypress',
function(e){

    if(e.key === 'Enter'){

        sendMessage();
    }

});


/* CLEAR CHAT */

clearChatBtn.onclick = ()=>{

    chatMessages.innerHTML = '';

}


/* SEND MESSAGE */

async function sendMessage(){

    const message =
    userInput.value.trim();

    if(message === '') return;

    addUserMessage(message);

    userInput.value = '';

    showTyping();

    try{

        const response =
        await fetch(

            '/chatbot/generate-blog/',

            {

                method:'POST',

                headers:{

                    'Content-Type':
                    'application/json',

                    'X-CSRFToken':
                    csrfToken
                },

                body:JSON.stringify({

                    prompt:message

                })

            }

        );

        const data =
        await response.json();

        hideTyping();

        latestAIResponse =
        data.content;

        latestAIData = data;

        showGeneratedImage(

            data.image_url

        );

        addAIMessage(`

<h2>${data.title}</h2>

<br>

<b>Category:</b>
${data.category}

<br><br>

<b>Meta Description:</b>

<br>

${data.meta_description}

<br><br>

<b>Tags:</b>

<br>

${data.tags}

<br><br>

${data.content}

<br><br>

<h3>FAQ</h3>

<br>

${data.faq}

<br><br>

<h3>Conclusion</h3>

<br>

${data.conclusion}

<br><br>

✅ Grammar Score:
${data.grammar_score}

<br>

🚀 SEO Score:
${data.seo_score}

<br>

🎯 Tone:
${data.tone}

        `);

        speakMessage(

            'Your AI blog has been generated successfully.'

        );

    }

    catch(error){

        hideTyping();

        addAIMessage(

            'Error generating AI response'

        );

    }

}


/* USER MESSAGE */

function addUserMessage(text){

    const div =
    document.createElement('div');

    div.className =
    'user-message';

    div.innerHTML = text;

    chatMessages.appendChild(div);

    scrollBottom();

}


/* AI MESSAGE */

function addAIMessage(text){

    const div =
    document.createElement('div');

    div.className =
    'ai-message';

    div.innerHTML =
    text.replace(/\n/g,'<br>');

    chatMessages.appendChild(div);

    scrollBottom();

}


/* IMAGE */

function showGeneratedImage(imageUrl){

    const imageContainer =
    document.getElementById(
    'imagePreviewContainer'
    );

    imageContainer.innerHTML = `

    <div class="generated-image-card">

        <img src="${imageUrl}"
        class="generated-image">

    </div>

    `;
}


/* SCROLL */

function scrollBottom(){

    chatMessages.scrollTop =
    chatMessages.scrollHeight;

}


/* TYPING */

function showTyping(){

    typingContainer.classList.remove(
    'hidden'
    );

}

function hideTyping(){

    typingContainer.classList.add(
    'hidden'
    );

}


/* SAVE DRAFT */

document.getElementById(
'saveDraftBtn'
).onclick = async ()=>{

    if(latestAIResponse === ''){

        alert(
        'Generate blog first'
        );

        return;
    }

    const response =
    await fetch(

        '/chatbot/save-draft/',

        {

            method:'POST',

            headers:{

                'Content-Type':
                'application/json',

                'X-CSRFToken':
                csrfToken

            },

            body:JSON.stringify({

                title:
                latestAIData.title,

                slug:
                latestAIData.slug,

                category:
                latestAIData.category,

                meta_description:
                latestAIData.meta_description,

                tags:
                latestAIData.tags,

                content:
                latestAIData.content,

                image_url:
                latestAIData.image_url,

                faq:
                latestAIData.faq,

                conclusion:
                latestAIData.conclusion,

                seo_score:
                latestAIData.seo_score,

                grammar_score:
                latestAIData.grammar_score,

                tone:
                latestAIData.tone

            })

        }

    );

    const data =
    await response.json();

    alert(data.message);

}


/* REWRITE */

document.getElementById(
'rewriteBtn'
).onclick = async ()=>{

    const response =
    await fetch(

        '/chatbot/rewrite-blog/',

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

    addAIMessage(data.response);

}


/* SEO */

document.getElementById(
'seoBtn'
).onclick = async ()=>{

    const response =
    await fetch(

        '/chatbot/seo-blog/',

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

    addAIMessage(data.response);

}


/* GRAMMAR */

document.getElementById(
'grammarBtn'
).onclick = async ()=>{

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

    addAIMessage(data.response);

}


/* HUMANIZE */

document.getElementById(
'humanizeBtn'
).onclick = async ()=>{

    const response =
    await fetch(

        '/chatbot/humanize-blog/',

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

    addAIMessage(data.response);

}


/* CUSTOM IMAGE */

const customImageInput =
document.getElementById(
'customImageInput'
);

customImageInput.addEventListener(
'change',
function(){

    const file =
    this.files[0];

    if(!file) return;

    if(file.size > 2000000){

        alert(
        'Image must be below 2MB'
        );

        return;
    }

    const reader =
    new FileReader();

    reader.onload = function(e){

        const imageContainer =
        document.getElementById(
        'imagePreviewContainer'
        );

        imageContainer.innerHTML = `

        <div class="generated-image-card">

            <img src="${e.target.result}"
            class="generated-image">

        </div>

        `;
    }

    reader.readAsDataURL(file);

});