import json
from typing import Any
from app.services.ai_service import AIService

COURSE_MODEL = "gpt-4o-mini"
COURSE_MAX_COMPLETION_TOKENS = 1200
HOMEWORK_EVALUATION_MAX_COMPLETION_TOKENS = 800

# Steps where "press button below" hint is appended — exercise is handled separately (no hint)
_CONVERSATIONAL_STEPS = {
    "intro", "vocab", "vocabulary", "dialogue", "grammar",
    # V2 steps:
    "vocab_1", "vocab_2",
    "dialogue_1", "dialogue_2", "dialogue_3", "dialogue_4",
}

_PRESS_BUTTON_HINT = {
    "uz": "\n\n✅ <i>Tushundingiz bo'lsa, pastdagi tugmani bosing.</i>",
    "ru": "\n\n✅ <i>Если поняли — нажмите кнопку ниже.</i>",
    "tj": "\n\n✅ <i>Агар фаҳмидед, тугмаи поёниро пахш кунед.</i>",
}

_CHINESE_FORMAT_RULE = """
XITOYCHA MATN FORMATI (HECH QACHON BUZMANG):
- Har qanday xitoycha so'z, ibora yoki jumla FAQAT shu 3 qatorli formatda beriladi:
  <b>汉字</b>
  <code>pīnyīn</code>
  tarjima
- Xitoychani bitta qatorda "<b>汉字</b> [<code>pinyin</code>] — tarjima" ko'rinishida yozma.
- Bir nechta xitoycha birlik bo'lsa, har bir birlik orasida bitta bo'sh qator qoldir.
- Pinyin har doim tone belgilar bilan yozilsin.
- Tarjima foydalanuvchi tanlagan tilda bo'lsin.
"""

# MUHIM QOIDA — barcha tushuntirish bulimlari uchun (intro/vocab/dialogue/grammar)
_EXPLANATION_RULE = """
MUHIM QOIDA (ASOSIY VAZIFA):
- Sen HECH QACHON foydalanuvchiga mashq, savol yoki test bermaysan
- Sening vazifang: foydalanuvchiga hozirgi mavzuni tushuntirish
- Agar foydalanuvchi savol bersa — tushuntir, misollar keltir
- Agar foydalanuvchi xato yozsa: avval xatoni ko'rsat, keyin "Nega xato:" va "To'g'ri qilish uchun:" deb qisqa tushuntir
- Har bir javob oxirida yana biror narsani tushuntirishni TAKLIF qil
  (masalan: "Yana so'zlar haqida misollar xohlaysizmi?" yoki "Grammatika qoidasi haqida ko'proq aytaymi?")
- Aslo: "Endi mashq qilamiz", "Quyidagi savolga javob bering", "Sinab ko'ring" dema
"""


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

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Talabani bu darsga iliq kutib ol.

DARS MA'LUMOTLARI:
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasiga moslashtirilgan
- Jami 12 qatordan oshmasin, 90 so'zdan uzun bo'lmasin
- 2-3 ta so'z va asosiy grammatika mavzusini qiziqarli tarzda tanishtir
- Hali o'qitma — faqat tanishtir
- Oxirida "Tayyor? Ketdik! 🚀" kabi quvnoq gap bilan tugat ({user_language} tilida)
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""

        return prompt, data

    def _prompt_vocab(self, lesson, user_language, user_level) -> tuple:
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {"lesson_title": title, "vocabulary": vocab}

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Bu darsning so'zlarini qiziqarli tarzda o'rgat.

SO'ZLAR MA'LUMOTI:
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 8 ta asosiy so'zni tanla, javob 32 qatordan oshmasin
- Har bir so'z 3 qatorli xitoycha formatda bo'lsin
- Misol jumla kerak bo'lsa, u ham 3 qatorli xitoycha formatda bo'lsin
- O'xshash so'zlar bo'lsa (masalan 我/你, 大/小), ularni yonma-yon solishtir
- Izohlar juda qisqa bo'lsin: har so'zga maksimum 1 oddiy gap
- Foydalanuvchi savollarini tushuntir, keyin TAKLIF qil (masalan: "Yana qaysi so'z haqida ko'proq bilmoqchisiz?")
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""

        return prompt, data

    def _prompt_dialogue(self, lesson, user_language, user_level) -> tuple:
        dialogue = self._parse(getattr(lesson, "dialogue_json", None), [])
        title = self._safe(getattr(lesson, "title", ""))

        data = {"lesson_title": title, "dialogue": dialogue}

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Bu dialogni qadamma-qadam o'rgat.

DIALOG MA'LUMOTI:
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 4 ta dialog qatorini tushuntir, javob 26 qatordan oshmasin
- Har bir dialog qatori 3 qatorli xitoycha formatda bo'lsin
- Taqdimotdan keyin kontekstni qisqacha tushuntir (bu suhbat qayerda/qachon bo'ladi)
- Dialogdan 1-2 ta foydali iboralarni amaliy hayot bilan solishtirgan holda tushuntir
- Qo'shimcha izohlar 4 qisqa gapdan oshmasin
- Foydalanuvchi dialog haqida savol bersa — tushuntir va TAKLIF qil (masalan: "Ushbu ibora boshqa situatsiyalarda qanday ishlatiladi, ko'rmoqchimisiz?")
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""

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

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Grammatika qoidalarini aniq va qisqa tushuntir.

GRAMMATIKA MA'LUMOTI:
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 2 ta grammatika nuqtasini tushuntir, javob 28 qatordan oshmasin
- Har bir grammatika nuqtasi: 1 qisqa qoida + 1 naqsh + 1-2 misol
- Har bir xitoycha misol 3 qatorli xitoycha formatda bo'lsin
- O'xshash tuzilmalar bo'lsa (masalan 的/地/得, 吗/呢, 在/有), tezkor maslahat bilan solishtir
- Misollar FAQAT lesson_vocabulary so'zlaridan foydalansin
- Har bir izoh maksimum 2 gap bo'lsin
- Foydalanuvchi savol bersa tushuntir va TAKLIF qil (masalan: "Bu qoidani boshqa misollar bilan ko'rmoqchimisiz?")
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""

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

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Foydalanuvchi mashq javoblarini tekshir.

MASHQ MA'LUMOTI:
{json.dumps(data, ensure_ascii=False, indent=2)}

ASOSIY VAZIFA — JAVOBNI MAZMUN BO'YICHA TEKSHIR (FORMAT BO'YICHA EMAS):
- Foydalanuvchi xitoy belgilari, pinyin yoki ma'no yozishi mumkin — BARCHASI QABUL QILINADI
- HTML teglari (<b>, <code>) talab qilinmaydi — foydalanuvchi oddiy matn yozadi
- Har bir javobni FAQAT MAZMUN bo'yicha tekshir:
  * ✅ — ma'no/so'z to'g'ri bo'lsa
  * ❌ — ma'no/so'z noto'g'ri bo'lsa
- Noto'g'ri bo'lsa: TO'G'RI JAVOBNI 3 qatorli xitoycha formatda ko'rsat
- Noto'g'ri bo'lsa albatta yoz:
  * Nega xato: 1 qisqa gap
  * To'g'ri qilish uchun: 1 aniq maslahat
- Rag'batlantiruvchi bo'l: "Yaxshi! 👏" yoki "Deyarli to'g'ri! Mana maslahat..."

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Javob 16 qatordan oshmasin
- Keyingi bo'limga o'tish haqida HECH NARSA dema — tizim o'zi o'tkazadi
{_CHINESE_FORMAT_RULE}"""

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

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Foydalanuvchiga TEST savollarini ber.

TEST MA'LUMOTI:
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- BIRINCHI CHAQIRUVDA (foydalanuvchi xabari yo'q bo'lsa):
  * FAQAT 3-4 ta TEST SAVOLI ber — raqamlangan (1, 2, 3, 4)
  * Savol turlari: ko'p tanlovli (A/B/C/D) YOKI bo'sh to'ldirish
  * FAQAT test_vocabulary va test_grammar dan — tashqi so'z yo'q
  * Tushuntirma, izoh, so'z ma'nolari BERMA — faqat savollar
  * Savoldagi har bir xitoycha matn 3 qatorli xitoycha formatda bo'lsin
  * Test savollari 18 qatordan oshmasin
- FOYDALANUVCHI JAVOB YUBORGANDA:
  * Har bir javobni tekshir: ✅ to'g'ri yoki ❌ noto'g'ri
  * Noto'g'ri bo'lsa: TO'G'RI JAVOBNI 3 qatorli xitoycha formatda ko'rsat
  * Noto'g'ri bo'lsa: "Nega xato:" va "To'g'ri qilish uchun:" deb 1 tadan aniq gap yoz
  * Umumiy ball ber (masalan: 3/4 ✅)
  * Tekshiruv javobi 18 qatordan oshmasin
- Rag'batlantiruvchi bo'l
{_CHINESE_FORMAT_RULE}"""

        return prompt, data

    def _prompt_satisfaction_check(self, lesson, user_language, user_level) -> tuple:
        title = self._safe(getattr(lesson, "title", ""))
        data = {"lesson_title": title}

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Talaba bu darsni tushunganini tekshir.

DARS: {title}

QOIDALAR:
- Faqat {user_language} tilida javob ber
- BITTA oddiy savol ber: darsni tushundingizmi?
- Maksimal 2 qator
- Yangi kontent o'qitma
- Oldinga siljima — talabaning tugmalar orqali javobini kut
{_CHINESE_FORMAT_RULE}"""

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

        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Uy vazifasini baholash.

UY VAZIFASI MA'LUMOTI:
{json.dumps(data, ensure_ascii=False, indent=2)}

ASOSIY VAZIFA — FOYDALANUVCHI JAVOBINI TEKSHIR:
- Har bir bandni tekshir: ✅ to'g'ri yoki ❌ noto'g'ri
- Noto'g'ri bo'lsa: TO'G'RI JAVOBNI 3 qatorli xitoycha formatda ko'rsat
- Noto'g'ri bo'lsa albatta yoz:
  * Nega xato: 1 qisqa gap
  * To'g'ri qilish uchun: 1 aniq maslahat
- Ball ber: 0-100
- Nimasi yaxshi va nimani yaxshilash kerakligini aniq ayt
- Rag'batlantiruvchi va aniq bo'l

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 16 qator
{_CHINESE_FORMAT_RULE}"""

        return prompt, data

    def _prompt_vocab_1(self, lesson, user_language, user_level) -> tuple:
        """V2: birinchi 8 ta so'z."""
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        vocab_page = vocab[:8]
        title = self._safe(getattr(lesson, "title", ""))
        data = {"lesson_title": title, "vocabulary": vocab_page}
        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Bu darsning birinchi qismidagi so'zlarni qiziqarli tarzda o'rgat.

SO'ZLAR (1–8):
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 8 ta so'z ber, javob 32 qatordan oshmasin
- Har bir so'z 3 qatorli xitoycha formatda bo'lsin
- Misol kerak bo'lsa, u ham 3 qatorli xitoycha formatda bo'lsin
- Har bir so'z izohi maksimum 1 qisqa gap bo'lsin
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""
        return prompt, data

    def _prompt_vocab_2(self, lesson, user_language, user_level) -> tuple:
        """V2: 9+ so'zlar."""
        vocab = self._parse(getattr(lesson, "vocabulary_json", None), [])
        vocab_page = vocab[8:]
        title = self._safe(getattr(lesson, "title", ""))
        data = {"lesson_title": title, "vocabulary": vocab_page}
        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Bu darsning ikkinchi qismidagi so'zlarni o'rgat.

SO'ZLAR (9+):
{json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 8 ta so'z ber, javob 32 qatordan oshmasin
- Har bir so'z 3 qatorli xitoycha formatda bo'lsin
- Misol kerak bo'lsa, u ham 3 qatorli xitoycha formatda bo'lsin
- Har bir so'z izohi maksimum 1 qisqa gap bo'lsin
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""
        return prompt, data

    def _prompt_dialogue_n(self, lesson, user_language, user_level, n: int = 1) -> tuple:
        """V2: n-chi dialog bloki (grammar_notes inline)."""
        import json as _json
        dialogues = self._parse(getattr(lesson, "dialogue_json", None), [])
        block = dialogues[n - 1] if isinstance(dialogues, list) and len(dialogues) >= n else {}
        title = self._safe(getattr(lesson, "title", ""))
        data = {"lesson_title": title, "dialogue_block": block, "block_number": n}
        prompt = f"""Sen do'stona HSK xitoy tili o'qituvchisisан. Bu dialogni va unga bog'liq grammatikani qisqa tushuntir.

DIALOG MA'LUMOTI:
{_json.dumps(data, ensure_ascii=False, indent=2)}

QOIDALAR:
- Faqat {user_language} tilida javob ber, {user_level} darajasi
- Maksimal 4 ta dialog qatorini tushuntir, javob 26 qatordan oshmasin
- Har bir dialog qatori 3 qatorli xitoycha formatda bo'lsin
- Dialogdan 1-2 ta foydali ibora va grammar_notes ni qisqa tushuntir
- Qo'shimcha izohlar 4 qisqa gapdan oshmasin
{_CHINESE_FORMAT_RULE}
{_EXPLANATION_RULE}"""
        return prompt, data

    # ─── STEP ROUTER ────────────────────────────────────────────

    def _build_prompt_for_step(self, lesson, step: str, user_language: str, user_level: str) -> tuple:
        # V2 dialogue_N steps
        if step.startswith("dialogue_"):
            try:
                n = int(step.split("_", 1)[1])
            except (ValueError, IndexError):
                n = 1
            return self._prompt_dialogue_n(lesson, user_language, user_level, n)

        handlers = {
            "intro":               self._prompt_intro,
            "vocab":               self._prompt_vocab,
            "vocabulary":          self._prompt_vocab,
            # V2 vocab steps
            "vocab_1":             self._prompt_vocab_1,
            "vocab_2":             self._prompt_vocab_2,
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
            full_text += f"\n\nFOYDALANUVCHI XABARI:\n{user_message}"

        response = await self.ai_service.generate_reply(
            text=full_text,
            user_language=user_language,
            user_level=user_level,
            history=history or [],
            model_override=COURSE_MODEL,
            max_completion_tokens=COURSE_MAX_COMPLETION_TOKENS,
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
- Set passed = true if score >= 60
- feedback_text must be in {user_language}, short and clear
- feedback_text must be max 8 lines and max 600 characters
- If the student is wrong, feedback_text must include:
  1. Why it is wrong
  2. How to avoid the same mistake next time
  3. The correct answer if needed
- Any Chinese word, phrase, or sentence inside feedback_text must follow this exact 3-line format:
  <b>汉字</b>
  <code>pīnyīn</code>
  translation in {user_language}
- Return ONLY valid JSON, nothing else:
{{"score": 0, "passed": false, "feedback_text": "..."}}"""

    async def evaluate_homework(self, user_language, user_level, lesson, submission_text) -> dict:
        submission_text = (submission_text or "").strip()
        if not submission_text:
            return {"score": 0, "passed": False, "feedback_text": "Javob bo'sh."}

        prompt = self._build_homework_evaluation_prompt(user_language, user_level, lesson, submission_text)

        raw = await self.ai_service.generate_reply(
            text=prompt,
            user_language=user_language,
            user_level=user_level,
            history=[],
            model_override=COURSE_MODEL,
            max_completion_tokens=HOMEWORK_EVALUATION_MAX_COMPLETION_TOKENS,
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
