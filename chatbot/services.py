# =========================================================
# KD AI ASSISTANT - services.py
# FULLY UPGRADED ULTRA PREMIUM VERSION
# YOUTUBE ERROR 153 FIXED VERSION
# =========================================================

import requests
import random
import re

from django.conf import settings


# =========================================================
# API KEYS
# =========================================================

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

WEB_SEARCH_API_KEY = settings.WEB_SEARCH_API_KEY

GNEWS_API_KEY = settings.GNEWS_API_KEY


# =========================================================
# CLEAN QUERY
# =========================================================

def clean_query(query):

    if not query:

        return "technology"

    query = str(query).strip()

    query = re.sub(

        r'[^a-zA-Z0-9\s]',

        '',

        query

    )

    return query[:100]


# =========================================================
# SMART VIDEO QUERY
# =========================================================

def build_video_query(query):

    query = clean_query(query)

    blocked_words = [

        "write",
        "premium",
        "blog",
        "article",
        "seo",
        "optimized",
        "generate"

    ]

    words = query.split()

    final_words = [

        word for word in words
        if word.lower() not in blocked_words

    ]

    optimized_query = " ".join(final_words)

    optimized_query += " tutorial guide"

    return optimized_query


# =========================================================
# YOUTUBE SEARCH API
# =========================================================

def get_youtube_videos(

    query,

    max_results=4

):

    try:

        optimized_query = (

            build_video_query(query)

        )

        search_url = (

            "https://www.googleapis.com/youtube/v3/search"

        )

        params = {

            "part":"snippet",

            "q":optimized_query,

            "key":YOUTUBE_API_KEY,

            "maxResults":15,

            "type":"video",

            "videoEmbeddable":"true",

            "videoSyndicated":"true",

            "safeSearch":"strict",

            "relevanceLanguage":"en",

            "videoDuration":"medium",

            "order":"viewCount"

        }

        response = requests.get(

            search_url,

            params=params,

            timeout=20

        )

        data = response.json()

        items = data.get(

            "items",

            []

        )

        videos = []

        used_ids = set()

        blocked_keywords = [

            "shorts",
            "live",
            "music",
            "song",
            "movie",
            "trailer",
            "gaming",
            "tiktok",
            "tedx",
            "podcast",
            "news",
            "reaction",
            "stream",
            "radio"

        ]

        for item in items:

            video_id = (

                item

                .get("id", {})

                .get("videoId")

            )

            snippet = item.get(

                "snippet",

                {}

            )

            title = snippet.get(

                "title",

                ""

            )

            if not video_id:

                continue

            if video_id in used_ids:

                continue

            lower_title = title.lower()

            blocked = any(

                keyword in lower_title
                for keyword in blocked_keywords

            )

            if blocked:

                continue

            # =================================================
            # SAFE EMBED URL
            # =================================================

            embed_url = (

                f"https://www.youtube-nocookie.com/embed/{video_id}"

            )

            # =================================================
            # SAFE THUMBNAIL
            # =================================================

            thumbnail = (

                snippet.get(
                    "thumbnails",
                    {}
                )
                .get(
                    "high",
                    {}
                )
                .get(
                    "url"
                )

                or

                snippet.get(
                    "thumbnails",
                    {}
                )
                .get(
                    "medium",
                    {}
                )
                .get(
                    "url"
                )

                or

                snippet.get(
                    "thumbnails",
                    {}
                )
                .get(
                    "default",
                    {}
                )
                .get(
                    "url",
                    f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                )

            )

            videos.append({

                "title":title,

                "embed":embed_url,

                "thumbnail":thumbnail

            })

            used_ids.add(video_id)

            if len(videos) >= max_results:

                break

        # =================================================
        # FALLBACK
        # =================================================

        if not videos:

            return fallback_videos(query)

        return videos

    except Exception as e:

        print(

            "YOUTUBE ERROR:",

            e

        )

        return fallback_videos(query)


# =========================================================
# FALLBACK VIDEOS
# =========================================================

def fallback_videos(query="technology"):

    query = query.lower()

    if "food" in query:

        return [

            {

                "title":
                "Best Street Food Guide",

                "embed":
                "https://www.youtube-nocookie.com/embed/MdDofqo8QWQ",

                "thumbnail":
                "https://img.youtube.com/vi/MdDofqo8QWQ/hqdefault.jpg"

            },

            {

                "title":
                "Delicious Food Recipes",

                "embed":
                "https://www.youtube-nocookie.com/embed/1APwq1df6Mw",

                "thumbnail":
                "https://img.youtube.com/vi/1APwq1df6Mw/hqdefault.jpg"

            }

        ]

    elif "fashion" in query:

        return [

            {

                "title":
                "Modern Fashion Trends",

                "embed":
                "https://www.youtube-nocookie.com/embed/mJgBOIoGihA",

                "thumbnail":
                "https://img.youtube.com/vi/mJgBOIoGihA/hqdefault.jpg"

            },

            {

                "title":
                "Fashion Styling Tips",

                "embed":
                "https://www.youtube-nocookie.com/embed/6_b7RDuLwcI",

                "thumbnail":
                "https://img.youtube.com/vi/6_b7RDuLwcI/hqdefault.jpg"

            }

        ]

    elif "technology" in query or "ai" in query:

        return [

            {

                "title":
                "Latest AI Technology",

                "embed":
                "https://www.youtube-nocookie.com/embed/jNQXAC9IVRw",

                "thumbnail":
                "https://img.youtube.com/vi/jNQXAC9IVRw/hqdefault.jpg"

            },

            {

                "title":
                "Future Technology Guide",

                "embed":
                "https://www.youtube-nocookie.com/embed/ysz5S6PUM-U",

                "thumbnail":
                "https://img.youtube.com/vi/ysz5S6PUM-U/hqdefault.jpg"

            }

        ]

    return [

        {

            "title":
            "KnowledgeDose Premium Guide",

            "embed":
            "https://www.youtube-nocookie.com/embed/jNQXAC9IVRw",

            "thumbnail":
            "https://img.youtube.com/vi/jNQXAC9IVRw/hqdefault.jpg"

        }

    ]


# =========================================================
# GNEWS TRENDING
# =========================================================

def get_trending_news(query="technology"):

    try:

        query = clean_query(query)

        url = "https://gnews.io/api/v4/search"

        params = {

            "q":query,

            "lang":"en",

            "country":"pk",

            "max":8,

            "apikey":
            GNEWS_API_KEY

        }

        response = requests.get(

            url,

            params=params,

            timeout=20

        )

        data = response.json()

        articles = data.get(

            "articles",

            []

        )

        trending_news = []

        for article in articles:

            image = article.get(

                "image",

                ""

            )

            if not image:

                continue

            trending_news.append({

                "title":
                article.get(
                    "title",
                    ""
                ),

                "description":
                article.get(
                    "description",
                    ""
                ),

                "url":
                article.get(
                    "url",
                    ""
                ),

                "image":image,

                "published_at":
                article.get(
                    "publishedAt",
                    ""
                )

            })

        return trending_news

    except Exception as e:

        print(

            "GNEWS ERROR:",

            e

        )

        return []


# =========================================================
# WEB SEARCH
# =========================================================

def web_search(query):

    try:

        query = clean_query(query)

        url = "https://google.serper.dev/search"

        headers = {

            "X-API-KEY":
            WEB_SEARCH_API_KEY,

            "Content-Type":
            "application/json"

        }

        payload = {

            "q":query

        }

        response = requests.post(

            url,

            headers=headers,

            json=payload,

            timeout=20

        )

        data = response.json()

        results = data.get(

            "organic",

            []

        )

        final_results = []

        used_links = set()

        for item in results[:10]:

            link = item.get(

                "link",

                ""

            )

            if not link:

                continue

            if link in used_links:

                continue

            final_results.append({

                "title":
                item.get(
                    "title",
                    ""
                ),

                "link":link,

                "snippet":
                item.get(
                    "snippet",
                    ""
                )

            })

            used_links.add(link)

        return final_results[:5]

    except Exception as e:

        print(

            "WEB SEARCH ERROR:",

            e

        )

        return []


# =========================================================
# TRENDING TOPICS
# =========================================================

def get_trending_topics():

    return [

        "Best AI Tools",

        "Future of Artificial Intelligence",

        "Technology News",

        "Digital Marketing Trends",

        "Business Growth Strategies",

        "Remote Freelancing Trends",

        "Startup Growth",

        "Online Learning Ideas",

        "Nature and Mental Health",

        "AI Automation Systems",

        "Future Technology Innovations",

        "Cybersecurity Trends",

        "Passive Income Ideas",

        "Modern Education Systems",

        "Social Media Growth",

        "Smart Productivity Hacks"

    ]


# =========================================================
# SEO KEYWORDS
# =========================================================

def generate_keywords(title):

    title = clean_query(title)

    words = title.split()

    keywords = []

    for word in words:

        if len(word) > 3:

            keywords.append(
                word.lower()
            )

    keywords.extend([

        "AI",
        "Technology",
        "KnowledgeDose",
        "Trending"

    ])

    return list(
        set(keywords)
    )


# =========================================================
# RELATED BLOG LINKS
# =========================================================

def generate_related_links(category):

    related = {

        "AI":[

            "https://openai.com",

            "https://huggingface.co",

            "https://deepmind.google"

        ],

        "Technology":[

            "https://techcrunch.com",

            "https://www.theverge.com"

        ],

        "Business":[

            "https://forbes.com",

            "https://entrepreneur.com"

        ],

        "Education":[

            "https://coursera.org",

            "https://edx.org"

        ],

        "Food":[

            "https://foodnetwork.com",

            "https://allrecipes.com"

        ],

        "Fashion":[

            "https://vogue.com",

            "https://elle.com"

        ]

    }

    return related.get(

        category,

        [
            "https://google.com"
        ]

    )


# =========================================================
# ESTIMATED READING TIME
# =========================================================

def calculate_reading_time(content):

    try:

        word_count = len(
            content.split()
        )

        minutes = max(

            1,

            round(word_count / 200)

        )

        return f"{minutes} min read"

    except Exception:

        return "5 min read"


# =========================================================
# BLOG META DATA
# =========================================================

def generate_blog_meta(

    title,

    category,

    content

):

    return {

        "reading_time":
        calculate_reading_time(
            content
        ),

        "keywords":
        generate_keywords(
            title
        ),

        "related_links":
        generate_related_links(
            category
        )

    }