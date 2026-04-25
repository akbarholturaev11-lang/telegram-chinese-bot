import json
from typing import Any
from app.services.ai_service import AIService

COURSE_MODEL = "gpt-4.1"

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
            "grammar_preview": grammar[:2],
            "dialogue_preview": dialogue[:1],
        }

        prompt = f"""You are an HSK Chinese teacher. Your task: introduce this lesson warmly and clearly.

LESSON DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Give a short, engaging introduction (3-5 lines)
- Preview what the student will learn: vocabulary, grammar, dialogue topic
- Do NOT teach yet — just introduce
- End with: "Ready? Let's begin!" (in {user_language})"""

        return prompt, data

    def _prompt_vocab(self, lesson, user_language, user_level) -> tuple:
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {"lesson_title": title, "vocabulary": vocab}

        prompt = f"""You are an HSK Chinese teacher. Your task: teach the vocabulary for this lesson.

VOCABULARY DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Present ONLY the words in the vocabulary list above — no other words
- For each word show: Chinese character, pinyin, meaning in {user_language}, 1 short example sentence
- If the user asks about a word — explain only from this list
- If the user asks about something outside this list — politely redirect to the current vocabulary
- Keep it clear and structured"""

        return prompt, data

    def _prompt_dialogue(self, lesson, user_language, user_level) -> tuple:
        dialogue = self._parse(getattr(lesson, "dialogue_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {"lesson_title": title, "dialogue": dialogue}

        prompt = f"""You are an HSK Chinese teacher. Your task: teach the dialogue for this lesson.

DIALOGUE DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Present ONLY the dialogue above — no other scenarios
- Explain each line: Chinese, pinyin, meaning in {user_language}
- Explain the context and when this dialogue would be used
- If user asks questions — answer only about this dialogue
- Do NOT introduce new vocabulary outside the dialogue"""

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

        prompt = f"""You are an HSK Chinese teacher. Your task: teach the grammar points for this lesson.

GRAMMAR DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Teach ONLY the grammar points listed above
- For each grammar point: explain the rule, show the pattern, give 2 examples using lesson vocabulary
- Examples must use ONLY the lesson_vocabulary list above
- Do NOT introduce grammar from other lessons
- Keep explanations clear and concise"""

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

        prompt = f"""You are an HSK Chinese teacher. Your task: conduct exercises for this lesson.

EXERCISE DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Give exercises using ONLY the allowed_vocabulary and allowed_grammar above
- Do NOT use vocabulary or grammar from other lessons
- Check the user's answers against correct_answers if provided
- Give clear feedback: what is correct, what needs improvement
- Encourage the student briefly"""

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

        prompt = f"""You are an HSK Chinese teacher. Your task: conduct a quiz for this lesson.

QUIZ DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Create a short quiz using ONLY test_vocabulary and test_grammar above
- Quiz format: 3-5 questions (multiple choice or fill in the blank)
- Do NOT test vocabulary or grammar outside the lists above
- When user answers: check correctness, give score, explain mistakes
- Be encouraging"""

        return prompt, data

    def _prompt_satisfaction_check(self, lesson, user_language, user_level) -> tuple:
        title = self._safe(getattr(lesson, "title", ""))
        data = {"lesson_title": title}

        prompt = f"""You are an HSK Chinese teacher. Your task: check if the student understood this lesson.

LESSON: {title}

RULES:
- Reply ONLY in {user_language}
- Ask ONE simple question: did the student understand the lesson?
- Offer two choices: yes (understood) or no (need more explanation)
- Do NOT teach new content here
- Do NOT move to the next step yourself — wait for the student's answer"""

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

        prompt = f"""You are an HSK Chinese teacher. Your task: give and check homework for this lesson.

HOMEWORK DATA:
{json.dumps(data, ensure_ascii=False, indent=2)}

RULES:
- Reply ONLY in {user_language}
- Level: {user_level}
- Give homework using ONLY allowed_vocabulary and allowed_grammar above
- Do NOT create tasks outside this lesson scope
- When student submits: check it, give clear feedback, give score 0-100
- Be encouraging and specific about what was good and what needs work"""

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

        return await self.ai_service.generate_reply(
            text=full_text,
            user_language=user_language,
            user_level=user_level,
            history=history or [],
            model_override=COURSE_MODEL,
        )

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
