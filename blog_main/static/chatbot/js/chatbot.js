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


/* SEND BUTTON */

sendBtn.onclick = ()=>{

    sendMessage();

}


/* ENTER KEY */

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

        latestAIData =
        data;

        addAIMessage(`

<div class="ai-blog-card">

    <!-- TITLE -->

    <div class="ai-blog-header">

        <h1>${data.title}</h1>

        <div class="ai-meta">

            <span>
                📂 ${data.category}
            </span>

            <span>
                🚀 SEO:
                ${data.seo_score}
            </span>

            <span>
                ✅ Grammar:
                ${data.grammar_score}
            </span>

            <span>
                🎯 ${data.tone}
            </span>

        </div>

    </div>


    <!-- META DESCRIPTION -->

    <div class="ai-blog-description">

        <h3>
            📌 Meta Description
        </h3>

        <p>
            ${data.meta_description}
        </p>

    </div>


    <!-- TAGS -->

    <div class="ai-blog-tags">

        <h3>
            🏷 Tags
        </h3>

        <p>
            ${data.tags}
        </p>

    </div>


    <!-- IMAGE -->

    <div class="generated-image-card">

        <img src="${data.image_url}"
        class="generated-image">

    </div>


    <!-- BLOG CONTENT -->

    <div class="ai-blog-content-wrapper">

        <div class="ai-blog-content">

            ${data.content.replace(/\n/g,'<br>')}

        </div>

    </div>


    <!-- FAQ -->

    <div class="ai-blog-faq">

        <h2>
            ❓ FAQs
        </h2>

        <p>
            ${data.faq}
        </p>

    </div>


    <!-- CONCLUSION -->

    <div class="ai-blog-conclusion">

        <h2>
            📌 Conclusion
        </h2>

        <p>
            ${data.conclusion}
        </p>

    </div>

</div>

        `);

        speakMessage(

            'Your AI blog has been generated successfully.'

        );

    }

    catch(error){

        hideTyping();

        addAIMessage(

            '❌ Error generating AI response'

        );

    }

}


/* USER MESSAGE */

function addUserMessage(text){

    const div =
    document.createElement('div');

    div.className =
    'user-message';

    div.innerHTML =
    text;

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
    text;

    chatMessages.appendChild(div);

    scrollBottom();

}


/* UPDATE BLOG CONTENT */

function updateBlogContent(newContent){

    const blogContent = document.querySelector(
        '.ai-blog-content'
    );

    if(blogContent){

        blogContent.innerHTML =
        newContent.replace(/\n/g,'<br>');

        latestAIResponse =
        newContent;
    }

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
                latestAIResponse,

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

    updateBlogContent(data.response);

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

    updateBlogContent(data.response);

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

    updateBlogContent(data.response);

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

    updateBlogContent(data.response);

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

        const image =
        document.querySelector(
        '.generated-image'
        );

        if(image){

            image.src =
            e.target.result;
        }

    }

    reader.readAsDataURL(file);

});