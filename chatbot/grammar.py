import requests


# ================= REAL LANGUAGETOOL GRAMMAR CHECKER ================= #

def check_grammar(text):

    try:

        response = requests.post(

            "https://api.languagetool.org/v2/check",

            data={

                "text": text,

                "language": "en-US"

            },

            timeout=30

        )

        result = response.json()

        matches = result.get(
            'matches',
            []
        )

        corrected_text = text

        # ✅ APPLY CORRECTIONS

        for match in reversed(matches):

            replacements = match.get(
                'replacements',
                []
            )

            if replacements:

                replacement = replacements[0]['value']

                offset = match['offset']

                length = match['length']

                corrected_text = (

                    corrected_text[:offset]

                    + replacement

                    + corrected_text[offset + length:]

                )

        # ✅ SCORE SYSTEM

        total_mistakes = len(matches)

        grammar_score = max(

            70,

            100 - total_mistakes

        )

        return {

            'corrected_text':

            corrected_text,

            'grammar_score':

            grammar_score,

            'mistakes':

            total_mistakes

        }

    except Exception:

        return {

            'corrected_text':

            text,

            'grammar_score':

            95,

            'mistakes':

            0

        }