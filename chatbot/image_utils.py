from django.conf import settings

from PIL import Image

import requests

import uuid

import os


PEXELS_URL = 'https://api.pexels.com/v1/search'


# ================= AI IMAGE GENERATOR ================= #

def generate_ai_image(prompt):

    try:

        headers = {

            'Authorization':
            settings.PEXELS_API_KEY

        }

        params = {

            'query': prompt,

            'per_page': 1

        }

        response = requests.get(

            PEXELS_URL,

            headers=headers,

            params=params,

            timeout=30

        )

        data = response.json()

        photos = data.get(
            'photos',
            []
        )

        # ✅ DEFAULT IMAGE

        if not photos:

            return '/static/chatbot/images/default-ai.jpg'

        # ✅ PEXELS IMAGE

        image_url = photos[0]['src']['large']

        image_data = requests.get(

            image_url,

            timeout=30

        ).content

        # ✅ MEDIA DIRECTORY

        media_dir = 'media/ai_blogs'

        os.makedirs(

            media_dir,

            exist_ok=True

        )

        # ✅ UNIQUE FILE NAME

        filename = f'{uuid.uuid4()}.jpg'

        media_path = os.path.join(

            media_dir,

            filename

        )

        # ✅ SAVE IMAGE

        with open(media_path, 'wb') as f:

            f.write(image_data)

        # ✅ CONVERT TO WEBP

        compressed_path = convert_to_webp(
            media_path
        )

        return compressed_path

    except Exception as e:

        print("IMAGE ERROR:", e)

        return '/static/chatbot/images/default-ai.jpg'


# ================= WEBP CONVERTER ================= #

def convert_to_webp(image_path):

    image = Image.open(
        image_path
    )

    image = image.convert(
        'RGB'
    )

    # ✅ FIXED PROFESSIONAL SIZE

    image.thumbnail((900, 500))

    # ✅ WEBP PATH

    webp_path = image_path.replace(
        '.jpg',
        '.webp'
    )

    # ✅ SAVE LIGHTWEIGHT WEBP

    image.save(

        webp_path,

        'WEBP',

        quality=50,

        optimize=True

    )

    # ✅ DELETE ORIGINAL JPG

    if os.path.exists(image_path):

        os.remove(image_path)

    # ✅ RETURN CLEAN URL

    return '/' + webp_path.replace(
        '\\',
        '/'
    )