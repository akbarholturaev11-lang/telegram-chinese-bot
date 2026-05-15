# Graph Report - ..  (2026-05-16)

## Corpus Check
- 295 files · ~553,232 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2668 nodes · 6562 edges · 54 communities detected
- Extraction: 55% EXTRACTED · 45% INFERRED · 0% AMBIGUOUS · INFERRED: 2971 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]

## God Nodes (most connected - your core abstractions)
1. `UserRepository` - 164 edges
2. `t()` - 120 edges
3. `add()` - 91 edges
4. `CourseLesson` - 69 edges
5. `CourseEngineService` - 66 edges
6. `handle_text_message()` - 57 edges
7. `CourseAudioRepository` - 52 edges
8. `CourseTutorService` - 50 edges
9. `AIUsageBudgetService` - 47 edges
10. `Response` - 47 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `text()`  [INFERRED]
  check_tables.py → graphify/worked/httpx/raw/models.py
- `clean()` --calls--> `text()`  [INFERRED]
  full_clean.py → graphify/worked/httpx/raw/models.py
- `_ensure_bootstrap_columns()` --calls--> `text()`  [INFERRED]
  app/db/session.py → graphify/worked/httpx/raw/models.py
- `discount_confirm()` --calls--> `create()`  [INFERRED]
  app/bot/handlers/admin_discount.py → graphify/tests/fixtures/sample.ex
- `process_level()` --calls--> `create()`  [INFERRED]
  app/bot/handlers/start.py → graphify/tests/fixtures/sample.ex

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (176): MyApp.Accounts.User, create(), validate(), Server, admin_deleteuser_handler(), delete_user_command(), _clear_voice_mode(), command_language_callback_handler() (+168 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (253): _body_content(), cache_dir(), cached_files(), check_semantic_cache(), clear_cache(), file_hash(), load_cached(), Return set of file paths that have a valid cache entry (hash still matches). (+245 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (172): _cross_community_surprises(), _cross_file_surprises(), _file_category(), god_nodes(), graph_diff(), _is_concept_node(), _is_file_node(), _node_community_map() (+164 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (101): Exception, Auth, BasicAuth, BearerAuth, DigestAuth, NetRCAuth, Authentication handlers. Auth objects are callables that modify a request before, Load credentials from ~/.netrc based on the request host. (+93 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (106): Base, Base, DeclarativeBase, AdminAudioStates, AdminPortfolioStates, admin_audio_list_handler(), admin_back_keyboard(), admin_broadcast_handler() (+98 more)

### Community 5 - "Community 5"
Cohesion: 0.02
Nodes (165): _git_root(), _hooks_dir(), install(), _install_hook(), Walk up to find .git directory., Return the git hooks directory, respecting core.hooksPath if set (e.g. Husky)., Install a single git hook, appending if an existing hook is present., Remove graphify section from a git hook using start/end markers. (+157 more)

### Community 6 - "Community 6"
Cohesion: 0.02
Nodes (90): add(), _community_article(), _cross_community_links(), _god_node_article(), _index_md(), Return (community_label, edge_count) pairs for cross-community connections, sort, admin_stats_handler(), CourseLesson (+82 more)

### Community 7 - "Community 7"
Cohesion: 0.03
Nodes (121): find(), collect_files(), extract_python(), Extract classes, functions, and imports from a .py file via tree-sitter AST., _prepare_title_i18n(), _status_label(), course_go_dialogue(), course_go_exercise() (+113 more)

### Community 8 - "Community 8"
Cohesion: 0.03
Nodes (110): build_graph(), Graph, Return the first path component - used to detect cross-repo edges., Score how surprising a cross-file edge is. Returns (score, reasons)., _surprise_score(), _top_level_dir(), build(), build_from_json() (+102 more)

### Community 9 - "Community 9"
Cohesion: 0.04
Nodes (63): admin_payment_approve_handler(), admin_payment_reject_handler(), admin_payment_reject_with_reason_handler(), _is_night(), payment_screenshot_handler(), _waiting_message(), _admin_discount_choices(), _admin_discount_matrix() (+55 more)

### Community 10 - "Community 10"
Cohesion: 0.03
Nodes (100): _detect_url_type(), _download_binary(), _fetch_arxiv(), _fetch_html(), _fetch_tweet(), _fetch_webpage(), _html_to_markdown(), ingest() (+92 more)

### Community 11 - "Community 11"
Cohesion: 0.04
Nodes (38): _background_scheduler(), lifespan(), Run all lesson seed scripts in the background after startup., Run all lesson seed scripts in the background after startup., Run all lesson seed scripts in the background after startup., _seed_lessons(), BaseMiddleware, create_bot() (+30 more)

### Community 12 - "Community 12"
Cohesion: 0.03
Nodes (32): ApiClient, area(), CacheManager, Circle, Color, Config, createProcessor(), DataProcessor (+24 more)

### Community 13 - "Community 13"
Cohesion: 0.04
Nodes (67): handle_delete(), handle_enrich(), handle_get(), handle_list(), handle_search(), handle_upload(), API module - exposes the document pipeline over HTTP. Thin layer over parser, va, Accept a list of file paths, run the full pipeline on each,     and return a sum (+59 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (70): Enum, classify_file(), convert_office_file(), count_words(), detect(), detect_incremental(), docx_to_markdown(), extract_pdf_text() (+62 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (56): admin_discount_panel(), _admin_ids(), _delete_admin_input(), discount_cancel(), discount_confirm(), discount_custom_duration(), discount_disable(), discount_duration() (+48 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (39): Analyzer, compute_score(), normalize(), Fixture: functions and methods that call each other - for call-graph extraction, run_analysis(), _bfs(), _communities_from_graph(), _dfs() (+31 more)

### Community 17 - "Community 17"
Cohesion: 0.07
Nodes (17): BroadcastStates, DiscountStates, FeedbackStates, OnboardingStates, cmd_start(), _get_demo_lesson(), process_language(), process_level() (+9 more)

### Community 18 - "Community 18"
Cohesion: 0.06
Nodes (20): do_run_migrations(), ensure_version_column_width(), run_async_migrations(), run_migrations_online(), text(), delete_user(), main(), clean() (+12 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (22): bc_activity_filter(), bc_cancel(), bc_confirm(), bc_discount_filter(), bc_enter_text(), bc_lang_filter(), bc_level_filter(), bc_mode_filter() (+14 more)

### Community 20 - "Community 20"
Cohesion: 0.19
Nodes (22): _estimate_tokens(), print_benchmark(), _query_subgraph_tokens(), Token-reduction benchmark - measures how much context graphify saves vs naive fu, Print a human-readable benchmark report., Run BFS from best-matching nodes and return estimated tokens in the subgraph con, Measure token reduction: corpus tokens vs graphify query tokens.      Args:, run_benchmark() (+14 more)

### Community 21 - "Community 21"
Cohesion: 0.36
Nodes (1): ImageInputService

### Community 22 - "Community 22"
Cohesion: 0.48
Nodes (6): _add_column_if_missing(), downgrade(), _drop_column_if_exists(), _has_column(), add discount campaign title i18n  Revision ID: 0019_add_discount_campaign_title_, upgrade()

### Community 23 - "Community 23"
Cohesion: 0.48
Nodes (6): _add_column_if_missing(), downgrade(), _drop_column_if_exists(), _has_column(), add discount campaign reason i18n  Revision ID: 0020_add_discount_campaign_reaso, upgrade()

### Community 24 - "Community 24"
Cohesion: 0.43
Nodes (6): EventServiceProvider, NotifyAdmins, OrderPlaced, SendWelcomeEmail, ShipOrder, UserRegistered

### Community 25 - "Community 25"
Cohesion: 0.53
Nodes (4): Get-PyVenvConfig(), global:deactivate(), global:_OLD_VIRTUAL_PROMPT(), global:prompt()

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (5): Animal, -initWithName, -speak, Dog, -fetch

### Community 27 - "Community 27"
Cohesion: 0.67
Nodes (4): AppServiceProvider, CashierGateway, PaymentGateway, StripeGateway

### Community 28 - "Community 28"
Cohesion: 0.6
Nodes (2): ColorResolver, DefaultPalette

### Community 29 - "Community 29"
Cohesion: 0.5
Nodes (2): Settings, BaseSettings

### Community 30 - "Community 30"
Cohesion: 0.5
Nodes (1): add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026

### Community 31 - "Community 31"
Cohesion: 0.5
Nodes (1): add course_audio table for storing telegram file_ids  Revision ID: 0015_add_cour

### Community 32 - "Community 32"
Cohesion: 0.5
Nodes (1): add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (1): add reminder_prompt_count to course_progress  Revision ID: 0014_add_reminder_pro

### Community 34 - "Community 34"
Cohesion: 0.5
Nodes (1): add ai usage budgets  Revision ID: 0022_add_ai_usage_budgets Revises: 0021_add_b

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (1): add weekly progress fields  Revision ID: 0017_add_weekly_progress_fields Revises

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (1): add course_promo_sent to users  Revision ID: 0016_add_course_promo_sent Revises:

### Community 37 - "Community 37"
Cohesion: 0.5
Nodes (1): add selected plan type to users  Revision ID: 0008 Revises: 0007 Create Date: 20

### Community 38 - "Community 38"
Cohesion: 0.5
Nodes (1): add referrals and user discount fields  Revision ID: 0003 Revises: 0002 Create D

### Community 39 - "Community 39"
Cohesion: 0.5
Nodes (1): add user voice mode  Revision ID: 0023_add_user_voice_mode Revises: 0022_add_ai_

### Community 40 - "Community 40"
Cohesion: 0.5
Nodes (1): add expiry reminder sent at to users  Revision ID: 0010 Revises: 0009 Create Dat

### Community 41 - "Community 41"
Cohesion: 0.5
Nodes (1): add discount progress fields to users  Revision ID: 0007 Revises: 0006 Create Da

### Community 42 - "Community 42"
Cohesion: 0.5
Nodes (1): add payment message ids for cleanup on approve  Revision ID: 0012_add_payment_ms

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (1): add bonus questions used to users  Revision ID: 0009 Revises: 0008 Create Date:

### Community 44 - "Community 44"
Cohesion: 0.5
Nodes (1): add reminder_tz_offset and last_reminder_sent_at to course_progress  Revision ID

### Community 45 - "Community 45"
Cohesion: 0.5
Nodes (1): initial migration  Revision ID: 0001 Revises: Create Date: 2026-03-24

### Community 46 - "Community 46"
Cohesion: 0.5
Nodes (1): Transformer

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (1): graphify - extract · build · cluster · analyze · report.

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (1): Universal dispatcher: har qanday step nomi uchun formatlangan matn qaytaradi.

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): lesson.title oddiy string yoki JSON bo'lishi mumkin — xitoycha qismini qaytaradi

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): V2 darslar uchun universal 'Davom etamiz' tugmasi (audiosiz).

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): V2 vocab_1 / vocab_2 step: [🔉]  [▶️ Davom etamiz].

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): V2 dialogue_N step: [🔉]  [▶️ Davom etamiz].

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Keyingi o'qish vaqtini tanlash — inline tugmalar (ReplyKeyboard o'rniga).

## Knowledge Gaps
- **403 isolated node(s):** `AI tutor javobidan keyin: 'Tushundim' → keyingi bo'limga o'tish.`, `Shown while waiting for 3 referrals — only back button.`, `Shown when 3/3 referrals reached — plan buttons + back.`, `lesson.title oddiy string yoki JSON bo'lishi mumkin — xitoycha qismini qaytaradi`, `V2 darslar uchun universal 'Davom etamiz' tugmasi (audiosiz).` (+398 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 21`** (8 nodes): `image_input_service.py`, `ImageInputService`, `.get_image_content_type()`, `.get_image_file_id()`, `.get_image_mime_type()`, `.get_invalid_file_reason_key()`, `.is_photo_message()`, `.is_supported_image_message()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (5 nodes): `ColorResolver`, `.accent()`, `.primary()`, `DefaultPalette`, `sample_php_static_prop.php`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (4 nodes): `admin_id_list()`, `config.py`, `Settings`, `BaseSettings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (4 nodes): `0005_add_daily_limit_offer_sent_at.py`, `downgrade()`, `add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (4 nodes): `0015_add_course_audio.py`, `downgrade()`, `add course_audio table for storing telegram file_ids  Revision ID: 0015_add_cour`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (4 nodes): `0004_add_trial_dates_to_users.py`, `downgrade()`, `add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (4 nodes): `0014_add_reminder_prompt_count.py`, `downgrade()`, `add reminder_prompt_count to course_progress  Revision ID: 0014_add_reminder_pro`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (4 nodes): `0022_add_ai_usage_budgets.py`, `downgrade()`, `add ai usage budgets  Revision ID: 0022_add_ai_usage_budgets Revises: 0021_add_b`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (4 nodes): `0017_add_weekly_progress_fields.py`, `downgrade()`, `add weekly progress fields  Revision ID: 0017_add_weekly_progress_fields Revises`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (4 nodes): `0016_add_course_promo_sent.py`, `downgrade()`, `add course_promo_sent to users  Revision ID: 0016_add_course_promo_sent Revises:`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (4 nodes): `0008_add_selected_plan_type_to_users.py`, `downgrade()`, `add selected plan type to users  Revision ID: 0008 Revises: 0007 Create Date: 20`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (4 nodes): `0003_add_referrals_and_user_discount_fields.py`, `downgrade()`, `add referrals and user discount fields  Revision ID: 0003 Revises: 0002 Create D`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (4 nodes): `0023_add_user_voice_mode.py`, `downgrade()`, `add user voice mode  Revision ID: 0023_add_user_voice_mode Revises: 0022_add_ai_`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (4 nodes): `0010_add_expiry_reminder_sent_at_to_users.py`, `downgrade()`, `add expiry reminder sent at to users  Revision ID: 0010 Revises: 0009 Create Dat`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (4 nodes): `0007_add_discount_progress_fields_to_users.py`, `downgrade()`, `add discount progress fields to users  Revision ID: 0007 Revises: 0006 Create Da`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (4 nodes): `0012_add_payment_msg_ids.py`, `downgrade()`, `add payment message ids for cleanup on approve  Revision ID: 0012_add_payment_ms`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (4 nodes): `0009_add_bonus_questions_used_to_users.py`, `downgrade()`, `add bonus questions used to users  Revision ID: 0009 Revises: 0008 Create Date:`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (4 nodes): `0013_add_reminder_tz_and_last_sent.py`, `downgrade()`, `add reminder_tz_offset and last_reminder_sent_at to course_progress  Revision ID`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (4 nodes): `0001_initial.py`, `downgrade()`, `initial migration  Revision ID: 0001 Revises: Create Date: 2026-03-24`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (4 nodes): `Transformer`, `.forward()`, `.__init__()`, `sample.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (3 nodes): `__init__.py`, `__getattr__()`, `graphify - extract · build · cluster · analyze · report.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `Universal dispatcher: har qanday step nomi uchun formatlangan matn qaytaradi.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `lesson.title oddiy string yoki JSON bo'lishi mumkin — xitoycha qismini qaytaradi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `V2 darslar uchun universal 'Davom etamiz' tugmasi (audiosiz).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `V2 vocab_1 / vocab_2 step: [🔉]  [▶️ Davom etamiz].`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `V2 dialogue_N step: [🔉]  [▶️ Davom etamiz].`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `Keyingi o'qish vaqtini tanlash — inline tugmalar (ReplyKeyboard o'rniga).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `t()` connect `Community 0` to `Community 7`, `Community 9`, `Community 11`, `Community 15`, `Community 17`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `UserRepository` connect `Community 0` to `Community 4`, `Community 7`, `Community 9`, `Community 11`, `Community 15`, `Community 17`, `Community 19`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `_ensure_bootstrap_columns()` connect `Community 11` to `Community 18`, `Community 2`, `Community 6`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 138 inferred relationships involving `UserRepository` (e.g. with `User` and `Message`) actually correct?**
  _`UserRepository` has 138 INFERRED edges - model-reasoned connections that need verification._
- **Are the 115 inferred relationships involving `str` (e.g. with `_ensure_bootstrap_columns()` and `discount_title_for_lang()`) actually correct?**
  _`str` has 115 INFERRED edges - model-reasoned connections that need verification._
- **Are the 119 inferred relationships involving `t()` (e.g. with `course_review_offer_keyboard()` and `course_satisfaction_keyboard()`) actually correct?**
  _`t()` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Are the 89 inferred relationships involving `add()` (e.g. with `.create()` and `.create()`) actually correct?**
  _`add()` has 89 INFERRED edges - model-reasoned connections that need verification._