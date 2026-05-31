# =========================================================
# KD AI ASSISTANT - image_utils.py
# FULLY UPGRADED ULTRA PREMIUM VERSION
# =========================================================

import os
import io
import random
import requests
import hashlib
from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile


# =========================================================
# PEXELS API
# =========================================================

PEXELS_API_KEY = settings.PEXELS_API_KEY

PEXELS_URL = "https://api.pexels.com/v1/search"


# =========================================================
# SAFE FALLBACK IMAGES
# =========================================================

FALLBACK_IMAGES = [

    "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg",

    "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg",

    "https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg",

    "https://images.pexels.com/photos/1181675/pexels-photo-1181675.jpeg",

    "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg",

    "https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg",

    "https://images.pexels.com/photos/5212345/pexels-photo-5212345.jpeg"

]


# =========================================================
# IMAGE SETTINGS
# =========================================================

IMAGE_WIDTH = 1280

IMAGE_HEIGHT = 720

IMAGE_QUALITY = 75

UPLOAD_FOLDER = "uploads/ai_blogs/"


# =========================================================
# CLEAN QUERY
# =========================================================

def clean_query(query):

    if not query:

        return "technology"

    query = (
        str(query)
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )

    return query


# =========================================================
# SMART IMAGE QUERY
# =========================================================

def build_image_query(query):

    query = clean_query(query)

    blocked_words = [

        "write",
        "blog",
        "article",
        "seo",
        "generate",
        "premium"

    ]

    words = query.split()

    final_words = [

        word for word in words
        if word.lower() not in blocked_words

    ]

    optimized_query = " ".join(final_words)

    optimized_query += " realistic professional"

    return optimized_query


# =========================================================
# REMOVE DUPLICATES
# =========================================================

def remove_duplicate_images(images):

    unique_images = []

    used_hashes = set()

    for image in images:

        image_hash = hashlib.md5(

            image.encode()

        ).hexdigest()

        if image_hash not in used_hashes:

            unique_images.append(image)

            used_hashes.add(image_hash)

    return unique_images


# =========================================================
# IMAGE VALIDATION
# =========================================================

def validate_image_url(url):

    try:

        if not url:

            return False

        valid_domains = [

            "pexels.com",
            "images.pexels.com"

        ]

        return any(

            domain in url
            for domain in valid_domains

        )

    except Exception:

        return False


# =========================================================
# DOWNLOAD + COMPRESS IMAGE
# =========================================================

def download_and_compress_image(

    image_url,

    title="kd-ai-blog"

):

    try:

        response = requests.get(

            image_url,

            timeout=30

        )

        if response.status_code != 200:

            return None

        image = Image.open(

            io.BytesIO(response.content)

        )

        # =============================================
        # RGB CONVERT
        # =============================================

        if image.mode in ("RGBA", "P"):

            image = image.convert("RGB")

        # =============================================
        # RESIZE
        # =============================================

        image = image.resize(

            (

                IMAGE_WIDTH,

                IMAGE_HEIGHT

            )

        )

        # =============================================
        # SAFE FILE NAME
        # =============================================

        safe_title = (

            title.lower()
            .replace(" ", "-")
            .replace("/", "-")
        )

        random_hash = hashlib.md5(

            image_url.encode()

        ).hexdigest()[:10]

        file_name = f"""

        {safe_title}-{random_hash}.jpg

        """.replace("\n", "").strip()

        # =============================================
        # SAVE BUFFER
        # =============================================

        buffer = io.BytesIO()

        image.save(

            buffer,

            format="JPEG",

            quality=IMAGE_QUALITY,

            optimize=True

        )

        # =============================================
        # DJANGO FILE
        # =============================================

        return ContentFile(

            buffer.getvalue(),

            name=file_name

        )

    except Exception as e:

        print(

            "IMAGE DOWNLOAD ERROR:",

            e

        )

        return None


# =========================================================
# FETCH PEXELS IMAGES
# =========================================================

def get_pexels_images(

    query,

    per_page=6

):

    try:

        query = build_image_query(query)

        headers = {

            "Authorization":
            PEXELS_API_KEY

        }

        params = {

            "query":query,

            "per_page":15,

            "orientation":"landscape",

            "size":"large",

            "locale":"en-US"

        }

        response = requests.get(

            PEXELS_URL,

            headers=headers,

            params=params,

            timeout=20

        )

        data = response.json()

        photos = data.get(
            "photos",
            []
        )

        images = []

        used_photographers = set()

        for photo in photos:

            src = photo.get(
                "src",
                {}
            )

            photographer = photo.get(
                "photographer",
                ""
            )

            if photographer in used_photographers:

                continue

            image_url = (

                src.get("large2x")

                or

                src.get("large")

                or

                src.get("medium")

            )

            if not image_url:

                continue

            if not validate_image_url(
                image_url
            ):

                continue

            images.append(
                image_url
            )

            used_photographers.add(
                photographer
            )

        # =============================================
        # REMOVE DUPLICATES
        # =============================================

        images = remove_duplicate_images(
            images
        )

        # =============================================
        # RANDOMIZE
        # =============================================

        random.shuffle(images)

        # =============================================
        # FALLBACK
        # =============================================

        if not images:

            return random.sample(

                FALLBACK_IMAGES,

                min(

                    len(FALLBACK_IMAGES),

                    4

                )

            )

        return images[:per_page]

    except Exception as e:

        print(

            "PEXELS ERROR:",

            e

        )

        return random.sample(

            FALLBACK_IMAGES,

            min(

                len(FALLBACK_IMAGES),

                4

            )

        )


# =========================================================
# FEATURED IMAGE
# =========================================================

def get_featured_image(query):

    try:

        images = get_pexels_images(

            query,

            per_page=1

        )

        if images:

            return images[0]

        return random.choice(
            FALLBACK_IMAGES
        )

    except Exception:

        return random.choice(
            FALLBACK_IMAGES
        )


# =========================================================
# INLINE IMAGES
# =========================================================

def get_inline_images(query):

    try:

        images = get_pexels_images(

            query,

            per_page=6

        )

        return images

    except Exception:

        return FALLBACK_IMAGES[:4]


# =========================================================
# CATEGORY IMAGE MAPPING
# =========================================================

CATEGORY_IMAGE_QUERIES = {

    "AI":
    "artificial intelligence futuristic technology robots",

    "Technology":
    "modern technology innovation computers",

    "Business":
    "startup business office meeting success",

    "Education":
    "digital education online learning students classroom",

    "Health":
    "healthcare wellness fitness healthy lifestyle",

    "Travel":
    "luxury travel destinations tourism",

    "Sports":
    "sports athlete stadium football cricket",

    "Fashion":
    "luxury fashion modern style clothing",

    "Food":
    "premium restaurant food recipes cooking",

    "Motivation":
    "success motivation inspiration goals",

    "Nature":
    "beautiful nature landscape mountains",

    "Environment":
    "eco sustainability environment earth",

    "Internet":
    "internet digital world networking",

    "Freelancing":
    "remote freelancing workspace laptop",

    "News":
    "breaking news media journalism",

    "Current Affairs":
    "global politics current affairs conference"

}


# =========================================================
# CATEGORY BASED IMAGES
# =========================================================

def get_category_images(category):

    query = CATEGORY_IMAGE_QUERIES.get(

        category,

        "modern technology"

    )

    return get_pexels_images(query)


# =========================================================
# BLOG IMAGE PACKAGE
# =========================================================

def generate_blog_images(

    title="",

    category="General"

):

    try:

        combined_query = f"""

        {title}

        {category}

        realistic
        professional
        modern
        hd

        """

        featured_image = get_featured_image(
            combined_query
        )

        inline_images = get_inline_images(
            combined_query
        )

        inline_images = [

            image for image in inline_images
            if image != featured_image
        ]

        return {

            "featured_image":
            featured_image,

            "inline_images":
            inline_images[:6]

        }

    except Exception as e:

        print(

            "BLOG IMAGE ERROR:",

            e

        )

        return {

            "featured_image":
            random.choice(
                FALLBACK_IMAGES
            ),

            "inline_images":
            FALLBACK_IMAGES[:4]

        }


# =========================================================
# IMAGE PLACEHOLDER
# =========================================================

def get_placeholder_image():

    return random.choice(
        FALLBACK_IMAGES
    )