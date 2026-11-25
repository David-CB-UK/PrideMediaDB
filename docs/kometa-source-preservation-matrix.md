# Kometa YAML Source Preservation Specification

## 1. Purpose

This document defines how PrideMediaDB should interpret and preserve information from the Kometa `Movies-LGBT.yml` source.

The YAML is both a catalogue source and a source of curated collection definitions. It also contains useful information in comments following film identifiers. The importer must preserve that information rather than treating the YAML as a list of IMDb IDs alone.

This is a design specification for the importer. It does not authorise changing the source YAML, automatically correcting uncertain identities, or promoting unverified classifications.

## 2. Core principles

1. Preserve the original source text and its provenance.
2. Preserve every source appearance, including repeated appearances and original positions.
3. Use verified external identifiers to identify works; never merge on title/year alone.
4. Separate a work's identity from its collection memberships.
5. Separate representation, eligibility, genre, theme, format, language and runtime.
6. Preserve unknown or ambiguous annotations for later review.
7. Do not make artwork availability a condition of a successful catalogue import.
8. Re-imports must be repeatable and must not overwrite user-managed information.
9. Invalid source structure must reject the whole import; do not commit a partial catalogue.
10. Keep Kometa-only configuration out of PrideMediaDB's domain model unless a later, explicit requirement justifies retaining it.

## 3. Main film-list entry format

A film-list entry can contain:

- An IMDb identifier as the YAML list value.
- A comment beginning with `#`.
- A title in the comment after the identifier.
- A year/date in parentheses.
- An original or alternative title in braces, for example `{original title-Les Roseaux sauvages}`.
- Other details in square brackets or braces.
- Free-text explanatory notes.

The YAML parser (PyYAML) discards comments. Therefore, parsing the YAML into ordinary Python dictionaries and lists is not sufficient to preserve the source.

### Required reader behaviour

The importer must combine structured YAML parsing with a source-text reader that captures each list-entry line. For each appearance, retain at least:

- Source file name and source hash.
- Collection name.
- Original line number.
- Original position within the collection's source list.
- Leading IMDb identifier, if present.
- Entire original source line.
- Exact text after the comment marker.
- Raw bracketed and braced annotations, including their order and punctuation.
- Parsed values, where parsing is unambiguous.
- Parsing/review status and any warnings.

The original text is authoritative for provenance. Parsed fields are interpretations and must never replace the raw text.

A line that is commented out is not an active YAML list entry. It must not silently become a film or collection membership. However, relevant commented-out material may be reported for manual review where it contains a plausible identifier or useful note.

## 4. Annotation interpretation

### 4.1 Representation codes

The following meanings have been confirmed:

| Annotation | Meaning | Treatment |
|---|---|---|
| `[G]` | Gay | Representation category |
| `[L]` | Lesbian | Representation category |
| `[B]` | Bisexual | Representation category |
| `[T]` | Transgender | Representation category |
| `[Q]` | Queer or questioning | Representation category |
| `[NB]` | Non-binary | Representation category |
| `[I]` | Intersex | Representation category |
| `[G - minor]` | Gay representation through a minor supporting character | Gay representation plus a qualifier |
| `[LGBTQ+]` | General LGBTQ+ inclusion | Broad LGBTQ+ eligibility/scope annotation, not a substitute for specific representation |
| `[LGBTQ+ History]` | LGBTQ+ history | Theme |

Composite annotations such as `[G/B]`, `[T/NB]`, `[Q/T/NB/I]` and `[B, L]` represent multiple classifications. Split the codes into their constituent categories while preserving the original composite string.

Do not infer that every person represented in a film has every identity represented by a composite annotation. The annotation describes the film's classification, not necessarily the identity of a single character or person.

The label "queer interpretation" is not an established source annotation and must not be invented as a classification.

### 4.2 Themes and subjects

Confirmed interpretations include:

| Annotation | Treatment |
|---|---|
| `[Christmas]` | Film theme; should also be represented in the Christmas collection |
| `[LGBTQ+ History]` | Film theme |
| `[Drag]` | Theme/subject |

Where a film has a `[Christmas]` annotation but lacks an explicit appearance in the Christmas collection, the importer should identify the discrepancy. Any resulting membership must be recorded as annotation-derived, not misrepresented as an explicit YAML list appearance.

Other film-level genre/theme annotations, such as Horror and Comedy, are to be retained and mapped into the appropriate PrideMediaDB genre or theme taxonomy. The exact taxonomy and mappings still need to be agreed. Do not treat collection-level `item_genre` as an individual film's genre.

### 4.3 Formats and work types

Known examples include:

- `[Short]`
- `[Documentary]`
- TV Movie
- TV Series
- TV Mini Series
- Individual television episodes

Individual television episodes are eligible catalogue works where they meet the project's LGBTQ+ relevance criteria. The eventual data model must distinguish episodes from films and series and should link episodes to their parent series where that relationship is known.

### 4.4 Languages and subtitles

The user has confirmed that standalone language annotations (for example `[Swedish]`, `[Thai]` or `[French]`) refer to the original language.

Keep these concepts separate:

- Original language.
- Other spoken languages, where known.
- Subtitle languages.
- Original/alternative titles.

English subtitle annotations such as `[Eng Sub]`, `[English Sub]` or `[English Subtitle]` mean English subtitles are available, normally for a work not originally in English. They must not cause the film's original language to be recorded as English.

Preserve the exact source wording. Normalise obvious spelling variations for structured values only where the intended language is unambiguous; keep the original spelling in the source annotation.

A title in another language is not, by itself, proof of the film's original spoken language.

### 4.5 Runtime

Runtime annotations such as `[6min]`, `[8m]` or `[12 mins]` should be parsed into a duration in minutes where possible.

Preserve the original runtime text and its source appearance. API metadata may provide a preferred runtime, but the YAML runtime must remain available as a source observation. Compare conflicting values and flag material discrepancies rather than silently discarding either value.

For television series, an episode runtime must not be confused with the total duration of the series.

### 4.6 Titles and brace annotations

Preserve all brace annotations verbatim. Known patterns include:

- `{original title-...}`
- `{original-...}`
- `{English title-...}`
- `{also known as-...}` and `{aka ...}`
- `{dir-...}`
- `{imdb-...}`
- `{tmdb-...}`
- `{edition-...}`
- `{Language-...}`

Where unambiguous, extract alternative titles, director information, external identifier candidates, edition notes and language information into appropriate structured records. Preserve the complete original brace annotation as well.

An identifier embedded in a comment is not automatically a verified identifier for the leading IMDb entry. It must be reconciled and reviewed before it is used to merge or identify works.

### 4.7 Free-text notes and unknown annotations

Preserve all unrecognised square-bracket, brace and free-text content verbatim, with its collection and source-entry context. Flag it as unclassified for later review.

Unknown annotations must not cause a valid source import to fail merely because their meaning is not yet known. They must not be silently discarded or assigned an invented meaning.

## 5. Collection-level configuration

| YAML field | Decision | PrideMediaDB treatment |
|---|---|---|
| Collection key/name | Preserve | Collection name |
| `summary` | Preserve | Collection description |
| `imdb_id` | Preserve | Film identity reference and membership source |
| `imdb_list` | Preserve | Typed external collection/list source reference |
| `tmdb_collection` | Preserve | Typed external source reference |
| `tmdb_list` | Preserve | Typed external source reference |
| `tmdb_person` | Preserve | Typed external source reference |
| `tvdb_list` | Preserve | Typed external source reference |
| `tvdb_show` | Preserve | Typed external source reference |
| Multiple builders | Preserve source provenance | Resolve the resulting membership without duplicating the Film or active membership |
| `smart_filter` | Preserve for interpretation | Recreate using PrideMediaDB data only if the rule is agreed and supported |
| `item_label` | Collection-level only | Do not copy as an individual Film classification. The general LGBTQ+ label describes the relevant collection's scope |
| `item_genre` | Collection-level only | Preserve against the collection; do not assign automatically to every member Film |
| `url_poster` | Optional | May be used to retrieve collection artwork. Not essential to a successful import |
| `file_poster` | Do not import as a path | Local Plex path is not portable. Prefer application/API artwork; a local image may be uploaded separately if needed |
| `sort_title` | Do not import | Collection display ordering will be handled by PrideMediaDB |
| `collection_order` | Do not reproduce as Kometa configuration | Default collection-film display order in PrideMediaDB is release date/year. Preserve original source position separately |
| `template`, `optional` | Do not store in domain models | Kometa configuration only |
| `sync_mode` | Do not import | Plex synchronisation behaviour |
| `visible_home`, `visible_shared`, `visible_library` | Do not import | Plex visibility settings, not PrideMediaDB publication controls |

### Collection artwork

Artwork is not required for a valid catalogue import. Prefer obtaining film artwork through a supported metadata API when available. `url_poster` may provide an optional collection-artwork retrieval source or fallback. Do not depend on external URLs remaining available; where artwork is adopted, store an application-managed copy and retain its source/provenance.

### Collection ordering

The default display order for films within collections is release date/year, not Kometa's order. Retain original source positions to preserve provenance and allow later review or an explicitly curated ordering feature.

The collection's own display order is an application concern and should not depend on `sort_title`.

## 6. Short-film smart collections — decision pending

The source defines two dynamic short-film collection rules:

- Micro: LGBTQ+ labelled works with runtime under 10 minutes.
- Short: LGBTQ+ labelled works with runtime from 10 minutes up to, but not including, 50 minutes.

The user has not yet confirmed whether PrideMediaDB should automatically assign eligible works to these collections based on its own representation and runtime data, or whether membership should remain manually curated. Do not implement either behaviour until clarified.

Plex labels must not be treated as the source of truth for PrideMediaDB's eligibility rules.

## 7. Film identity, editions and episodes

### Film identity

Use verified external identifiers, with IMDb as the primary source identifier where available. Do not merge works based on title/year alone. Preserve missing, conflicting or unresolved identifiers for review.

### Different cuts and editions

The user's preference is to represent different cuts/editions as one Film record with edition details, rather than separate Film records by default. Preserve edition notes and all relevant source identifiers. Where different cuts have separate IMDb records, do not automatically merge those identifiers: verify the relationship and record the additional identifier against the Film only after reconciliation.

### Television episodes

Individual television episodes are eligible works where LGBTQ+ relevant. Preserve their work type and parent-series relationship where known. Further model details for episode numbering, seasons and series relationships remain to be designed.

## 8. Re-import behaviour

Imports should be versioned snapshots and idempotent.

1. Record the source filename, hash, import time and outcome.
2. Parse and validate the entire source before modifying the live catalogue.
3. Reject the whole import when required structure or any collection is invalid; do not apply a partial import.
4. Apply validated database changes in one transaction.
5. Re-importing the same source version must not create duplicate Films, collections or active memberships.
6. Preserve every source appearance, including repeated entries and differing annotations.
7. When a film is removed from a collection in a later source snapshot, withdraw that source-managed membership but retain the Film record.
8. When a film disappears from the master catalogue, withdraw its active membership in that source catalogue but retain the Film and all application data.
9. When a source-managed collection disappears, archive/deactivate it rather than permanently deleting it.
10. Do not overwrite user ratings, reviews, watchlists, watched status, suggestions or administrator-managed information.
11. Keep source-managed values separate from application/editorial overrides.
12. Preserve unresolved entries in an import-review record; do not invent identifiers or silently discard them.

## 9. Suggested data responsibilities

The final Django model design remains subject to the requirements review and TDD. The likely responsibilities are:

- Film: core work identity and film-level data.
- ExternalIdentifier: verified identifiers from IMDb, TMDb, TVDb and other sources.
- Collection: curated collection identity and description.
- CollectionMembership: Film-to-Collection relationship, active state and any application-level position/metadata.
- Source: identity of the YAML/catalogue source.
- ImportRun: source version, hash, date, status, counts and warnings.
- SourceAppearance: each individual source occurrence, including raw annotation text, line and position.
- AlternativeTitle: original and other known titles, including title type/language where known.
- Representation, Genre, Theme, Language and WorkType: structured classifications and metadata, linked to Films as appropriate.
- Edition details: information about cuts/editions attached to the Film without automatically creating a separate Film.
- Series/episode relationship: represent an eligible episode and link it to its series when known.

This is a conceptual responsibility list, not a commitment to create every item as a separate Django model. The final structure should be as simple as the project requirements permit.

## 10. Remaining ambiguities and review items

The following must be resolved or explicitly handled during implementation:

1. Whether the two short-film smart collections should dynamically populate from PrideMediaDB's own data or remain manually curated.
2. The complete controlled vocabulary and mapping for film-level genre/theme annotations beyond confirmed examples.
3. The full set of brace annotation formats and which can be parsed reliably.
4. How to represent a work with multiple original/spoken languages.
5. How to handle runtime discrepancies between YAML and API metadata.
6. How to reconcile multiple or conflicting external identifiers embedded in comments.
7. Exact series/season/episode relationships and episode metadata.
8. What happens when an edition/cut has its own IMDb identifier but is intended to be grouped under one Film record.
9. Which collection membership discrepancies, such as `[Christmas]` without explicit Christmas collection membership, may create inferred memberships and how administrators review them.
10. How API artwork selection, storage, refresh and fallback should work.

Items not yet decided must remain explicit open questions. The importer must preserve the original source information while those decisions are pending.
