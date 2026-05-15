# Graph Report - telegram_chinese_bot_clean  (2026-05-15)

## Corpus Check
- 295 files · ~548,411 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2639 nodes · 6438 edges · 54 communities detected
- Extraction: 55% EXTRACTED · 45% INFERRED · 0% AMBIGUOUS · INFERRED: 2898 edges (avg confidence: 0.74)
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
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]

## God Nodes (most connected - your core abstractions)
1. `UserRepository` - 154 edges
2. `t()` - 122 edges
3. `add()` - 90 edges
4. `CourseLesson` - 69 edges
5. `CourseEngineService` - 60 edges
6. `handle_text_message()` - 56 edges
7. `CourseTutorService` - 50 edges
8. `AIUsageBudgetService` - 48 edges
9. `Response` - 47 edges
10. `CourseAudioRepository` - 45 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `text()`  [INFERRED]
  check_tables.py → graphify/worked/httpx/raw/models.py
- `clean()` --calls--> `text()`  [INFERRED]
  full_clean.py → graphify/worked/httpx/raw/models.py
- `_ensure_bootstrap_columns()` --calls--> `text()`  [INFERRED]
  app/db/session.py → graphify/worked/httpx/raw/models.py
- `run_course_entry_flow()` --calls--> `create()`  [INFERRED]
  app/bot/handlers/course.py → graphify/tests/fixtures/sample.ex
- `discount_confirm()` --calls--> `create()`  [INFERRED]
  app/bot/handlers/admin_discount.py → graphify/tests/fixtures/sample.ex

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (133): admin_deleteuser_handler(), delete_user_command(), admin_payment_approve_handler(), admin_payment_reject_handler(), admin_payment_reject_reason_select_handler(), admin_payment_reject_with_reason_handler(), _clear_voice_mode(), command_language_callback_handler() (+125 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (145): add(), _node_community_map(), Generate questions the graph is uniquely positioned to answer.     Based on: AMB, Invert communities dict: node_id -> community_id., suggest_questions(), build(), build_from_json(), build_merge() (+137 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (210): _check_tree_sitter_version(), _csharp_extra_walk(), extract(), extract_blade(), extract_c(), extract_cpp(), extract_csharp(), extract_dart() (+202 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (101): Exception, Auth, BasicAuth, BearerAuth, DigestAuth, NetRCAuth, Authentication handlers. Auth objects are callables that modify a request before, Load credentials from ~/.netrc based on the request host. (+93 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (165): _git_root(), _hooks_dir(), install(), _install_hook(), Walk up to find .git directory., Return the git hooks directory, respecting core.hooksPath if set (e.g. Husky)., Install a single git hook, appending if an existing hook is present., Remove graphify section from a git hook using start/end markers. (+157 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (63): MyApp.Accounts.User, create(), validate(), Server, BroadcastStates, DiscountStates, FeedbackStates, OnboardingStates (+55 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (119): find(), _estimate_tokens(), print_benchmark(), _query_subgraph_tokens(), Token-reduction benchmark - measures how much context graphify saves vs naive fu, Print a human-readable benchmark report., Run BFS from best-matching nodes and return estimated tokens in the subgraph con, Measure token reduction: corpus tokens vs graphify query tokens.      Args: (+111 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (113): profile_menu_course(), _status_label(), _block_if_course_disabled(), course_audio_dialogue_handler(), course_audio_dialogue_n_handler(), course_audio_vocab_handler(), course_command_handler(), course_continue_handler() (+105 more)

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (64): AdminAudioStates, admin_audio_entry(), admin_audio_from_panel(), _after_upload_keyboard(), ask_for_audio_file(), audio_stats(), _audio_types_for_lesson(), _audio_types_keyboard() (+56 more)

### Community 9 - "Community 9"
Cohesion: 0.03
Nodes (100): _detect_url_type(), _download_binary(), _fetch_arxiv(), _fetch_html(), _fetch_tweet(), _fetch_webpage(), _html_to_markdown(), ingest() (+92 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (64): Base, Base, DeclarativeBase, AdminPortfolioStates, admin_audio_list_handler(), admin_broadcast_handler(), admin_broadcast_info(), admin_deleteuser_info() (+56 more)

### Community 11 - "Community 11"
Cohesion: 0.04
Nodes (87): build_graph(), Graph, _cross_community_surprises(), _cross_file_surprises(), _file_category(), god_nodes(), graph_diff(), _is_concept_node() (+79 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (78): bc_activity_filter(), bc_cancel(), bc_confirm(), bc_discount_filter(), bc_enter_text(), bc_lang_filter(), bc_level_filter(), bc_mode_filter() (+70 more)

### Community 13 - "Community 13"
Cohesion: 0.03
Nodes (32): ApiClient, area(), CacheManager, Circle, Color, Config, createProcessor(), DataProcessor (+24 more)

### Community 14 - "Community 14"
Cohesion: 0.04
Nodes (67): handle_delete(), handle_enrich(), handle_get(), handle_list(), handle_search(), handle_upload(), API module - exposes the document pipeline over HTTP. Thin layer over parser, va, Accept a list of file paths, run the full pipeline on each,     and return a sum (+59 more)

### Community 15 - "Community 15"
Cohesion: 0.05
Nodes (70): Enum, classify_file(), convert_office_file(), count_words(), detect(), detect_incremental(), docx_to_markdown(), extract_pdf_text() (+62 more)

### Community 16 - "Community 16"
Cohesion: 0.07
Nodes (19): _background_scheduler(), lifespan(), Run all lesson seed scripts in the background after startup., Run all lesson seed scripts in the background after startup., Run all lesson seed scripts in the background after startup., _seed_lessons(), BaseMiddleware, create_bot() (+11 more)

### Community 17 - "Community 17"
Cohesion: 0.07
Nodes (43): _body_content(), cache_dir(), cached_files(), check_semantic_cache(), clear_cache(), file_hash(), load_cached(), Return set of file paths that have a valid cache entry (hash still matches). (+35 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (39): Analyzer, compute_score(), normalize(), Fixture: functions and methods that call each other - for call-graph extraction, run_analysis(), _strip_diacritics(), _bfs(), _communities_from_graph() (+31 more)

### Community 19 - "Community 19"
Cohesion: 0.07
Nodes (42): collect_files(), extract_python(), Extract classes, functions, and imports from a .py file via tree-sitter AST., After merging multiple files, no internal edges should be dangling., Call-graph pass must produce INFERRED calls edges., AST-resolved call edges are deterministic and should be EXTRACTED/1.0., Same input always produces same output., run_analysis() calls compute_score() - must appear as a calls edge. (+34 more)

### Community 20 - "Community 20"
Cohesion: 0.06
Nodes (20): do_run_migrations(), ensure_version_column_width(), run_async_migrations(), run_migrations_online(), text(), delete_user(), main(), clean() (+12 more)

### Community 21 - "Community 21"
Cohesion: 0.17
Nodes (25): _community_article(), _cross_community_links(), _god_node_article(), _index_md(), Return (community_label, edge_count) pairs for cross-community connections, sort, Generate a Wikipedia-style wiki from the graph.      Writes:       - index.md, _safe_filename(), to_wiki() (+17 more)

### Community 22 - "Community 22"
Cohesion: 0.2
Nodes (15): assert_valid(), Validate an extraction JSON dict against the graphify schema.     Returns a list, Raise ValueError with all errors if extraction is invalid., validate_extraction(), test_assert_valid_passes_silently(), test_assert_valid_raises_on_errors(), test_dangling_edge_source(), test_dangling_edge_target() (+7 more)

### Community 23 - "Community 23"
Cohesion: 0.48
Nodes (6): _add_column_if_missing(), downgrade(), _drop_column_if_exists(), _has_column(), add discount campaign title i18n  Revision ID: 0019_add_discount_campaign_title_, upgrade()

### Community 24 - "Community 24"
Cohesion: 0.48
Nodes (6): _add_column_if_missing(), downgrade(), _drop_column_if_exists(), _has_column(), add discount campaign reason i18n  Revision ID: 0020_add_discount_campaign_reaso, upgrade()

### Community 25 - "Community 25"
Cohesion: 0.43
Nodes (6): EventServiceProvider, NotifyAdmins, OrderPlaced, SendWelcomeEmail, ShipOrder, UserRegistered

### Community 26 - "Community 26"
Cohesion: 0.53
Nodes (4): Get-PyVenvConfig(), global:deactivate(), global:_OLD_VIRTUAL_PROMPT(), global:prompt()

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (5): Animal, -initWithName, -speak, Dog, -fetch

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (4): AppServiceProvider, CashierGateway, PaymentGateway, StripeGateway

### Community 29 - "Community 29"
Cohesion: 0.6
Nodes (2): ColorResolver, DefaultPalette

### Community 30 - "Community 30"
Cohesion: 0.5
Nodes (2): Settings, BaseSettings

### Community 31 - "Community 31"
Cohesion: 0.5
Nodes (1): add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026

### Community 32 - "Community 32"
Cohesion: 0.5
Nodes (1): add course_audio table for storing telegram file_ids  Revision ID: 0015_add_cour

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (1): add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2

### Community 34 - "Community 34"
Cohesion: 0.5
Nodes (1): add reminder_prompt_count to course_progress  Revision ID: 0014_add_reminder_pro

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (1): add ai usage budgets  Revision ID: 0022_add_ai_usage_budgets Revises: 0021_add_b

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (1): add weekly progress fields  Revision ID: 0017_add_weekly_progress_fields Revises

### Community 37 - "Community 37"
Cohesion: 0.5
Nodes (1): add course_promo_sent to users  Revision ID: 0016_add_course_promo_sent Revises:

### Community 38 - "Community 38"
Cohesion: 0.5
Nodes (1): add selected plan type to users  Revision ID: 0008 Revises: 0007 Create Date: 20

### Community 39 - "Community 39"
Cohesion: 0.5
Nodes (1): add referrals and user discount fields  Revision ID: 0003 Revises: 0002 Create D

### Community 40 - "Community 40"
Cohesion: 0.5
Nodes (1): add user voice mode  Revision ID: 0023_add_user_voice_mode Revises: 0022_add_ai_

### Community 41 - "Community 41"
Cohesion: 0.5
Nodes (1): add expiry reminder sent at to users  Revision ID: 0010 Revises: 0009 Create Dat

### Community 42 - "Community 42"
Cohesion: 0.5
Nodes (1): add discount progress fields to users  Revision ID: 0007 Revises: 0006 Create Da

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (1): add payment message ids for cleanup on approve  Revision ID: 0012_add_payment_ms

### Community 44 - "Community 44"
Cohesion: 0.5
Nodes (1): add bonus questions used to users  Revision ID: 0009 Revises: 0008 Create Date:

### Community 45 - "Community 45"
Cohesion: 0.5
Nodes (1): add reminder_tz_offset and last_reminder_sent_at to course_progress  Revision ID

### Community 46 - "Community 46"
Cohesion: 0.5
Nodes (1): initial migration  Revision ID: 0001 Revises: Create Date: 2026-03-24

### Community 47 - "Community 47"
Cohesion: 0.5
Nodes (1): Transformer

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (1): graphify - extract · build · cluster · analyze · report.

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
- **402 isolated node(s):** `AI tutor javobidan keyin: 'Tushundim' → keyingi bo'limga o'tish.`, `Shown while waiting for 3 referrals — only back button.`, `Shown when 3/3 referrals reached — plan buttons + back.`, `lesson.title oddiy string yoki JSON bo'lishi mumkin — xitoycha qismini qaytaradi`, `V2 darslar uchun universal 'Davom etamiz' tugmasi (audiosiz).` (+397 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (5 nodes): `ColorResolver`, `.accent()`, `.primary()`, `DefaultPalette`, `sample_php_static_prop.php`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (4 nodes): `admin_id_list()`, `config.py`, `Settings`, `BaseSettings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (4 nodes): `0005_add_daily_limit_offer_sent_at.py`, `downgrade()`, `add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (4 nodes): `0015_add_course_audio.py`, `downgrade()`, `add course_audio table for storing telegram file_ids  Revision ID: 0015_add_cour`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (4 nodes): `0004_add_trial_dates_to_users.py`, `downgrade()`, `add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (4 nodes): `0014_add_reminder_prompt_count.py`, `downgrade()`, `add reminder_prompt_count to course_progress  Revision ID: 0014_add_reminder_pro`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (4 nodes): `0022_add_ai_usage_budgets.py`, `downgrade()`, `add ai usage budgets  Revision ID: 0022_add_ai_usage_budgets Revises: 0021_add_b`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (4 nodes): `0017_add_weekly_progress_fields.py`, `downgrade()`, `add weekly progress fields  Revision ID: 0017_add_weekly_progress_fields Revises`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (4 nodes): `0016_add_course_promo_sent.py`, `downgrade()`, `add course_promo_sent to users  Revision ID: 0016_add_course_promo_sent Revises:`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (4 nodes): `0008_add_selected_plan_type_to_users.py`, `downgrade()`, `add selected plan type to users  Revision ID: 0008 Revises: 0007 Create Date: 20`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (4 nodes): `0003_add_referrals_and_user_discount_fields.py`, `downgrade()`, `add referrals and user discount fields  Revision ID: 0003 Revises: 0002 Create D`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (4 nodes): `0023_add_user_voice_mode.py`, `downgrade()`, `add user voice mode  Revision ID: 0023_add_user_voice_mode Revises: 0022_add_ai_`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (4 nodes): `0010_add_expiry_reminder_sent_at_to_users.py`, `downgrade()`, `add expiry reminder sent at to users  Revision ID: 0010 Revises: 0009 Create Dat`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (4 nodes): `0007_add_discount_progress_fields_to_users.py`, `downgrade()`, `add discount progress fields to users  Revision ID: 0007 Revises: 0006 Create Da`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (4 nodes): `0012_add_payment_msg_ids.py`, `downgrade()`, `add payment message ids for cleanup on approve  Revision ID: 0012_add_payment_ms`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (4 nodes): `0009_add_bonus_questions_used_to_users.py`, `downgrade()`, `add bonus questions used to users  Revision ID: 0009 Revises: 0008 Create Date:`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (4 nodes): `0013_add_reminder_tz_and_last_sent.py`, `downgrade()`, `add reminder_tz_offset and last_reminder_sent_at to course_progress  Revision ID`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (4 nodes): `0001_initial.py`, `downgrade()`, `initial migration  Revision ID: 0001 Revises: Create Date: 2026-03-24`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (4 nodes): `Transformer`, `.forward()`, `.__init__()`, `sample.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (3 nodes): `__init__.py`, `__getattr__()`, `graphify - extract · build · cluster · analyze · report.`
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

- **Why does `add()` connect `Community 1` to `Community 0`, `Community 2`, `Community 6`, `Community 7`, `Community 8`, `Community 10`, `Community 11`, `Community 13`, `Community 14`, `Community 15`, `Community 18`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `t()` connect `Community 0` to `Community 16`, `Community 12`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `UserRepository` connect `Community 0` to `Community 5`, `Community 7`, `Community 8`, `Community 10`, `Community 12`, `Community 16`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 128 inferred relationships involving `UserRepository` (e.g. with `User` and `Message`) actually correct?**
  _`UserRepository` has 128 INFERRED edges - model-reasoned connections that need verification._
- **Are the 121 inferred relationships involving `t()` (e.g. with `course_review_offer_keyboard()` and `course_satisfaction_keyboard()`) actually correct?**
  _`t()` has 121 INFERRED edges - model-reasoned connections that need verification._
- **Are the 112 inferred relationships involving `str` (e.g. with `_ensure_bootstrap_columns()` and `discount_title_for_lang()`) actually correct?**
  _`str` has 112 INFERRED edges - model-reasoned connections that need verification._
- **Are the 88 inferred relationships involving `add()` (e.g. with `.create()` and `.create()`) actually correct?**
  _`add()` has 88 INFERRED edges - model-reasoned connections that need verification._