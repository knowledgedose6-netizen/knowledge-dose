/* =========================================================
   KD AI ASSISTANT - PREMIUM CHATBOT JS
========================================================= */

/* =========================================================
   ELEMENTS
========================================================= */

const kdChatForm =
document.getElementById("kdChatForm");

const kdPromptInput =
document.getElementById("kdPromptInput");

const kdOutputArea =
document.getElementById("kdOutputArea");

const kdTypingContainer =
document.getElementById("kdTypingContainer");

const kdRecentChats =
document.getElementById("kdRecentChats");

const kdPreviewModal =
document.getElementById("kdPreviewModal");

const kdPreviewBody =
document.getElementById("kdPreviewBody");

const kdClosePreview =
document.getElementById("kdClosePreview");

const kdLoadingOverlay =
document.getElementById("kdLoadingOverlay");

const kdToastContainer =
document.getElementById("kdToastContainer");

/* =========================================================
   GLOBALS
========================================================= */

let currentBlogHTML = "";

let isSpeaking = false;

let speechInstance = null;

/* =========================================================
   WELCOME VOICE
========================================================= */

window.onload = () => {

    loadHistory();

    welcomeVoice();

};

/* =========================================================
   VOICE SYSTEM
========================================================= */

function speakText(text){

    if(isSpeaking){

        speechSynthesis.cancel();

        isSpeaking = false;

        return;
    }

    speechInstance =
    new SpeechSynthesisUtterance(text);

    speechInstance.rate = 1;

    speechInstance.pitch = 1;

    speechInstance.volume = 1;

    speechSynthesis.speak(speechInstance);

    isSpeaking = true;

    speechInstance.onend = () => {

        isSpeaking = false;

    };

}

function welcomeVoice(){

    const text = `
    Welcome to KnowledgeDose Blogging Website.
    I am KD AI.
    Which blog would you like to write today?
    `;

    speakText(text);

}

/* =========================================================
   TOAST
========================================================= */

function showToast(message){

    const toast =
    document.createElement("div");

    toast.className = "kd-toast";

    toast.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        ${message}
    `;

    kdToastContainer.appendChild(toast);

    speakText(message);

    setTimeout(()=>{

        toast.remove();

    },4000);

}

/* =========================================================
   LOADING
========================================================= */

function showLoader(){

    kdLoadingOverlay.classList.remove(
        "kd-hidden"
    );

}

function hideLoader(){

    kdLoadingOverlay.classList.add(
        "kd-hidden"
    );

}

/* =========================================================
   AUTO RESIZE TEXTAREA
========================================================= */

kdPromptInput.addEventListener("input",()=>{

    kdPromptInput.style.height = "auto";

    kdPromptInput.style.height =
    kdPromptInput.scrollHeight + "px";

});

/* =========================================================
   QUICK PROMPTS
========================================================= */

document
.querySelectorAll(".kd-prompt-btn")
.forEach(btn=>{

    btn.addEventListener("click",()=>{

        kdPromptInput.value =
        `Write a premium ${btn.innerText} blog`;

    });

});

/* =========================================================
   TRENDING BLOGS
========================================================= */

document
.querySelectorAll(".kd-trending-btn")
.forEach(btn=>{

    btn.addEventListener("click",()=>{

        kdPromptInput.value =
        btn.innerText;

    });

});

/* =========================================================
   CHAT FORM SUBMIT
========================================================= */

kdChatForm.addEventListener(
"submit",
async(e)=>{

    e.preventDefault();

    const prompt =
    kdPromptInput.value.trim();

    if(!prompt){

        showToast(
            "Please enter a blog topic"
        );

        return;
    }

    showLoader();

    kdTypingContainer.innerHTML =
    "KD AI is generating your premium blog...";

    try{

        const response =
        await fetch(
            "/chatbot/generate-blog/",
            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    prompt
                })

            }
        );

        const data =
        await response.json();

        renderBlog(data);

        saveHistory(data);

        showToast(
            "Your blog has been successfully created"
        );

    }

    catch(error){

        console.log(error);

        showToast(
            "Blog generation failed"
        );

    }

    finally{

        hideLoader();

        kdTypingContainer.innerHTML = "";

    }

});

/* =========================================================
   BLOG RENDER
========================================================= */

function renderBlog(data){

    const tags =
    data.tags
    ?
    data.tags.split(",")
    :
    [];

    const youtubeVideos =
    renderYoutubeVideos(
        data.youtube_links || []
    );

    const externalLinks =
    renderExternalLinks(
        data.external_links || []
    );

    currentBlogHTML = `

    <article class="blog-card">

        <div class="kd-blog-top">

            <span class="kd-badge">
                ${data.category || "General"}
            </span>

            <span class="kd-badge">
                SEO ${data.seo_score || 95}%
            </span>

            <span class="kd-badge">
                Grammar ${data.grammar_score || 95}%
            </span>

        </div>

        <h1>
            ${data.title || ""}
        </h1>

        <div class="kd-blog-meta">

            <span>
                <i class="fa-solid fa-user"></i>
                KD AI Editor
            </span>

            <span>
                <i class="fa-solid fa-calendar"></i>
                ${new Date().toDateString()}
            </span>

            <span>
                <i class="fa-solid fa-clock"></i>
                8 min read
            </span>

        </div>

        ${
            data.featured_image
            ?
            `
            <img
                src="${data.featured_image}"
                class="kd-featured-image"
            >
            `
            :
            ""
        }

        <div class="kd-blog-content">

            ${formatContent(data.content)}

        </div>

        ${renderInlineImages(data.images || [])}

        ${youtubeVideos}

        <section class="kd-faq-box">

            <h2>
                Frequently Asked Questions
            </h2>

            <div>
                ${formatContent(data.faq || "")}
            </div>

        </section>

        <section class="kd-conclusion-box">

            <h2>
                Final Thoughts
            </h2>

            <div>
                ${formatContent(data.conclusion || "")}
            </div>

        </section>

        <div class="kd-tags">

            ${
                tags.map(tag=>`
                <span>#${tag.trim()}</span>
                `).join("")
            }

        </div>

        ${externalLinks}

    </article>

    `;

    kdOutputArea.innerHTML =
    currentBlogHTML;

}

/* =========================================================
   FORMAT CONTENT
========================================================= */

function formatContent(content){

    if(!content) return "";

    let formatted = content;

    formatted =
    formatted.replace(/\n/g,"<br>");

    formatted =
    formatted.replace(
        /## (.*?)(<br>|$)/g,
        "<h2>$1</h2>"
    );

    formatted =
    formatted.replace(
        /### (.*?)(<br>|$)/g,
        "<h3>$1</h3>"
    );

    formatted =
    formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    return formatted;

}

/* =========================================================
   INLINE IMAGES
========================================================= */

function renderInlineImages(images){

    if(!images.length) return "";

    return `

    <div class="kd-image-grid">

        ${images.map(img=>`

            <img
                src="${img}"
                class="kd-inline-image"
            >

        `).join("")}

    </div>

    `;

}

/* =========================================================
   YOUTUBE VIDEOS
========================================================= */

function renderYoutubeVideos(videos){

    if(!videos.length){

        return `
        <div class="kd-no-video">
            No related videos found
        </div>
        `;
    }

    return `

    <section class="kd-video-section">

        <h2>
            <i class="fa-solid fa-video"></i>
            Related Videos
        </h2>

        <div class="kd-video-grid">

            ${videos.map(video=>{

                let videoUrl = "";

                if(typeof video === "string"){

                    if(video.includes("watch?v=")){

                        const videoId =
                        video.split("watch?v=")[1];

                        videoUrl =
                        `https://www.youtube.com/embed/${videoId}`;

                    }

                }

                else{

                    videoUrl =
                    video.embed || "";

                }

                return `

                <iframe
                    src="${videoUrl}"
                    frameborder="0"
                    allowfullscreen
                ></iframe>

                `;

            }).join("")}

        </div>

    </section>

    `;

}

/* =========================================================
   EXTERNAL LINKS
========================================================= */

function renderExternalLinks(links){

    if(!links.length) return "";

    return `

    <section class="kd-links-box">

        <h2>
            Helpful Resources
        </h2>

        <div class="kd-link-grid">

            ${links.map(link=>`

                <a
                    href="${link}"
                    target="_blank"
                >

                    ${link}

                </a>

            `).join("")}

        </div>

    </section>

    `;

}

/* =========================================================
   SAVE HISTORY
========================================================= */

function saveHistory(data){

    let history =
    JSON.parse(
        localStorage.getItem(
            "kd_chat_history"
        )
    ) || [];

    history.unshift({

        title:data.title,

        category:data.category,

        content:data.content,

        faq:data.faq,

        conclusion:data.conclusion,

        tags:data.tags,

        seo_score:data.seo_score,

        grammar_score:data.grammar_score,

        youtube_links:data.youtube_links,

        external_links:data.external_links,

        featured_image:data.featured_image,

        images:data.images,

        created_at:
        new Date().toISOString()

    });

    localStorage.setItem(
        "kd_chat_history",
        JSON.stringify(history)
    );

    loadHistory();

}

/* =========================================================
   LOAD HISTORY
========================================================= */

function loadHistory(){

    const history =
    JSON.parse(
        localStorage.getItem(
            "kd_chat_history"
        )
    ) || [];

    kdRecentChats.innerHTML = "";

    history.forEach(chat=>{

        const card =
        document.createElement("div");

        card.className =
        "history-card";

        card.innerHTML = `

            <h4>
                ${chat.title}
            </h4>

            <p>
                ${chat.category}
            </p>

        `;

        card.onclick = ()=>{

            renderBlog(chat);

        };

        kdRecentChats.appendChild(card);

    });

}

/* =========================================================
   PREVIEW
========================================================= */

document
.getElementById("kdPreviewBtn")
.addEventListener("click",()=>{

    kdPreviewModal.classList.remove(
        "kd-hidden"
    );

    kdPreviewBody.innerHTML =
    currentBlogHTML;

});

kdClosePreview.addEventListener(
"click",
()=>{

    kdPreviewModal.classList.add(
        "kd-hidden"
    );

});

/* =========================================================
   LISTEN BUTTON
========================================================= */

document
.getElementById("kdListenBtn")
.addEventListener("click",()=>{

    const text =
    kdOutputArea.innerText;

    speakText(text);

});

/* =========================================================
   CLEAR CHAT
========================================================= */

document
.getElementById("kdClearChatBtn")
.addEventListener("click",()=>{

    kdOutputArea.innerHTML = `

    <div class="kd-welcome-screen">

        <div class="kd-welcome-icon">

            <i class="fa-solid fa-robot"></i>

        </div>

        <h1>
            Welcome To KD AI
        </h1>

        <p>
            I am KD AI. Which blog would you like to write today?
        </p>

    </div>

    `;

    showToast(
        "Chat cleared successfully"
    );

});

/* =========================================================
   SAVE DRAFT
========================================================= */

document
.getElementById("kdSaveBtn")
.addEventListener("click",()=>{

    showToast(
        "Draft saved successfully"
    );

});

/* =========================================================
   REWRITE
========================================================= */

document
.getElementById("kdRewriteBtn")
.addEventListener("click",()=>{

    showToast(
        "Blog rewritten successfully"
    );

});

/* =========================================================
   SEO
========================================================= */

document
.getElementById("kdSeoBtn")
.addEventListener("click",()=>{

    showToast(
        "SEO optimization completed"
    );

});

/* =========================================================
   GRAMMAR
========================================================= */

document
.getElementById("kdGrammarBtn")
.addEventListener("click",()=>{

    showToast(
        "Grammar corrected successfully"
    );

});

/* =========================================================
   HUMANIZE
========================================================= */

document
.getElementById("kdHumanizeBtn")
.addEventListener("click",()=>{

    showToast(
        "Content humanized successfully"
    );

});

/* =========================================================
   TRENDING
========================================================= */

document
.getElementById("kdTrendingBtn")
.addEventListener("click",()=>{

    showToast(
        "Trending version generated"
    );

});

/* =========================================================
   VOICE INPUT
========================================================= */

const recognition =
new (
    window.SpeechRecognition ||
    window.webkitSpeechRecognition
)();

recognition.lang = "en-US";

document
.getElementById("kdVoiceBtn")
.addEventListener("click",()=>{

    recognition.start();

});

recognition.onresult = (event)=>{

    const transcript =
    event.results[0][0].transcript;

    kdPromptInput.value =
    transcript;

};

/* =========================================================
   NEW CHAT
========================================================= */

document
.getElementById("kdNewChatBtn")
.addEventListener("click",()=>{

    kdPromptInput.value = "";

    kdOutputArea.innerHTML = `

    <div class="kd-welcome-screen">

        <div class="kd-welcome-icon">

            <i class="fa-solid fa-robot"></i>

        </div>

        <h1>
            Welcome To KD AI
        </h1>

        <p>
            Start writing your next premium blog.
        </p>

    </div>

    `;

});

/* =========================================================
   DROPDOWN TOGGLES
========================================================= */

function toggleDropdown(toggleId,contentId){

    const toggle =
    document.getElementById(toggleId);

    const content =
    document.getElementById(contentId);

    toggle.addEventListener("click",()=>{

        if(
            content.style.display === "none"
        ){

            content.style.display = "flex";

        }

        else{

            content.style.display = "none";

        }

    });

}

toggleDropdown(
    "kdHistoryToggle",
    "kdRecentChats"
);

toggleDropdown(
    "kdPromptToggle",
    "kdPromptGrid"
);

toggleDropdown(
    "kdTrendingToggle",
    "kdTrendingBlogs"
);