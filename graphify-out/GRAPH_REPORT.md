# Graph Report - telegram_chinese_bot_clean  (2026-04-28)

## Corpus Check
- 246 files · ~281,704 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2104 nodes · 4620 edges · 42 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 1975 edges (avg confidence: 0.75)
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

## God Nodes (most connected - your core abstractions)
1. `UserRepository` - 95 edges
2. `add()` - 82 edges
3. `CourseLesson` - 66 edges
4. `t()` - 65 edges
5. `Response` - 47 edges
6. `build_from_json()` - 43 edges
7. `Request` - 42 edges
8. `main()` - 38 edges
9. `CourseEngineService` - 37 edges
10. `cluster()` - 37 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `text()`  [INFERRED]
  check_tables.py → graphify/worked/httpx/raw/models.py
- `clean()` --calls--> `text()`  [INFERRED]
  full_clean.py → graphify/worked/httpx/raw/models.py
- `process_level()` --calls--> `create()`  [INFERRED]
  app/bot/handlers/start.py → graphify/tests/fixtures/sample.ex
- `delete_user()` --calls--> `text()`  [INFERRED]
  scripts/delete_user.py → graphify/worked/httpx/raw/models.py
- `upgrade()` --calls--> `text()`  [INFERRED]
  alembic/versions/0002_add_messages.py → graphify/worked/httpx/raw/models.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (207): _cross_community_surprises(), _cross_file_surprises(), _file_category(), god_nodes(), graph_diff(), _is_concept_node(), _is_file_node(), _node_community_map() (+199 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (121): MyApp.Accounts.User, create(), validate(), admin_deleteuser_handler(), admin_giveaccess_handler(), admin_payment_approve_handler(), admin_payment_reject_handler(), admin_payment_reject_with_reason_handler() (+113 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (210): _check_tree_sitter_version(), _csharp_extra_walk(), extract(), extract_blade(), extract_c(), extract_cpp(), extract_csharp(), extract_dart() (+202 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (101): Exception, Auth, BasicAuth, BearerAuth, DigestAuth, NetRCAuth, Authentication handlers. Auth objects are callables that modify a request before, Load credentials from ~/.netrc based on the request host. (+93 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (72): Base, Base, DeclarativeBase, add(), CourseAttempt, CourseLesson, CourseProgress, Message (+64 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (125): _git_root(), _hooks_dir(), install(), _install_hook(), Walk up to find .git directory., Return the git hooks directory, respecting core.hooksPath if set (e.g. Husky)., Install a single git hook, appending if an existing hook is present., Remove graphify section from a git hook using start/end markers. (+117 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (22): admin_payment_reject_reason_select_handler(), handle_image_message(), _is_night(), payment_screenshot_handler(), _waiting_message(), admin_payment_review_keyboard(), admin_reject_reason_keyboard(), MessageRepository (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.03
Nodes (100): _detect_url_type(), _download_binary(), _fetch_arxiv(), _fetch_html(), _fetch_tweet(), _fetch_webpage(), _html_to_markdown(), ingest() (+92 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (73): build_graph(), Graph, Server, Return the first path component - used to detect cross-repo edges., Score how surprising a cross-file edge is. Returns (score, reasons)., _surprise_score(), _top_level_dir(), _bfs() (+65 more)

### Community 9 - "Community 9"
Cohesion: 0.04
Nodes (67): handle_delete(), handle_enrich(), handle_get(), handle_list(), handle_search(), handle_upload(), API module - exposes the document pipeline over HTTP. Thin layer over parser, va, Accept a list of file paths, run the full pipeline on each,     and return a sum (+59 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (70): Enum, classify_file(), convert_office_file(), count_words(), detect(), detect_incremental(), docx_to_markdown(), extract_pdf_text() (+62 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (58): _community_article(), _cross_community_links(), _god_node_article(), _index_md(), Return (community_label, edge_count) pairs for cross-community connections, sort, Generate a Wikipedia-style wiki from the graph.      Writes:       - index.md, _safe_filename(), to_wiki() (+50 more)

### Community 12 - "Community 12"
Cohesion: 0.04
Nodes (20): ApiClient, area(), Circle, Color, Config, describe(), Geometry, HttpClient (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.06
Nodes (44): find(), _body_content(), cache_dir(), cached_files(), check_semantic_cache(), clear_cache(), file_hash(), load_cached() (+36 more)

### Community 14 - "Community 14"
Cohesion: 0.07
Nodes (42): collect_files(), extract_python(), Extract classes, functions, and imports from a .py file via tree-sitter AST., After merging multiple files, no internal edges should be dangling., Call-graph pass must produce INFERRED calls edges., AST-resolved call edges are deterministic and should be EXTRACTED/1.0., Same input always produces same output., run_analysis() calls compute_score() - must appear as a calls edge. (+34 more)

### Community 15 - "Community 15"
Cohesion: 0.1
Nodes (24): BroadcastStates, OnboardingStates, bc_cancel(), bc_confirm(), bc_enter_text(), bc_lang_filter(), bc_level_filter(), bc_receive_text() (+16 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (11): _background_scheduler(), lifespan(), BaseMiddleware, create_bot(), main(), init_db(), DBSessionMiddleware, DbSessionMiddleware (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (13): CacheManager, createProcessor(), DataProcessor, Get-Data(), GraphifyDemo, IProcessor, Loggable, NetworkError (+5 more)

### Community 18 - "Community 18"
Cohesion: 0.1
Nodes (29): claude_install(), claude_uninstall(), Write the graphify section to the local CLAUDE.md., Remove the graphify section from the local CLAUDE.md., Tests for graphify claude install / uninstall commands., claude_install also writes .claude/settings.json with PreToolUse hook., Running claude_install twice does not duplicate the PreToolUse hook., Creates CLAUDE.md when none exists. (+21 more)

### Community 19 - "Community 19"
Cohesion: 0.19
Nodes (22): _estimate_tokens(), print_benchmark(), _query_subgraph_tokens(), Token-reduction benchmark - measures how much context graphify saves vs naive fu, Print a human-readable benchmark report., Run BFS from best-matching nodes and return estimated tokens in the subgraph con, Measure token reduction: corpus tokens vs graphify query tokens.      Args:, run_benchmark() (+14 more)

### Community 20 - "Community 20"
Cohesion: 0.11
Nodes (10): text(), delete_user(), main(), clean(), add messages table  Revision ID: 0002 Revises: 0001 Create Date: 2026-03-25, upgrade(), add payments table  Revision ID: 0006 Revises: 0005 Create Date: 2026-03-26, upgrade() (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (14): check_update(), _notify_only(), Check for pending semantic update flag and notify the user if set.      Cron-saf, Write a flag file and print a notification (fallback for non-code-only corpora)., Tests for watch.py - file watcher helpers (no watchdog required)., check_update returns True and is silent when needs_update flag is absent., check_update returns True and prints notification when flag exists., check_update never removes the needs_update flag (clearing is LLM's job). (+6 more)

### Community 22 - "Community 22"
Cohesion: 0.2
Nodes (15): assert_valid(), Validate an extraction JSON dict against the graphify schema.     Returns a list, Raise ValueError with all errors if extraction is invalid., validate_extraction(), test_assert_valid_passes_silently(), test_assert_valid_raises_on_errors(), test_dangling_edge_source(), test_dangling_edge_target() (+7 more)

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (6): Analyzer, compute_score(), normalize(), Fixture: functions and methods that call each other - for call-graph extraction, run_analysis(), _strip_diacritics()

### Community 24 - "Community 24"
Cohesion: 0.42
Nodes (8): admin_broadcast_handler(), admin_broadcast_info(), admin_deleteuser_info(), admin_giveaccess_info(), admin_menu_handler(), admin_menu_keyboard(), admin_stats_callback(), _is_admin()

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
Cohesion: 0.5
Nodes (2): run_async_migrations(), run_migrations_online()

### Community 30 - "Community 30"
Cohesion: 0.6
Nodes (2): ColorResolver, DefaultPalette

### Community 31 - "Community 31"
Cohesion: 0.5
Nodes (2): Settings, BaseSettings

### Community 32 - "Community 32"
Cohesion: 0.5
Nodes (1): add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (1): add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2

### Community 34 - "Community 34"
Cohesion: 0.5
Nodes (1): add selected plan type to users  Revision ID: 0008 Revises: 0007 Create Date: 20

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (1): add referrals and user discount fields  Revision ID: 0003 Revises: 0002 Create D

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (1): add expiry reminder sent at to users  Revision ID: 0010 Revises: 0009 Create Dat

### Community 37 - "Community 37"
Cohesion: 0.5
Nodes (1): add discount progress fields to users  Revision ID: 0007 Revises: 0006 Create Da

### Community 38 - "Community 38"
Cohesion: 0.5
Nodes (1): add bonus questions used to users  Revision ID: 0009 Revises: 0008 Create Date:

### Community 39 - "Community 39"
Cohesion: 0.5
Nodes (1): initial migration  Revision ID: 0001 Revises: Create Date: 2026-03-24

### Community 40 - "Community 40"
Cohesion: 0.5
Nodes (1): Transformer

### Community 41 - "Community 41"
Cohesion: 0.67
Nodes (1): graphify - extract · build · cluster · analyze · report.

## Knowledge Gaps
- **369 isolated node(s):** `Shown while waiting for 3 referrals — only back button.`, `Shown when 3/3 referrals reached — plan buttons + back.`, `add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026`, `add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2`, `add messages table  Revision ID: 0002 Revises: 0001 Create Date: 2026-03-25` (+364 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (5 nodes): `do_run_migrations()`, `env.py`, `run_async_migrations()`, `run_migrations_offline()`, `run_migrations_online()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (5 nodes): `ColorResolver`, `.accent()`, `.primary()`, `DefaultPalette`, `sample_php_static_prop.php`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (4 nodes): `admin_id_list()`, `config.py`, `Settings`, `BaseSettings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (4 nodes): `0005_add_daily_limit_offer_sent_at.py`, `downgrade()`, `add daily limit offer sent at  Revision ID: 0005 Revises: 0004 Create Date: 2026`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (4 nodes): `0004_add_trial_dates_to_users.py`, `downgrade()`, `add trial dates to users  Revision ID: 0004 Revises: 0003 Create Date: 2026-03-2`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (4 nodes): `0008_add_selected_plan_type_to_users.py`, `downgrade()`, `add selected plan type to users  Revision ID: 0008 Revises: 0007 Create Date: 20`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (4 nodes): `0003_add_referrals_and_user_discount_fields.py`, `downgrade()`, `add referrals and user discount fields  Revision ID: 0003 Revises: 0002 Create D`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (4 nodes): `0010_add_expiry_reminder_sent_at_to_users.py`, `downgrade()`, `add expiry reminder sent at to users  Revision ID: 0010 Revises: 0009 Create Dat`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (4 nodes): `0007_add_discount_progress_fields_to_users.py`, `downgrade()`, `add discount progress fields to users  Revision ID: 0007 Revises: 0006 Create Da`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (4 nodes): `0009_add_bonus_questions_used_to_users.py`, `downgrade()`, `add bonus questions used to users  Revision ID: 0009 Revises: 0008 Create Date:`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (4 nodes): `0001_initial.py`, `downgrade()`, `initial migration  Revision ID: 0001 Revises: Create Date: 2026-03-24`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (4 nodes): `Transformer`, `.forward()`, `.__init__()`, `sample.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (3 nodes): `__init__.py`, `__getattr__()`, `graphify - extract · build · cluster · analyze · report.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `add()` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 17`, `Community 19`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `Cookies` connect `Community 3` to `Community 2`, `Community 11`, `Community 15`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `build_from_json()` connect `Community 0` to `Community 8`, `Community 2`, `Community 11`, `Community 22`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 97 inferred relationships involving `str` (e.g. with `format_intro()` and `_fmt_date()`) actually correct?**
  _`str` has 97 INFERRED edges - model-reasoned connections that need verification._
- **Are the 71 inferred relationships involving `UserRepository` (e.g. with `User` and `Message`) actually correct?**
  _`UserRepository` has 71 INFERRED edges - model-reasoned connections that need verification._
- **Are the 80 inferred relationships involving `add()` (e.g. with `.create()` and `.create()`) actually correct?**
  _`add()` has 80 INFERRED edges - model-reasoned connections that need verification._
- **Are the 64 inferred relationships involving `CourseLesson` (e.g. with `CourseLessonRepository` and `Base`) actually correct?**
  _`CourseLesson` has 64 INFERRED edges - model-reasoned connections that need verification._