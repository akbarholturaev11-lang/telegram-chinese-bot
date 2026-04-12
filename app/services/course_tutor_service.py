import json
from typing import Any

from app.services.ai_service import AIService


class CourseTutorService:
    def __init__(self):
        self.ai_service = AIService()

    def _parse_json_field(self, value: Any, default: Any):
        if value is None or value == "":
            return default
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except Exception:
            return default

    def _safe_text(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip()

    def _build_fallback_intro(self, lesson, vocab, dialogue, grammar) -> str:
        title = self._safe_text(getattr(lesson, "title", ""))
        vocab_words = [item.get("zh", "") for item in vocab[:3] if isinstance(item, dict) and item.get("zh")]
        grammar_titles = [item.get("title_zh", "") for item in grammar[:2] if isinstance(item, dict) and item.get("title_zh")]

        first_scene = ""
        if dialogue and isinstance(dialogue[0], dict):
            first_scene = dialogue[0].get("scene_label_zh", "") or dialogue[0].get("section_label", "")

        parts = []
        if title:
            parts.append(f"Lesson topic: {title}")
        if first_scene:
            parts.append(f"Main scene: {first_scene}")
        if vocab_words:
            parts.append(f"Key words: {', '.join(vocab_words)}")
        if grammar_titles:
            parts.append(f"Grammar focus: {', '.join(grammar_titles)}")

        if not parts:
            return "Use the lesson title and available content to give a short introduction to the lesson."
        return " | ".join(parts)

    def _build_fallback_exercise(self, lesson, vocab, dialogue, grammar):
        title = self._safe_text(getattr(lesson, "title", ""))
        vocab_words = [item.get("zh", "") for item in vocab[:5] if isinstance(item, dict) and item.get("zh")]
        grammar_titles = [item.get("title_zh", "") for item in grammar[:2] if isinstance(item, dict) and item.get("title_zh")]

        exercise = {
            "fallback": True,
            "instruction": "Create 2 short exercises only from the current lesson theme and content.",
            "lesson_title": title,
            "allowed_vocabulary": vocab_words,
            "allowed_grammar": grammar_titles,
            "rules": [
                "Do not introduce another lesson topic.",
                "Do not use unrelated vocabulary.",
                "Keep exercises short and beginner-friendly for the current HSK level.",
            ],
        }
        return exercise

    def _build_fallback_homework(self, lesson, vocab, dialogue, grammar):
        title = self._safe_text(getattr(lesson, "title", ""))
        vocab_words = [item.get("zh", "") for item in vocab[:5] if isinstance(item, dict) and item.get("zh")]
        grammar_titles = [item.get("title_zh", "") for item in grammar[:2] if isinstance(item, dict) and item.get("title_zh")]

        homework = {
            "fallback": True,
            "instruction": "Create 1 short homework task only from the current lesson theme.",
            "lesson_title": title,
            "allowed_vocabulary": vocab_words,
            "allowed_grammar": grammar_titles,
            "rules": [
                "Homework must stay inside this lesson topic.",
                "Do not create another lesson.",
                "Do not use unrelated scenarios.",
            ],
        }
        return homework

    def _build_fallback_review(self, lesson, vocab, dialogue, grammar):
        title = self._safe_text(getattr(lesson, "title", ""))
        review_words = [item.get("zh", "") for item in vocab[:3] if isinstance(item, dict) and item.get("zh")]
        review_grammar = [item.get("title_zh", "") for item in grammar[:1] if isinstance(item, dict) and item.get("title_zh")]

        review = {
            "fallback": True,
            "instruction": "Create a short review from the current lesson only.",
            "lesson_title": title,
            "review_words": review_words,
            "review_grammar": review_grammar,
            "rules": [
                "Review only this lesson.",
                "Give short revision only.",
                "No new topic.",
            ],
        }
        return review

    def _build_step_payload(self, lesson, step: str) -> dict:
        vocab = self._parse_json_field(getattr(lesson, "vocabulary_json", None), [])
        dialogue = self._parse_json_field(getattr(lesson, "dialogue_json", None), [])
        grammar = self._parse_json_field(getattr(lesson, "grammar_json", None), [])
        exercise = self._parse_json_field(getattr(lesson, "exercise_json", None), [])
        answers = self._parse_json_field(getattr(lesson, "answers_json", None), [])
        homework = self._parse_json_field(getattr(lesson, "homework_json", None), [])
        review = self._parse_json_field(getattr(lesson, "review_json", None), [])
        intro_text = self._safe_text(getattr(lesson, "intro_text", ""))

        base = {
            "lesson_code": getattr(lesson, "lesson_code", ""),
            "lesson_title": getattr(lesson, "title", ""),
            "step": step,
        }

        if step == "intro":
            base["intro"] = intro_text or self._build_fallback_intro(lesson, vocab, dialogue, grammar)
            base["supporting_context"] = {
                "vocabulary_preview": vocab[:3],
                "dialogue_preview": dialogue[:1],
                "grammar_preview": grammar[:2],
            }
            return base

        if step == "vocabulary":
            base["vocabulary"] = vocab
            return base

        if step == "dialogue":
            base["dialogue"] = dialogue
            return base

        if step == "grammar":
            base["grammar"] = grammar
            base["vocabulary_preview"] = vocab[:5]
            return base

        if step == "exercise":
            base["exercise"] = exercise if exercise else self._build_fallback_exercise(lesson, vocab, dialogue, grammar)
            base["answers"] = answers
            base["allowed_context"] = {
                "vocabulary": vocab[:8],
                "dialogue": dialogue[:2],
                "grammar": grammar[:3],
            }
            return base

        if step == "homework":
            base["homework"] = homework if homework else self._build_fallback_homework(lesson, vocab, dialogue, grammar)
            base["allowed_context"] = {
                "vocabulary": vocab[:8],
                "dialogue": dialogue[:2],
                "grammar": grammar[:3],
            }
            return base

        if step == "review":
            base["review"] = review if review else self._build_fallback_review(lesson, vocab, dialogue, grammar)
            return base

        if step == "satisfaction_check":
            base["instruction"] = "Ask if the user understood the lesson. Do not move to another lesson."
            return base

        base["generic_context"] = {
            "intro": intro_text or self._build_fallback_intro(lesson, vocab, dialogue, grammar),
            "vocabulary": vocab[:5],
            "dialogue": dialogue[:1],
            "grammar": grammar[:2],
        }
        return base

    def _build_prompt(
        self,
        user_language: str,
        user_level: str,
        lesson,
        step: str,
        user_message: str = "",
    ) -> str:
        step_payload = self._build_step_payload(lesson, step)
        payload_text = json.dumps(step_payload, ensure_ascii=False, indent=2)

        return f"""
You are an AI Chinese teacher running a structured HSK course lesson.

STRICT GLOBAL RULES:
1. Teach ONLY the current lesson.
2. Never switch to another lesson.
3. Never introduce another topic, another homework, another test, or another scenario from outside the current lesson.
4. If a section is missing in lesson data, create fallback content ONLY from the current lesson title, current lesson vocabulary, current lesson dialogue, and current lesson grammar.
5. All AI-generated exercises, tests, homework, examples, and review must stay inside the current lesson theme and context.
6. Do not invent unrelated vocabulary or unrelated grammar.
7. Respect the current step strictly. Do not jump to another step unless the user explicitly asks for clarification.
8. Explain in the user's language.
9. Keep the response structured, clear, and teacher-like.
10. If the user asks a follow-up question, answer only inside the current lesson and current step.

USER CONTEXT:
- user_language: {user_language}
- user_level: {user_level}
- current_step: {step}

CURRENT LESSON STEP DATA:
{payload_text}

USER MESSAGE:
{user_message}

STEP-SPECIFIC INSTRUCTIONS:
- intro: briefly introduce only this lesson and what will be learned.
- vocabulary: teach only the current lesson vocabulary.
- dialogue: explain only the current lesson dialogue.
- grammar: explain only the listed grammar points for this lesson.
- exercise: check or generate exercises only inside this lesson context.
- homework: give or check homework only inside this lesson context.
- review: review only this lesson, not another lesson.
- satisfaction_check: ask whether the user understood the lesson, without moving forward automatically.

Now respond for the current lesson and current step only.
""".strip()


    def _build_homework_evaluation_prompt(
        self,
        user_language: str,
        user_level: str,
        lesson,
        submission_text: str,
    ) -> str:
        vocab = self._parse_json_field(getattr(lesson, "vocabulary_json", None), [])
        dialogue = self._parse_json_field(getattr(lesson, "dialogue_json", None), [])
        grammar = self._parse_json_field(getattr(lesson, "grammar_json", None), [])
        homework = self._parse_json_field(getattr(lesson, "homework_json", None), [])

        title = self._safe_text(getattr(lesson, "title", ""))
        lesson_code = self._safe_text(getattr(lesson, "lesson_code", ""))

        if not homework:
            homework = self._build_fallback_homework(lesson, vocab, dialogue, grammar)

        payload = {
            "lesson_code": lesson_code,
            "lesson_title": title,
            "homework": homework,
            "allowed_context": {
                "vocabulary": vocab[:8],
                "dialogue": dialogue[:2],
                "grammar": grammar[:3],
            },
            "submission_text": submission_text,
        }

        payload_text = json.dumps(payload, ensure_ascii=False, indent=2)

        return f"""
You are evaluating a student's homework for a structured HSK course lesson.

STRICT RULES:
1. Evaluate ONLY inside the current lesson.
2. Do not use another lesson topic.
3. Do not use unrelated vocabulary or grammar.
4. If the stored homework is missing or incomplete, evaluate only against the current lesson title, vocabulary, dialogue, and grammar.
5. Feedback must be short, clear, and teacher-like.
6. Give a score from 0 to 100.
7. Decide passed = true only if the answer is acceptable for the current HSK lesson.
8. Return JSON only.
9. JSON format must be:
{
  "score": 0,
  "passed": false,
  "feedback_text": "..."
}

USER CONTEXT:
- user_language: {user_language}
- user_level: {user_level}

CURRENT LESSON HOMEWORK DATA:
{payload_text}
""".strip()

    async def evaluate_homework(
        self,
        user_language: str,
        user_level: str,
        lesson,
        submission_text: str,
    ) -> dict:
        submission_text = (submission_text or "").strip()
        if not submission_text:
            return {
                "score": 0,
                "passed": False,
                "feedback_text": "Homework submission is empty.",
            }

        prompt = self._build_homework_evaluation_prompt(
            user_language=user_language,
            user_level=user_level,
            lesson=lesson,
            submission_text=submission_text,
        )

        raw_reply = await self.ai_service.generate_reply(
            text=prompt,
            user_language=user_language,
            user_level=user_level,
            history=[],
        )

        try:
            data = json.loads(raw_reply)
        except Exception:
            data = {
                "score": 60,
                "passed": True,
                "feedback_text": raw_reply.strip() if raw_reply.strip() else "Homework received.",
            }

        score = data.get("score", 60)
        passed = data.get("passed", True)
        feedback_text = str(data.get("feedback_text", "")).strip()

        try:
            score = int(score)
        except Exception:
            score = 60

        if score < 0:
            score = 0
        if score > 100:
            score = 100

        if not isinstance(passed, bool):
            passed = bool(passed)

        if not feedback_text:
            if user_language == "tj":
                feedback_text = f"✅ Вазифа санҷида шуд. Баҳо: {score}/100"
            elif user_language == "uz":
                feedback_text = f"✅ Uy vazifa tekshirildi. Baho: {score}/100"
            else:
                feedback_text = f"✅ Домашнее задание проверено. Оценка: {score}/100"

        return {
            "score": score,
            "passed": passed,
            "feedback_text": feedback_text,
        }

    async def generate_step_response(
        self,
        user_language: str,
        user_level: str,
        lesson,
        step: str,
        user_message: str = "",
    ) -> str:
        prompt = self._build_prompt(
            user_language=user_language,
            user_level=user_level,
            lesson=lesson,
            step=step,
            user_message=user_message,
        )

        return await self.ai_service.generate_reply(
            text=prompt,
            user_language=user_language,
            user_level=user_level,
            history=[],
        )
