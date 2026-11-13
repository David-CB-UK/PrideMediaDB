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

## 3. Important design decisions still required

These are questions to settle before writing Django models:

1. **Film and Media:** Is Media intended to be a parent record for films, shorts and other media types, or does it duplicate Film?
2. **Representation:** What is the intended cardinality? A film can normally have several representation categories, and a category can apply to many films. If so, use a many-to-many relationship with a proper two-key junction.
3. **Age ratings:** Is one age rating stored per film, or can ratings vary by country/classification system?
4. **Collections and series:** What is the functional difference? Can one film belong to multiple collections or series?
5. **Watchlist and watched:** Can a user retain a film on their watchlist after marking it watched, or should marking watched remove it?
6. **Ratings and reviews:** Can a user submit a rating without a review? The backlog says yes; the database must support that.
7. **Authentication:** Use Django authentication rather than implementing password storage and login in a custom User table.
8. **Film suggestions:** Confirm the status workflow and how an approved suggestion becomes a catalogue Film without losing its submission history.

## 4. Scope protection

The first implementation should focus on the Must-have requirements in `docs/PROJECT-BACKLOG.md`.

- **Include in core design:** films/media, representation, genres/themes/categories, age ratings, artwork, languages/subtitles, collections/series, external identifiers, accounts, ratings/reviews, watchlist/watched and moderated film suggestions.
- **Defer to Should:** filtering enhancements, TMDb integration, external film links/ratings and additional metadata.
- **Defer to Could:** content warnings, Common Sense Media, awards/festivals, extra API and richer collection/series ordering.
- **Exclude from this release:** Plex integration, personalised recommendations, streaming aggregation, separate favourites, social/sharing and notifications/messaging.

## 5. Repository and implementation status

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

## 6. Next Phase 0 actions

1. Complete visual inspection of the conceptual ERD and compare it to the relational schema.
2. Resolve the eight design questions above, using the Must-have acceptance criteria as the deciding authority.
3. Produce the approved model-and-relationship table, including cardinality, uniqueness, nullability and deletion behaviour.
4. Confirm whether the Django project is to be created in this repository or already exists elsewhere.
5. Only then begin the Django foundation and model tests. Do not create or apply migrations before the design is reviewed.

**Review rule:** The ERDPlus diagrams are planning evidence, not an instruction to reproduce every generated table. The implemented Django data model must satisfy the prioritised requirements with the simplest sound relationships.
