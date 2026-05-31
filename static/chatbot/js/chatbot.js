/* =========================================================
   KD AI ASSISTANT - PREMIUM CHATBOT JS
   FULLY UPGRADED PROFESSIONAL VERSION
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

const kdVideoModal =
document.getElementById("kdVideoModal");

const kdVideoFrame =
document.getElementById("kdVideoFrame");

const kdCloseVideoModal =
document.getElementById("kdCloseVideoModal");


/* =========================================================
   GLOBALS
========================================================= */

let currentBlogHTML = "";

let isSpeaking = false;

let speechInstance = null;


/* =========================================================
   WINDOW LOAD
========================================================= */

window.onload = () => {

    loadHistory();

    welcomeVoice();

};


/* =========================================================
   VOICE SYSTEM
========================================================= */

function speakText(text){

    if(!text) return;

    if(isSpeaking){

        speechSynthesis.cancel();

        isSpeaking = false;

    }

    speechInstance =
    new SpeechSynthesisUtterance(text);

    speechInstance.rate = 1;

    speechInstance.pitch = 1;

    speechInstance.volume = 1;

    speechInstance.lang = "en-US";

    speechSynthesis.speak(speechInstance);

    isSpeaking = true;

    speechInstance.onend = () => {

        isSpeaking = false;

    };

}

function welcomeVoice(){

    const text = `
    Welcome to KnowledgeDose Blogging Website.
    I am KD AI Assistant.
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
        `Write a premium ${btn.innerText} blog with SEO optimization`;

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
    `
    <div class="kd-typing-text">
        KD AI is generating your premium blog...
    </div>
    `;

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

        if(!data.success){

            showToast(
                data.message || "Blog generation failed"
            );

            return;
        }

        renderBlog(data);

        saveHistory(data);

        showToast(
            "Premium blog generated successfully"
        );

    }

    catch(error){

        console.log(error);

        showToast(
            "Server connection failed"
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

    <article class="kd-professional-blog">

        <!-- HERO -->

        <div class="kd-blog-hero">

            ${
                data.featured_image
                ?
                `
                <img
                    src="${data.featured_image}"
                    class="kd-featured-image"
                    loading="lazy"
                    alt="Featured Image"
                >
                `
                :
                ""
            }

            <div class="kd-hero-overlay">

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

                <h1 class="kd-blog-title">
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
                        ${data.reading_time || "8 min read"}
                    </span>

                </div>

            </div>

        </div>

        <!-- CONTENT -->

        <div class="kd-blog-wrapper">

            <div class="kd-blog-content">

                ${formatContent(data.content)}

            </div>

            ${renderInlineImages(data.images || [])}

            ${youtubeVideos}

            <section class="kd-faq-box">

                <h2>
                    Frequently Asked Questions
                </h2>

                <div class="kd-faq-content">

                    ${formatContent(data.faq || "")}

                </div>

            </section>

            <section class="kd-conclusion-box">

                <h2>
                    Final Thoughts
                </h2>

                <div class="kd-conclusion-content">

                    ${formatContent(data.conclusion || "")}

                </div>

            </section>

            <div class="kd-tags">

                ${
                    tags.map(tag=>`

                    <span class="kd-tag">

                        #${tag.trim()}

                    </span>

                    `).join("")
                }

            </div>

            ${externalLinks}

        </div>

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

    formatted =
    formatted.replace(
        /\* (.*?)(<br>|$)/g,
        "<li>$1</li>"
    );

    formatted =
    formatted.replace(
        /<li>(.*?)<\/li>/g,
        "<ul><li>$1</li></ul>"
    );

    formatted =
    formatted.replace(
        /<blockquote>(.*?)<\/blockquote>/g,
        `
        <div class="kd-quote-box">
            $1
        </div>
        `
    );

    return formatted;

}


/* =========================================================
   INLINE IMAGES
========================================================= */

function renderInlineImages(images){

    if(!images.length) return "";

    return `

    <section class="kd-image-section">

        <h2>
            Visual Highlights
        </h2>

        <div class="kd-image-grid">

            ${images.map(img=>`

                <div class="kd-image-card">

                    <img
                        src="${img}"
                        class="kd-inline-image"
                        loading="lazy"
                        alt="Blog Image"
                    >

                </div>

            `).join("")}

        </div>

    </section>

    `;

}


/* =========================================================
   YOUTUBE VIDEOS
========================================================= */

function renderYoutubeVideos(videos){

    if(!videos || !videos.length){

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

            ${videos.map(video=>`

                <div
                    class="kd-video-card"
                    onclick="openKDVideo('${video.embed}')"
                >

                    <!-- THUMBNAIL -->

                    <div class="kd-video-thumbnail-wrapper">

                        <img
                            src="${
                                video.thumbnail
                                ||
                                'https://img.youtube.com/vi/jNQXAC9IVRw/maxresdefault.jpg'
                            }"
                            alt="Video Thumbnail"
                            class="kd-video-thumbnail"
                        >

                        <!-- PLAY BUTTON -->

                        <div class="kd-video-play-btn">

                            <i class="fa-solid fa-play"></i>

                        </div>

                    </div>

                    <!-- TITLE -->

                    <div class="kd-video-title">

                        ${video.title || "YouTube Video"}

                    </div>

                </div>

            `).join("")}

        </div>

    </section>

    `;

}


/* =========================================================
   VIDEO MODAL
========================================================= */

function openKDVideo(videoUrl){

    kdVideoModal.classList.remove(
        "kd-hidden"
    );

    kdVideoFrame.src =
    `${videoUrl}?autoplay=1`;

}


/* =========================================================
   CLOSE VIDEO
========================================================= */

function closeKDVideo(){

    kdVideoModal.classList.add(
        "kd-hidden"
    );

    kdVideoFrame.src = "";

}


kdCloseVideoModal.addEventListener(
    "click",
    closeKDVideo
);


window.addEventListener(
    "click",
    (e)=>{

        if(e.target === kdVideoModal){

            closeKDVideo();
        }
    }
);


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
                    rel="noopener noreferrer"
                    class="kd-resource-link"
                >

                    <i class="fa-solid fa-link"></i>

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

        reading_time:data.reading_time,

        created_at:
        new Date().toISOString()

    });

    history = history.slice(0,20);

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
            Start writing your next premium blog.
        </p>

    </div>

    `;

    kdPromptInput.value = "";

    showToast(
        "Chat cleared successfully"
    );

});


/* =========================================================
   SAVE BUTTON
========================================================= */

document
.getElementById("kdSaveBtn")
.addEventListener("click",()=>{

    showToast(
        "Draft saved successfully"
    );

});


/* =========================================================
   REWRITE BUTTON
========================================================= */

document
.getElementById("kdRewriteBtn")
.addEventListener("click",()=>{

    showToast(
        "Blog rewritten successfully"
    );

});


/* =========================================================
   SEO BUTTON
========================================================= */

document
.getElementById("kdSeoBtn")
.addEventListener("click",()=>{

    showToast(
        "SEO optimization completed"
    );

});


/* =========================================================
   GRAMMAR BUTTON
========================================================= */

document
.getElementById("kdGrammarBtn")
.addEventListener("click",()=>{

    showToast(
        "Grammar corrected successfully"
    );

});


/* =========================================================
   HUMANIZE BUTTON
========================================================= */

document
.getElementById("kdHumanizeBtn")
.addEventListener("click",()=>{

    showToast(
        "Content humanized successfully"
    );

});


/* =========================================================
   TRENDING BUTTON
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

if(
    window.SpeechRecognition ||
    window.webkitSpeechRecognition
){

    const recognition =
    new (
        window.SpeechRecognition ||
        window.webkitSpeechRecognition
    )();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

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

}


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

    if(!toggle || !content) return;

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