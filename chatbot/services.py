from .grammar import check_grammar

from .seo import seo_analysis

from .tone import analyze_tone


# ================= READABILITY ================= #

def calculate_readability(content):

    word_count = len(
        content.split()
    )

    sentence_count = max(
        content.count('.'),
        1
    )

    avg_words = word_count / sentence_count

    if avg_words <= 14:

        return 95

    elif avg_words <= 18:

        return 88

    elif avg_words <= 25:

        return 78

    return 65


# ================= CATEGORY TAGS ================= #

CATEGORY_TAGS = {

    'Technology':
    'AI, Technology, Innovation, Software',

    'Business':
    'Business, Startup, Marketing, Finance',

    'Food':
    'Food, Recipes, Cooking, Restaurant',

    'Health':
    'Health, Fitness, Wellness, Diet',

    'Education':
    'Education, Learning, Students, Study',

    'Nature':
    'Nature, Environment, Wildlife, Earth',

    'News':
    'News, Current Affairs, Breaking News',

    'Motivation':
    'Motivation, Success, Mindset, Inspiration'

}


# ================= PROCESS AI CONTENT ================= #

def process_ai_content(ai_data):

    content = ai_data.get(
        'content',
        ''
    )

    # ✅ CATEGORY

    category = ai_data.get(
        'category',
        'General'
    )

    # ✅ GRAMMAR

    grammar_data = check_grammar(
        content
    )

    corrected_content = grammar_data.get(
        'corrected_text',
        content
    )

    # ✅ SEO

    seo_data = seo_analysis(
        corrected_content
    )

    # ✅ TONE

    tone = analyze_tone(
        corrected_content
    )

    # ✅ READABILITY

    readability_score = calculate_readability(
        corrected_content
    )

    # ✅ AUTO TAGS

    auto_tags = CATEGORY_TAGS.get(
        category,
        'AI, Blog'
    )

    # ✅ FEATURED IMAGE PROMPT

    image_prompt = ai_data.get(
        'featured_image_prompt',
        f'{category} professional blog image'
    )

    return {

        'title':

        ai_data.get(
            'title',
            'Untitled Blog'
        ),

        'slug':

        ai_data.get(
            'slug',
            'untitled-blog'
        ),

        'category':

        category,

        'meta_description':

        ai_data.get(
            'meta_description',
            ''
        ),

        # ✅ AUTO TAGS

        'tags':

        ai_data.get(
            'tags',
            auto_tags
        ),

        # ✅ SMART IMAGE PROMPT

        'featured_image_prompt':

        image_prompt,

        # ✅ CORRECTED CONTENT

        'content':

        corrected_content,

        'faq':

        ai_data.get(
            'faq',
            ''
        ),

        'conclusion':

        ai_data.get(
            'conclusion',
            ''
        ),

        # ✅ SCORES

        'grammar_score':

        grammar_data.get(
            'grammar_score',
            95
        ),

        'seo_score':

        seo_data.get(
            'seo_score',
            90
        ),

        'seo_suggestions':

        seo_data.get(
            'suggestions',
            []
        ),

        'tone':

        tone,

        'readability_score':

        readability_score

    }