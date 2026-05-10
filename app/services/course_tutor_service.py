import json
from typing import Any
from app.services.ai_service import AIService

COURSE_MODEL = "o4-mini"

# Steps that have the "I understood" advance button — append hint to AI response
_CONVERSATIONAL_STEPS = {"intro", "vocab", "vocabulary", "dialogue", "grammar", "exercise", "quiz"}

_PRESS_BUTTON_HINT = {
    "uz": "\n\n✅ <i>Tushundingiz bo'lsa, pastdagi tugmani bosing.</i>",
    "ru": "\n\n✅ <i>Если поняли — нажмите кнопку ниже.</i>",
    "tj": "\n\n✅ <i>Агар фаҳмидед, тугмаи поёниро пахш кунед.</i>",
}


class CourseTutorService:
    def __init__(self):
        self.ai_service = AIService()

    def _parse(self, value: Any, default: Any):
        if value is None or value == "":
            return default
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except Exception:
            return default

    def _safe(self, value: Any) -> str:
        return str(value).strip() if value else ""

    # ─── STEP PROMPTS ───────────────────────────────────────────

    def _prompt_intro(self, lesson, user_language, user_level) -> tuple:
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        dialogue = self._parse(getattr(lesson, "dialogue_json", None), [])
        grammar = self._parse(getattr(lesson, "grammar_json", None), [])
        intro_text = self._safe(getattr(lesson, "intro_text", ""))
        title = self._safe(getattr(lesson, "title", ""))

        data = {
            "lesson_title": title,
            "intro_text": intro_text,
            "vocabulary_preview": vocab[:3],
            "grammar_preview": grammar[:1],
            "dialogue_preview": dialogue[:1],
        }

        prompt = f"""You are a friendly HSK Chinese tutor. Welcome the student to this lesson warmly.

LESSON DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, adapted for {user_level} level
- Use <b>...</b> for Chinese characters, <code>...</code> for pinyin
- Max 4 lines total
- Preview 2-3 vocabulary words and the main grammar topic to spark curiosity
- Do NOT teach yet — just introduce
- End with an energetic line like "Ready? Let's go! 🚀" (in {user_language})"""

        return prompt, data

    def _prompt_vocab(self, lesson, user_language, user_level) -> tuple:
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {"lesson_title": title, "vocabulary": vocab}

        prompt = f"""You are a friendly HSK Chinese tutor. Teach the vocabulary for this lesson engagingly.

VOCABULARY DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, {user_level} level
- Use <b>...</b> for Chinese characters, <code>...</code> for pinyin
- Format each word: <b>汉字</b> [<code>pīnyīn</code>] — meaning — one short example sentence
- If similar words exist (e.g. 我/你, 大/小, 去/来), compare them side by side to show the difference
- Max 2 lines per word, total response under 15 lines
- If student asks about a word outside this list, politely redirect to the current vocabulary"""

        return prompt, data

    def _prompt_dialogue(self, lesson, user_language, user_level) -> tuple:
        dialogue = self._parse(getattr(lesson, "dialogue_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {"lesson_title": title, "dialogue": dialogue}

        prompt = f"""You are a friendly HSK Chinese tutor. Teach this dialogue step by step.

DIALOGUE DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, {user_level} level
- Use <b>...</b> for Chinese, <code>...</code> for pinyin
- Present each line: <b>Chinese</b> [<code>pinyin</code>] — meaning in {user_language}
- After presenting, briefly explain the context (where/when this conversation happens)
- Highlight 1-2 useful patterns from the dialogue with a real-life comparison
- Max 12 lines total
- Answer student questions ONLY about this dialogue"""

        return prompt, data

    def _prompt_grammar(self, lesson, user_language, user_level) -> tuple:
        grammar = self._parse(getattr(lesson, "grammar_json", None), [])
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {
            "lesson_title": title,
            "grammar_points": grammar,
            "lesson_vocabulary": vocab[:5],
        }

        prompt = f"""You are a friendly HSK Chinese tutor. Teach the grammar points clearly and concisely.

GRAMMAR DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, {user_level} level
- Use <b>...</b> for Chinese, <code>...</code> for pinyin
- For each grammar point: rule → pattern with blanks → 2 examples using lesson_vocabulary
- If there are similar-looking structures (e.g. 的/地/得, 吗/呢, 在/有), compare them with a quick tip
- Examples must use ONLY lesson_vocabulary — no outside words
- Max 10 lines total"""

        return prompt, data

    def _prompt_exercise(self, lesson, user_language, user_level) -> tuple:
        exercise = self._parse(getattr(lesson, "exercise_json", None), [])
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        grammar = self._parse(getattr(lesson, "grammar_json", None), [])
        answers = self._parse(getattr(lesson, "answers_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        if not exercise:
            exercise = {
                "instruction": "Create 3 exercises from the lesson vocabulary and grammar only.",
                "allowed_vocabulary": [w.get("zh","") for w in vocab[:8] if isinstance(w,dict)],
                "allowed_grammar": [g.get("title_zh","") for g in grammar[:3] if isinstance(g,dict)],
            }

        data = {
            "lesson_title": title,
            "exercises": exercise,
            "correct_answers": answers,
            "allowed_vocabulary": vocab[:8],
            "allowed_grammar": grammar[:3],
        }

        prompt = f"""You are a friendly HSK Chinese tutor. Give short practice exercises.

EXERCISE DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, {user_level} level
- Use <b>...</b> for Chinese, <code>...</code> for pinyin
- Create 2-3 exercises using ONLY allowed_vocabulary and allowed_grammar
- Mix formats: fill-in-the-blank AND translate a sentence
- When checking: ✅ correct answer or ❌ + correct answer with a short tip
- Be encouraging: "Well done! 👏" or "Almost! Here's a tip..."
- Max 10 lines total"""

        return prompt, data

    def _prompt_quiz(self, lesson, user_language, user_level) -> tuple:
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        grammar = self._parse(getattr(lesson, "grammar_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {
            "lesson_title": title,
            "test_vocabulary": vocab[:10],
            "test_grammar": grammar[:3],
        }

        prompt = f"""You are a friendly HSK Chinese tutor. Give a short quiz to test understanding.

QUIZ DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, {user_level} level
- Use <b>...</b> for Chinese, <code>...</code> for pinyin
- 3-4 questions only (multiple choice or fill-in-the-blank)
- Use ONLY test_vocabulary and test_grammar — no outside content
- After student answers: show score, mark ✅/❌ per question, briefly explain mistakes
- Be encouraging
- Max 10 lines per interaction"""

        return prompt, data

    def _prompt_satisfaction_check(self, lesson, user_language, user_level) -> tuple:
        title = self._safe(getattr(lesson, "title", ""))
        data = {"lesson_title": title}

        prompt = f"""You are a friendly HSK Chinese tutor. Check if the student understood this lesson.

LESSON: {title}

RULES:
- Reply ONLY in {user_language}
- Ask ONE simple question: did you understand the lesson?
- Keep it to 2 lines maximum
- Do NOT teach new content
- Do NOT move forward — wait for the student's answer via the buttons"""

        return prompt, data

    def _prompt_homework(self, lesson, user_language, user_level) -> tuple:
        homework = self._parse(getattr(lesson, "homework_json", None), [])
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        grammar = self._parse(getattr(lesson, "grammar_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        if not homework:
            homework = {
                "instruction": "Create 1 homework task using only lesson vocabulary and grammar.",
                "allowed_vocabulary": [w.get("zh","") for w in vocab[:8] if isinstance(w,dict)],
                "allowed_grammar": [g.get("title_zh","") for g in grammar[:3] if isinstance(g,dict)],
            }

        data = {
            "lesson_title": title,
            "homework": homework,
            "allowed_vocabulary": vocab[:8],
            "allowed_grammar": grammar[:3],
        }

        prompt = f"""You are a friendly HSK Chinese tutor. Assign and evaluate homework.

HOMEWORK DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}, {user_level} level
- Use <b>...</b> for Chinese, <code>...</code> for pinyin
- Give ONE clear homework task using ONLY allowed_vocabulary and allowed_grammar
- When student submits: give score 0-100, mark each item ✅/❌, short specific feedback
- Be encouraging and concrete about what was good and what needs work
- Max 8 lines"""

        return prompt, data

    # ─── STEP ROUTER ────────────────────────────────────────────

    def _build_prompt_for_step(self, lesson, step: str, user_language: str, user_level: str) -> tuple:
        handlers = {
            "intro":               self._prompt_intro,
            "vocab":               self._prompt_vocab,
            "vocabulary":          self._prompt_vocab,
            "dialogue":            self._prompt_dialogue,
            "grammar":             self._prompt_grammar,
            "exercise":            self._prompt_exercise,
            "quiz":                self._prompt_quiz,
            "satisfaction_check":  self._prompt_satisfaction_check,
            "homework":            self._prompt_homework,
        }
        handler = handlers.get(step, self._prompt_intro)
        return handler(lesson, user_language, user_level)

    # ─── PUBLIC METHODS ──────────────────────────────────────────

    async def generate_step_response(
        self,
        user_language: str,
        user_level: str,
        lesson,
        step: str,
        user_message: str = "",
        history: list = None,
    ) -> str:
        prompt, _ = self._build_prompt_for_step(lesson, step, user_language, user_level)

        full_text = prompt
        if user_message:
            full_text += f"\n\nSTUDENT MESSAGE:\n{user_message}"

        response = await self.ai_service.generate_reply(
            text=full_text,
            user_language=user_language,
            user_level=user_level,
            history=history or [],
            model_override=COURSE_MODEL,
        )

        if step in _CONVERSATIONAL_STEPS:
            hint = _PRESS_BUTTON_HINT.get(user_language, _PRESS_BUTTON_HINT["ru"])
            response = response.rstrip() + hint

        return response

    def _build_homework_evaluation_prompt(self, user_language, user_level, lesson, submission_text) -> str:
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        grammar = self._parse(getattr(lesson, "grammar_json", None), [])
        homework = self._parse(getattr(lesson, "homework_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        if not homework:
            homework = {
                "instruction": "Evaluate based on lesson vocabulary and grammar.",
                "allowed_vocabulary": [w.get("zh","") for w in vocab[:8] if isinstance(w,dict)],
            }

        payload = {
            "lesson_title": title,
            "homework": homework,
            "allowed_vocabulary": vocab[:8],
            "allowed_grammar": grammar[:3],
            "student_submission": submission_text,
        }

        return f"""You are evaluating a student's homework for an HSK lesson.

DATA:
{json.dumps(payload, ensure_ascii=False, indent=2)}

RULES:
- Evaluate ONLY against the homework and lesson content above
- Give score 0-100
- decided passed = true if score >= 60
- feedback_text must be in {user_language}, short and clear
- Return ONLY valid JSON, nothing else:
{{"score": 0, "passed": false, "feedback_text": "..."}}"""

    async def evaluate_homework(self, user_language, user_level, lesson, submission_text) -> dict:
        submission_text = (submission_text or "").strip()
        if not submission_text:
            return {"score": 0, "passed": False, "feedback_text": "Empty submission."}

        prompt = self._build_homework_evaluation_prompt(user_language, user_level, lesson, submission_text)

        raw = await self.ai_service.generate_reply(
            text=prompt,
            user_language=user_language,
            user_level=user_level,
            history=[],
            model_override=COURSE_MODEL,
        )

        try:
            cleaned = raw.strip().replace("```json","").replace("```","")
            data = json.loads(cleaned)
        except Exception:
            data = {"score": 60, "passed": True, "feedback_text": raw.strip()}

        score = max(0, min(100, int(data.get("score", 60))))
        passed = bool(data.get("passed", True))
        feedback = str(data.get("feedback_text", "")).strip()

        if not feedback:
            feedback = f"✅ {score}/100"

        return {"score": score, "passed": passed, "feedback_text": feedback}
