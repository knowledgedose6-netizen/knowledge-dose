def analyze_tone(content):
    
    content = content.lower()


    # ================= TECHNOLOGY ================= #

    tech_keywords = [

        'technology',
        'ai',
        'software',
        'coding',
        'machine learning',
        'cybersecurity',
        'robotics'

    ]

    # ================= EDUCATION ================= #

    education_keywords = [

        'education',
        'student',
        'learning',
        'study',
        'university',
        'school'

    ]

    # ================= NEWS ================= #

    news_keywords = [

        'news',
        'breaking',
        'world',
        'current affairs',
        'latest updates'

    ]

    # ================= MOTIVATION ================= #

    motivation_keywords = [

        'success',
        'motivation',
        'mindset',
        'discipline',
        'inspiration',
        'growth'

    ]

    # ================= BUSINESS ================= #

    business_keywords = [

        'business',
        'startup',
        'marketing',
        'finance',
        'entrepreneur'

    ]

    # ================= HEALTH ================= #

    health_keywords = [

        'health',
        'fitness',
        'exercise',
        'diet',
        'mental health',
        'wellness'

    ]

    # ================= FOOD ================= #

    food_keywords = [

        'food',
        'recipe',
        'restaurant',
        'meal',
        'cooking'

    ]


    # ================= DETECTION ================= #

    if any(word in content for word in tech_keywords):

        return 'Technical'

    elif any(word in content for word in education_keywords):

        return 'Educational'

    elif any(word in content for word in news_keywords):

        return 'Professional News'

    elif any(word in content for word in motivation_keywords):

        return 'Motivational'

    elif any(word in content for word in business_keywords):

        return 'Business Professional'

    elif any(word in content for word in health_keywords):

        return 'Health & Wellness'

    elif any(word in content for word in food_keywords):

        return 'Lifestyle & Food'

    return 'Professional'