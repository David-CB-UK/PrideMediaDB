# Kometa YAML Import — Source Structure and Design

## 1. Purpose

This document records the structure of the Kometa YAML source used by PrideMediaDB and defines how it should be interpreted during catalogue import.

The source is:

`data/kometa/Movies-LGBT.yml`

The original source must remain unchanged by the importer.

The detailed source-field, annotation and re-import rules are maintained in the [Kometa YAML Source Preservation Specification](kometa-source-preservation-matrix.md). That specification is the working reference for what PrideMediaDB must preserve, interpret, defer or exclude.

## 2. AI assistance, accessibility and learning

This work was undertaken with **_substantial assistance from AI tools_**. AI guidance was an important part of making this technical investigation achievable, providing support with tasks that would otherwise have presented significant barriers to independent completion.

AI assistance was used to:

- Explain unfamiliar technical concepts, YAML structures and Python behaviour.
- Develop and refine commands to inspect and analyse the source data.
- Help identify patterns, inconsistencies and potential data-quality issues.
- Explore Kometa configuration behaviour and external metadata sources.
- Consider alternative approaches to catalogue importing, data modelling and source reconciliation.
- Translate the findings into documented requirements and potential implementation decisions.

The work remained directed by the project owner. Commands were run within the project environment, their outputs were reviewed, and findings were considered against the actual source data. Decisions about the project's requirements, data integrity, catalogue eligibility and intended behaviour were made through that collaborative process.

AI-generated explanations, suggestions and code are treated as assistance rather than automatically verified facts. Where appropriate, findings are checked against the source YAML, command output, relevant technical documentation and subsequent automated tests.

This approach reflects the project's commitment to accessible, supported learning and transparent use of AI, while retaining human oversight and responsibility for the resulting work.

## 3. Source provenance

- Source filename: `Movies-LGBT.yml`
- Working location: `data/kometa/Movies-LGBT.yml`
- Master source updated: 25 November 2026
- SHA-256: `5f356cf2c8c216325bbf1d42c4c0d17d540f901e7db7dba1b04df549dfe20437`
- Parser: PyYAML using the project's `UniqueKeyLoader`
- The source file is excluded from Git using `data/kometa/` in `.gitignore`.

The working copy was verified against the updated master source.

## 4. Overall catalogue structure

The YAML contains two top-level sections:

- `templates`
- `collections`

There are 2 templates and 87 collection definitions.

### 4.1 Master catalogue

`LGBTQ+ Collection` is the master catalogue containing the complete film list.

It uses an explicit `imdb_id` list and has the following fields:

| Field | Purpose |
|---|---|
| `template` | References the standard Collection template |
| `imdb_id` | Film IMDb identifiers |
| `collection_order` | `release.desc` |
| `file_poster` | Local Plex poster path |
| `sort_title` | Plex-specific collection display and sorting order |
| `item_genre` | Plex genre assignment |
| `item_label` | Plex labels |
| `summary` | Collection description |

The configured collection order is newest release first (`release.desc`).

The master list contains:

- 2,654 IMDb list entries.
- 2,594 unique, non-`None` IMDb identifiers.
- 58 IMDb identifiers occurring twice.
- Two entries with no IMDb identifier (`None`).

These figures describe the source list as it currently exists. They do not establish whether repeated entries are mistakes, and no entries should be removed without investigation.

### 4.2 Secondary collections

The remaining collections are overlapping groupings of films from the master catalogue.

Examples include:

- Boys on Film collections
- Short-film collections
- Horror collections
- Christmas collections
- Themed collections
- Film and television series collections

A film can belong to multiple secondary collections.

Collection membership must therefore be represented separately from film identity.

A film should not become multiple film records merely because it appears in several collections.

## 5. Templates

The source defines two templates.

### 5.1 Collection

The standard template contains:

| Field | Value |
|---|---|
| `optional` | `['poster']` |
| `url_poster` | `<<poster>>` |
| `sync_mode` | `sync` |
| `collection_order` | `release` |
| `sort_title` | `+!112_02_<<collection_name>>` |

Individual collection definitions can override template defaults.

For example, the master collection explicitly uses `release.desc`, rather than the template's default `release`.

### 5.2 LGBTQ_[Short]_Template

This template contains:

- A smart filter based on LGBTQ+ Plex labels
- Optional poster configuration
- Poster URL placeholder
- Synchronisation configuration
- Plex visibility settings
- A collection sort-title template

Individual short-film collections override the template's smart filter.

### 5.3 Template usage

| Template usage | Collections |
|---|---:|
| `Collection` | 50 |
| `LGBTQ_[Short]_Template` | 2 |
| No explicit template | 35 |
| **Total** | **87** |

All 35 collections without explicit templates have the same field combination:

- `imdb_id`
- `item_genre`
- `item_label`
- `sort_title`
- `summary`
- `url_poster`

The absence of a template reference does not mean that a collection is invalid.

## 6. Collection selection methods

The following selection fields have been identified.

| Selection field | Collections using it |
|---|---:|
| `imdb_id` | 66 |
| `imdb_list` | 3 |
| `tmdb_collection` | 13 |
| `tmdb_list` | 6 |
| `tmdb_person` | 2 |
| `tvdb_list` | 1 |
| `tvdb_show` | 1 |
| `smart_filter` | 2 |

These counts overlap. A collection can use multiple selection methods.

### 6.1 Combined selection methods

The following collections use more than one method:

| Collection | Selection methods |
|---|---|
| Heartstopper Collection | IMDb IDs, TVDb list, TVDb show |
| Strapped for Danger Collection | IMDb IDs, TMDb list |
| Christmas LGBTQ | IMDb IDs, IMDb lists |
| LGBTQ Horror | IMDb IDs, IMDb lists |
| Danny La Rue | IMDb IDs, TMDb person |
| Joe Orton | IMDb IDs, TMDb person |

Kometa documentation confirms that multiple builders can be used within one collection and their results combined.

The importer must retain the provenance of each selection source.

### 6.2 External reference formats

Observed value formats:

| Field | Observed format |
|---|---|
| `imdb_list` | String or list of strings |
| `tmdb_collection` | Integer |
| `tmdb_list` | Integer |
| `tmdb_person` | Integer |
| `tvdb_list` | String containing a URL |
| `tvdb_show` | String containing an identifier |

Example references:

- IMDb list: `ls507989915`
- TMDb collection: `102008`
- TMDb person: `940070`
- TVDb show: `395494,`

The original values must be preserved, including their original data types and formatting.

### 6.3 Shared external references

The TMDb collection identifier `545187` is used by:

- Mascarpone Collection
- Mathias & Frederick Collection

These collections have different descriptions, posters, sorting titles and metadata.

A shared external reference does not mean that two Kometa collections should be merged.

## 7. Short-film collections

Two collections use `LGBTQ_[Short]_Template`.

### 7.1 LGBTQ+ Short - Micro

- Summary: LGBTQ+ short films under 10 minutes.
- Smart filter uses LGBTQ+ labels.
- Duration condition: `duration.lt: 10`.
- Adds the `Short` label.

### 7.2 LGBTQ+ Short

- Summary: LGBTQ+ short films between 10 and 50 minutes.
- Requires the `LGBTQ+` label.
- Duration conditions: `duration.gte: 10` and `duration.lt: 50`.
- Adds the `Short` label.

These are dynamic Plex smart-filter collections, not explicit IMDb membership lists.

The nested `item_label` structure (`[['Short']]`) must be preserved and investigated before implementing any normalisation.

## 8. Film classification

PrideMediaDB should distinguish film format from collection membership.

IMDb's `titleType` is a candidate external classification source.

Relevant values include:

- `short`
- `movie`
- `tvMovie`
- `tvShort`
- `tvSeries`

IMDb's bulk title basics dataset may provide a practical way to match the existing IMDb identifiers locally.

The IMDb classification should be evaluated independently of Kometa's smart-filter labels.

Television movies remain eligible works within the project.

## 9. Import design decisions

The following principles have been agreed.

### 9.1 Film identity

- Use verified IMDb identifiers as the primary identity reference where available.
- Do not create duplicate film records because a film belongs to multiple collections.
- Do not merge films based only on title and year.
- Preserve unresolved external references for review.

### 9.2 Collection membership

- Treat the master catalogue separately from secondary collections.
- Represent film-to-collection membership using a many-to-many relationship.
- Combine selection sources when resolving collection membership.
- Deduplicate final membership relationships without discarding source appearances.
- Preserve the provenance of each source that contributed a film.

### 9.3 Source preservation

- Never edit the original YAML during import.
- Preserve original identifiers and source values.
- Report missing, invalid or duplicate values rather than silently correcting them.
- Record unresolved external lookups separately from confirmed empty results.

### 9.4 Plex-specific metadata

Plex-specific presentation settings should not automatically become film attributes.

In particular:

- Ignore local `file_poster` paths during initial import.
- Artwork should be investigated through external metadata sources and APIs later.
- Do not treat Plex labels, sorting titles or visibility settings as authoritative film classifications.
- Collection descriptions and other useful metadata may be retained separately.

## 10. Initial source-data observations

Exploratory inspection of the current source identified the following.

### 10.1 Master collection

- 2,654 IMDb list entries.
- 2,594 unique non-`None` IMDb identifiers.
- 58 IMDb identifiers occurring twice.
- Two `None` entries.
- No IMDb identifiers occurring more than twice.

The two `None` entries were found at zero-based positions 2,076 and 2,491.

There were also four adjacent repeated-ID pairs. The remaining 54 repeated-ID occurrences were non-adjacent.

These findings are observations, not permission to modify the source. Repeated entries must be investigated before any correction or removal.

### 10.2 Other collections

Two other collections contained repeated IMDb identifiers:

- `Boys On Film 19. No Ordinary Boy` contains `tt8215338` twice, at positions 4 and 10.
- `My Own Private...` contains `tt2261871` twice, at positions 0 and 1. This collection contains no other entries.

These require source review before any correction.

Repeated appearances across different collections are expected and must not be confused with repeated identifiers within an individual collection.

## 11. Outstanding questions

The following require further investigation or implementation tests:

1. Exact behaviour of combined Kometa builders in the installed source configuration.
2. Behaviour when an external list or collection cannot be retrieved.
3. Duplicate handling during external source resolution.
4. Handling of the nested `item_label` structure.
5. Interpretation of the trailing comma in `tvdb_show`.
6. How to reconcile TMDb and TVDb references against existing IMDb film identities.
7. How to preserve source ordering and individual source appearances.
8. How to use IMDb `titleType` alongside the project's eligibility rules.
9. How to handle missing or invalid identifiers without losing source provenance.

These questions should remain open until supported by inspection or tests. Expected behaviour must not be recorded as confirmed behaviour without evidence.

## 12. Development approach

Implementation should follow Test Driven Development (TDD), as required by the project specification.

### 12.1 Completed initial work

The initial YAML reader has been implemented using PyYAML and the project's `UniqueKeyLoader`.

The following five automated tests have passed:

| Test | Purpose |
|---|---|
| `test_load_valid_yaml` | Checks that valid YAML can be loaded. |
| `test_load_missing_file` | Checks handling of a missing source file. |
| `test_load_invalid_yaml` | Checks handling of invalid YAML syntax. |
| `test_load_empty_yaml` | Checks handling of an empty YAML file. |
| `test_load_duplicate_keys` | Checks that duplicate mapping keys are rejected. |

The test command is:

```bash
python manage.py test catalogue_import.kometa.tests.test_yaml_reader
```

The latest recorded run completed all five tests successfully.

Detailed testing evidence is maintained separately in `docs/testing.md`.

### 12.2 Planned development sequence

1. Complete source-structure inspection.
2. Define source validation rules.
3. Write tests for master catalogue validation.
4. Write tests for secondary collection definitions.
5. Implement external reference handling.
6. Design Film and Collection models.
7. Implement many-to-many membership and provenance.
8. Test import behaviour and error handling.

Existing `docs/testing.md` remains the authoritative testing evidence document. This document records source structure and import design, not the complete test history.
