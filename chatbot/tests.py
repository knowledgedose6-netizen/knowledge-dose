from django.test import TestCase

from django.contrib.auth.models import User

from blogs.models import Category

from .models import (

    AIBlogDraft,

    AIChatMessage

)

from .grammar import check_grammar

from .seo import seo_analysis

from .tone import analyze_tone

from .services import process_ai_content


# ================= GRAMMAR TEST ================= #

class GrammarTest(TestCase):

    def test_grammar_checker(self):

        text = (
            "He go to school everyday."
        )

        result = check_grammar(
            text
        )

        self.assertIn(

            'grammar_score',

            result

        )

        self.assertIn(

            'corrected_text',

            result

        )


# ================= SEO TEST ================= #

class SEOTest(TestCase):

    def test_seo_analysis(self):

        content = """

        <h1>Artificial Intelligence</h1>

        AI is changing the world.

        However, businesses are adapting.

        """

        result = seo_analysis(
            content
        )

        self.assertIn(

            'seo_score',

            result

        )

        self.assertIn(

            'suggestions',

            result

        )


# ================= TONE TEST ================= #

class ToneTest(TestCase):

    def test_tone_detection(self):

        content = (

            "AI technology and machine learning "

            "are transforming software industries."

        )

        tone = analyze_tone(
            content
        )

        self.assertTrue(

            'Technical' in tone

        )


# ================= SERVICES TEST ================= #

class ServicesTest(TestCase):

    def test_process_ai_content(self):

        ai_data = {

            'title':
            'AI Future',

            'slug':
            'ai-future',

            'category':
            'Technology',

            'meta_description':
            'Future of AI technology.',

            'content':
            'Artificial Intelligence is evolving rapidly.',

            'faq':
            'What is AI?',

            'conclusion':
            'AI is the future.'

        }

        result = process_ai_content(
            ai_data
        )

        self.assertEqual(

            result['title'],

            'AI Future'

        )

        self.assertIn(

            'seo_score',

            result

        )

        self.assertIn(

            'grammar_score',

            result

        )


# ================= MODEL TEST ================= #

class ModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(

            username='testuser',

            password='12345'

        )

        self.category = Category.objects.create(

            category_name='Technology'

        )

    def test_ai_blog_draft(self):

        draft = AIBlogDraft.objects.create(

            user=self.user,

            title='AI Blog',

            slug='ai-blog',

            category='Technology',

            meta_description='AI Description',

            tags='AI, Technology',

            content='AI blog content',

            seo_score=90,

            grammar_score=95,

            tone='Technical'

        )

        self.assertEqual(

            draft.title,

            'AI Blog'

        )

    def test_ai_chat_message(self):

        chat = AIChatMessage.objects.create(

            user=self.user,

            chat_title='AI Chat',

            message='Hello AI',

            response='AI response'

        )

        self.assertEqual(

            chat.chat_title,

            'AI Chat'

        )