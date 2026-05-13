import re


# ================= SEO ANALYSIS ================= #

def seo_analysis(content):

    content_lower = content.lower()

    words = content_lower.split()

    word_count = len(words)

    suggestions = []

    seo_score = 100


    # ================= WORD COUNT ================= #

    if word_count < 1000:

        seo_score -= 20

        suggestions.append(

            'Increase blog length to at least 1000+ words'

        )


    # ================= HEADINGS ================= #

    heading_count = len(

        re.findall(
            r'(##|#)',
            content
        )

    )

    if heading_count < 3:

        seo_score -= 10

        suggestions.append(

            'Add more headings and subheadings'

        )


    # ================= TRANSITION WORDS ================= #

    transition_words = [

        'however',
        'therefore',
        'moreover',
        'furthermore',
        'in addition',
        'for example',
        'on the other hand'

    ]

    found_transition = any(

        word in content_lower

        for word in transition_words

    )

    if not found_transition:

        seo_score -= 10

        suggestions.append(

            'Use more transition words'

        )


    # ================= PARAGRAPH LENGTH ================= #

    paragraphs = content.split('\n')

    long_paragraphs = [

        p for p in paragraphs

        if len(p.split()) > 180

    ]

    if long_paragraphs:

        seo_score -= 10

        suggestions.append(

            'Break long paragraphs into smaller sections'

        )


    # ================= KEYWORD DENSITY ================= #

    common_words = {}

    for word in words:

        if len(word) > 4:

            common_words[word] = common_words.get(

                word,
                0

            ) + 1

    top_keywords = sorted(

        common_words.items(),

        key=lambda x: x[1],

        reverse=True

    )[:5]

    if top_keywords:

        keyword, count = top_keywords[0]

        density = (count / word_count) * 100

        if density < 0.5:

            seo_score -= 10

            suggestions.append(

                f'Increase focus keyword density for "{keyword}"'

            )


    # ================= READABILITY ================= #

    average_sentence_length = (

        word_count / max(
            content.count('.'),
            1
        )

    )

    if average_sentence_length > 25:

        seo_score -= 10

        suggestions.append(

            'Use shorter sentences for better readability'

        )


    # ================= FINAL LIMIT ================= #

    if seo_score < 50:

        seo_score = 50


    # ================= PERFECT SEO ================= #

    if seo_score >= 90:

        suggestions.append(

            'SEO structure looks excellent'

        )


    return {

        'seo_score':

        seo_score,

        'suggestions':

        suggestions

    }