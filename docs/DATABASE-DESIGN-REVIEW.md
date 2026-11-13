# PrideMediaDB Database Design Review — Phase 0

**Status:** Initial review in progress — not approved for Django models or migrations  
**Purpose:** Compare the existing ERDPlus relational schema with the Must-have requirements before implementation.

## 1. Evidence checked

- `docs/PROJECT-BACKLOG.md` — Must/Should/Could/Won't priorities and core data requirements.
- `README.md` — database design notes and the stated purpose of the ERDPlus diagrams.
- `assets/images/readme-images/relational-schema.png` — visually inspected.
- Repository root — currently contains `.github/`, `.vscode/`, `README.md`, `assets/`, `docs/` and a basic `index.html`.

The conceptual ERD image is present in the repository, but the connected file retrieval returned no image content for that file. Its entities and relationships therefore remain to be checked visually. This review does not pretend that the conceptual diagram has been fully verified.

No Django project, app, `models.py`, `manage.py` or Django settings file was found in the repository root or GitHub code search during this check. Confirm the intended starting point before creating the Django structure.

## 2. Requirement-to-schema review

| Requirement / data area | What the current relational schema appears to contain | Initial assessment / action |
|---|---|---|
| Film catalogue | `FILM` with title, release date, runtime, synopsis, language, subtitles, identifiers, poster/art/trailer and timestamps | Core entity is present. Confirm required vs optional fields and whether every catalogue item should be a Film or a broader Media record. |
| Film/media types | `MEDIA`, `MEDIATYPE`, and a link from `FILM` to `MEDIA` | Needs clarification. Avoid two competing records for the same film. Decide whether Media is a parent/supertype, a separate asset, or unnecessary for the first release. |
| User accounts | A custom `USER` table with username, email, password hash and account flags | Prefer Django's built-in authentication user model for passwords and authentication. Only add a profile model if extra user-specific fields are genuinely needed. |
| Ratings | `RATES` linked to user and film | Good separation from written reviews. Confirm one rating per user per film and the allowed rating scale. |
| Written reviews | `REVIEW` linked to user and film | Keep separate from Rating so a rating can exist without a written review. Confirm whether one review per user per film is intended. |
| Watchlist | `WANTS TO WATCH` linked to user and film | Maps to a user-film relationship. Add uniqueness so the same film cannot be added twice by the same user. |
| Watched status | `HAS WATCHED` linked to user and film, with watched date | Keep distinct from watchlist and ratings. Confirm whether a film can be both watched and still on a watchlist. |
| Film suggestions | `FILMSUGGESTION` with title, identifiers, reason, status, admin notes and user link | Supports the Must-have suggestion workflow. Confirm pending as the default status and staff-only approval/rejection. |
| LGBTQ+ representation | `LGBTQ+CATEGORY`, `HAS REPRESENTATION`, and `HAS IDENTITY/STATUS` | Relationship needs inspection. The displayed schema appears to put `film_id` on the category table while the junction table shows only `film_id`; a proper film-to-category link normally needs both foreign keys in the junction. |
| Genres | `GENRE` and `HAS GENRE` | Appropriate many-to-many pattern: confirm the junction has both film and genre foreign keys and prevents duplicate pairs. |
| Languages | `LANGUAGE` and `HAS LANGUAGE` | Appropriate lookup plus relationship pattern if a film can have multiple languages. English-subtitle availability is also shown on Film; confirm its intended meaning and whether it is a simple yes/no field. |
| Countries | `COUNTRY` and `HAS COUNTRY` | Appropriate many-to-many pattern if films can have multiple countries. |
| Age ratings | `AGE RATING` and a `HAS` table linking film and age rating | Clarify whether each film has one rating or multiple ratings by country/classification system. A single rating may be a direct Film foreign key; multiple jurisdiction-specific ratings need a more explicit relationship. |
| Collections | `COLLECTION` and `BELONGS TO COLLECTION`, including collection order | Good starting point for ordered collections. Confirm whether a film may belong to multiple collections and whether short-film collections are represented here. |
| Series | `SERIES` and a Film/Media relationship | Possible overlap with Collection and Media. Define the difference between a series and a collection before implementation. |
| External identifiers | IMDb, TMDb and TVDb identifiers appear on Film; external rating data appears separately | Retain the identifiers required by the Must-have data scope. API integration and external ratings remain Should-have work, not a reason to build the API now. |
| External ratings | `EXTERNALRATING` linked to Media | Defer implementation until the Should-have story is reached. First confirm whether it belongs to Film or Media. |
| Content warnings | `CONTENTWARNING` and film-warning link | Content warnings are Could-have in the backlog; do not let this expand the initial schema without a later scope decision. |
| People and credits | `PERSON` and `MEDIA_PERSON` | Not clearly required by the current Must-have stories. Defer unless an accepted user story requires cast/crew information. |
| Similar-film suggestions | `SIMILARFILMSUGGESTION` and a related field on Film | Personalised recommendations are Won't-have for this release. Exclude from the initial implementation unless this table serves a separately approved, essential purpose. |
| Plex source IDs | `FILM_PLEX_SOURCE_ID` | Plex integration is Won't-have. Exclude from the current release. |

## 3. Decisions confirmed so far

These reflect the user's answers during the Phase 0 review. They are design decisions in progress, not yet a complete approved schema.

1. **Film and Media:** Keep both concepts for the current design. The longer-term intention is for Media to support other media types, potentially including television and books, while Film holds film-specific information. The precise parent/child or one-to-one relationship still needs to be defined so the two records do not duplicate fields.
2. **LGBTQ+ representation:** Treat the relationship between Film and representation categories as many-to-many. The final implementation should use a valid relationship with both foreign keys and should not store a single film foreign key on the reusable category record.
3. **Age ratings:** Keep the current release simple; do not implement multiple country-specific/classification-system ratings now. Record this as a future extension, not a Must-have implementation requirement.
4. **Series and collections:** A Series represents related instalments or entries (for example, *Where Are the Bears? 1, 2, etc.*). A Collection is a curated group of films, potentially grouped by theme or another editorial criterion. The model should allow films to be grouped without treating every collection as a sequential series.
5. **Watchlist and watched:** User's preference has been recorded, but the exact behaviour needs one clarification before it is treated as final: should a watched film remain on the user's watchlist, or should it be removed automatically?

## 4. Remaining design decisions

6. **Ratings and reviews:** The backlog requires a rating to be possible without a written review. Keep Rating and Review separate unless later acceptance criteria say otherwise.
7. **Authentication:** Use Django's built-in authentication rather than implementing password storage and login in a custom User table.
8. **Film suggestions:** Use a pending-by-default suggestion workflow with explicit staff approval/rejection. Confirm the exact approval process and how the resulting catalogue Film retains a link to the original suggestion.

## 5. Scope protection

The first implementation should focus on the Must-have requirements in `docs/PROJECT-BACKLOG.md`.

- **Include in core design:** films/media, representation, genres/themes/categories, age ratings, artwork, languages/subtitles, collections/series, external identifiers, accounts, ratings/reviews, watchlist/watched and moderated film suggestions.
- **Defer to Should:** filtering enhancements, TMDb integration, external film links/ratings and additional metadata.
- **Defer to Could:** content warnings, Common Sense Media, awards/festivals, extra API and richer collection/series ordering.
- **Exclude from this release:** Plex integration, personalised recommendations, streaming aggregation, separate favourites, social/sharing and notifications/messaging.

## 6. Repository and implementation status

| Item | Status |
|---|---|
| Project backlog inspected | Done |
| README database notes inspected | Done |
| Relational schema visually inspected | Done — initial review only |
| Conceptual ERD visually inspected | Outstanding — image retrieval issue |
| Current repository structure checked | Done — currently a static HTML/planning repository; no Django project detected |
| Model and relationship decisions approved | Not yet |
| Django models written | Not started |
| Migrations created/applied | Not started |

## 7. Next Phase 0 actions

1. Complete visual inspection of the conceptual ERD and compare it to the relational schema.
2. Resolve the eight design questions above, using the Must-have acceptance criteria as the deciding authority.
3. Clarify watchlist behaviour and the suggestion approval workflow, then produce the approved model-and-relationship table, including cardinality, uniqueness, nullability and deletion behaviour.
4. Confirm whether the Django project is to be created in this repository or already exists elsewhere.
5. Only then begin the Django foundation and model tests. Do not create or apply migrations before the design is reviewed.

**Review rule:** The ERDPlus diagrams are planning evidence, not an instruction to reproduce every generated table. The implemented Django data model must satisfy the prioritised requirements with the simplest sound relationships.
