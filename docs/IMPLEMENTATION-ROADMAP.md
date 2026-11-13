# PrideMediaDB Implementation Roadmap

> This roadmap connects the existing Project 3 planning, ERD, relational schema, wireframes, backlog and assessment requirements to the Django implementation. It uses the existing design work; it is not a proposal to start again.

## 1. Project rules and sources

- Repository: https://github.com/David-CB-UK/PrideMediaDB
- Preserve the existing homepage and individual film-detail wireframes. Do not recreate or replace them unnecessarily.
- The conceptual ERD and ERDPlus relational schema are planning artefacts: a starting point, not a requirement to turn every proposed entity into a model/table.
- Before implementing models, compare the actual ERD and schema with the Must-have backlog and acceptance criteria. Record justified changes.
- TDD is required: write a failing test for each behaviour before implementing it, make it pass, then refactor.
- Use Django authentication and Django admin where they meet requirements. A separate custom film-management or suggestion-review interface is not planned for the current release.
- Current Won't-have scope includes Where to Watch, Plex integration, separate favourites, personalised recommendations, social/sharing functionality, notifications/messaging and broad streaming aggregation.
- Follow the existing MoSCoW allocation: Must 18 points (60%), Should 6 (20%), Could 6 (20%). Do not silently promote future features into Must scope.

## 2. How the existing work connects

| Existing artefact | Implementation destination | Purpose |
|---|---|---|
| User goals, user stories and acceptance criteria | Tests, views, forms, permissions and templates | Define behaviour and completion |
| Conceptual ERD | Django model design | Candidate entities and relationships |
| ERDPlus relational schema | Model fields, foreign keys, many-to-many relationships and constraints | Database starting point to review |
| Homepage and page wireframes | HTML templates and reusable components | Page structure and visual hierarchy |
| Dark/light palettes, rainbow gradient and branding | CSS variables and reusable classes | Consistent visual identity |
| MoSCoW backlog and GitHub issues | Implementation sequence | Protect assessed scope |
| TDD/testing plan | Automated tests | Verify each behaviour as it is built |

The implementation chain is:

**User story and acceptance criteria → ERD/schema decision → Django model → test → view/form/URL → HTML template → CSS/JavaScript → browser and responsive checks.**

Not every page needs a new model. Not every ERD entity needs its own page. Not every visual element needs JavaScript.

## 3. Data model implementation map

This is a requirements-based mapping, not a claim that the final model design has already been approved. Verify exact fields, cardinalities, uniqueness rules and deletion behaviour against the ERD image, relational schema and acceptance criteria before migrations.

| Data responsibility | Likely Django implementation | Used by |
|---|---|---|
| Film catalogue | Film model | Homepage, browse/search, film detail, admin |
| Accounts | Django built-in User/authentication | Login, registration, dashboard and ownership |
| User rating | Rating linked to User and Film | Film detail, My Ratings |
| Written review | Review linked to User and Film, separate from Rating | Film detail, My Reviews |
| Watchlist membership | Watchlist or explicit user-film through model, as justified by ERD | Watchlist |
| Watched status/date | Watched or suitable explicit relationship model | Watched films, dashboard |
| User film suggestions | FilmSuggestion linked to submitting user, with moderation status | Suggest a Film, Django admin |
| LGBTQ+ categories | Reusable category model | Browse/discover, film detail |
| Film/category relationship | FilmRepresentation intermediary if relationship attributes/constraints require it; otherwise many-to-many | Film detail and representation discovery |
| Genres and themes | Reusable lookup models and relationships where required | Browse/search, film detail |
| Age rating | Lookup or field/model arrangement justified by ERD and requirements | Film detail and any in-scope filters |
| Language, country and subtitle metadata | Add only where supported by prioritised requirements and reviewed schema | Film detail and relevant filters |
| Collections and short-film groupings/series | Implement only to the extent required by Must-have catalogue requirements; richer ordering is Could-have | Discovery and film detail |
| External identifiers and ratings | Fields or related model only as required for planned API stories | Film detail and API enrichment |

Design rules:
- Ratings and written reviews are separate. A user can rate without writing a review.
- User-owned records belong to the authenticated user. Users must not edit or delete another user's records.
- Film suggestions remain pending until explicitly approved by an administrator; submission must not automatically add a public catalogue film.
- Watchlist and watched status are distinct. A watched film does not require a rating or review.
- Add database constraints, such as one rating per user per film, where confirmed by requirements.
- Django can create automatic many-to-many intermediary tables. Use explicit through models only where extra relationship data or constraints justify them.
- Do not implement deferred entities/features merely because they appeared in an early ERD draft.

## 4. Wireframe-to-template map

Use one shared base template and reusable CSS components. Logged-in/logged-out differences should normally be handled with authentication conditions and permissions, not duplicated whole sites.

| Existing wireframe / page | Suggested template | Django responsibility |
|---|---|---|
| Shared site shell | templates/base.html | Branding, navigation, theme assets, footer and content blocks |
| Logged-out and logged-in homepage | templates/home.html | Homepage sections; conditionally show member-specific content |
| Search and results | templates/films/browse.html or search_results.html | Search, filters, pagination; preserve active query/filter values |
| Individual film details | templates/films/film_detail.html | One Film plus representation, metadata, external ratings and reviews |
| My Account / dashboard | templates/accounts/dashboard.html | Current user's account/activity |
| Login | templates/registration/login.html | Django authentication |
| Registration | templates/registration/signup.html | Form validation and account creation |
| Watchlist and watched films | templates/accounts/watchlist.html | Current user's tracked films |
| My Ratings & Reviews | templates/accounts/my_reviews.html | Current user's ratings and optional reviews |
| Suggest a Film | templates/films/film_suggestion_form.html | Authenticated submission, pending moderation |
| Film management | Django admin | Staff-only catalogue management; no custom page planned |
| Film suggestion review | Django admin | Staff-only approval/rejection; no custom page planned |
| Custom 404 | templates/404.html | Branded not-found response |

The README wireframe section is the design reference. Where to Watch is explicitly a future enhancement and must not be included in the current film-detail implementation.

## 5. Shared visual system and CSS

Build the design system before styling every page. The documented visual direction is:
- Dark theme is primary, using deep navy and blue-grey surfaces.
- Light theme is a companion option, not a separate visual identity.
- Warm yellow is the main action/rating accent.
- Rainbow gradient is a restrained brand treatment for selected elements such as the wordmark, progress/rating bars, navigation highlights and badges.
- Representation labels should use relevant Pride-flag colours where appropriate, rather than applying the general brand gradient to every category.
- Mobile-first layouts must be checked at mobile, tablet and desktop sizes.

Suggested static structure (adapt to the actual Django project layout rather than creating duplicate folders):

    templates/
      base.html
      home.html
      films/
        browse.html
        film_detail.html
        film_suggestion_form.html
      accounts/
        dashboard.html
        watchlist.html
        my_reviews.html
      registration/
        login.html
        signup.html
      404.html

    static/
      css/style.css
      js/site.js
      images/

Suggested CSS layers:
1. Design tokens: theme colours, typography, spacing, radii and shadows.
2. Base styles: body, headings, links, focus states and images.
3. Shared layout: header, navigation, main container and footer.
4. Reusable components: buttons, forms, badges, alerts, film cards and rating display.
5. Page sections: hero/search, film grids, detail layout and account panels.
6. Theme variants: dark/light token values and theme switching.
7. Responsive rules: mobile-first breakpoints and layout changes.

Prefer reusable classes and CSS variables over one-off inline styling. Use semantic HTML and visible keyboard-focus states. Check colour contrast in both themes.

## 6. URL, view, form and permission responsibilities

| Feature | View/URL responsibility | Form and permission responsibility |
|---|---|---|
| Homepage | Select and order homepage film sections | Public access |
| Browse/search | Read search/filter parameters, return matching films and paginate | Validate filters; preserve parameters across pages |
| Film detail | Retrieve requested film and related data | Public read; member actions require authentication |
| Register/login/logout | Django authentication views or customised equivalents | Validate credentials and registration fields |
| Dashboard | Retrieve only the signed-in user's information | Login required |
| Watchlist/watched | Add/remove/update current user's film tracking | Login required; ownership enforced |
| Ratings/reviews | Create, display, update and delete user's contributions | Login required; ownership and uniqueness enforced |
| Film suggestion | Validate and save a pending suggestion | Login required; submitter cannot self-approve |
| Admin catalogue/moderation | Django admin | Staff/superuser permissions |

Use meaningful URL names and Django URL reversing in templates rather than hard-coded internal paths.

## 7. TDD implementation sequence

For every feature:
1. Read the user story and acceptance criteria.
2. Write a test for one expected behaviour and confirm it fails for the correct reason.
3. Implement the smallest model/view/form/template change needed.
4. Run relevant tests and make them pass.
5. Refactor without changing behaviour; rerun tests.
6. Check permissions, validation, accessibility and responsive behaviour relevant to the feature.
7. Commit the change and update its GitHub issue/Project Board and documentation.

### Phase 0 — Verify existing design before implementation
- Inspect the actual conceptual ERD and generated relational schema.
- Compare each proposed entity/relationship with Must-have backlog and acceptance criteria.
- Confirm core models, cardinalities, deletion behaviour, uniqueness constraints and required fields.
- Record which draft ERD elements are deferred or excluded, with reasons.
- Confirm current repository structure and settings before adding files.
- Do not run migrations until the model design has been reviewed.

### Phase 1 — Foundation and database
- Establish/check Django project and app structure.
- Configure settings, templates, static files and PostgreSQL for development and intended deployment.
- Implement reviewed core models.
- Add model tests for required fields, relationships, constraints and validation.
- Create and inspect migrations; apply to development database after review.
- Register suitable models in Django admin and test staff-only access.

### Phase 2 — Shared interface and responsive shell
- Build base.html from agreed branding and shared wireframe elements.
- Add CSS tokens for dark/light themes, typography, logo, navigation, footer, buttons, forms and alerts.
- Implement mobile-first layout and keyboard focus styling.
- Test the shell at mobile, tablet and desktop sizes before building all page content.

### Phase 3 — Public film discovery
- Build homepage sections using real database records.
- Build browse/search and pagination, preserving active search/filter parameters.
- Build film detail from the existing wireframe.
- Add representation and relevant metadata display.
- Test empty results, missing films, long titles, missing poster images and responsive film-card layouts.

### Phase 4 — Accounts and member features
- Implement registration, login and logout.
- Implement dashboard.
- Implement watchlist and watched status, including watched films without a rating/review.
- Implement ratings and reviews as separate but connected features.
- Test authentication, ownership, duplicate submissions, edit/delete permissions and validation.

### Phase 5 — Contributions and administration
- Implement film suggestion submission with pending status.
- Configure Django admin review and approval/rejection.
- Ensure approval is an explicit staff action and pending/rejected suggestions do not appear in the public catalogue.
- Test staff permissions and moderation state changes.

### Phase 6 — Should-have enhancements
Only after Must-have acceptance criteria are met:
- Additional film filtering.
- TMDb as the first external film API.
- External film links and ratings.
- Additional film metadata.
- Further accessibility/usability improvements.

### Phase 7 — Could-have features, if time permits
- Additional film API.
- Content warnings and parental guidance.
- Common Sense Media information.
- Awards/festival information.
- Richer collection/series ordering.

Do not implement Won't-have items in the current assessed release.

### Phase 8 — Final quality, deployment and evidence
- Run the complete automated test suite.
- Complete manual testing against acceptance criteria.
- Validate HTML/CSS and test responsive layouts, accessibility, forms, navigation and error handling.
- Check security settings, secrets and production database configuration.
- Deploy securely and verify the deployed application.
- Update README with implemented features, screenshots/mock-up, testing evidence, deployment instructions and honest limitations/reflections.

## 8. Feature-to-test traceability

| Feature | Essential test coverage |
|---|---|
| Models/database | Required fields, valid relationships, constraints and deletion behaviour |
| Homepage | Correct sections/records; empty catalogue handled |
| Search/browse | Matching, no results, invalid filters, pagination and query preservation |
| Film details | Correct film and related data; unknown film returns 404 |
| Representation | Correct categories and relationships displayed |
| Authentication | Registration validation, login/logout and protected pages |
| Watchlist/watched | Add/remove, ownership, duplicates, watched status/date, independent of rating |
| Ratings/reviews | Rating without review, optional review, edit/delete own item, cannot alter another's |
| Suggestions | Authenticated submission, pending default, validation, staff approval/rejection |
| Admin | Staff-only access and correct moderation/catalogue operations |
| Interface | Navigation, forms, feedback, keyboard access, theme contrast and responsiveness |
| Deployment | Production configuration, static/media handling as applicable, secure settings and smoke tests |

## 9. Progress and definition of done

Track progress against GitHub issues and acceptance criteria, not by counting templates or files alone.

A feature is complete only when:
- Its acceptance criteria are met.
- Relevant automated tests pass.
- Permissions and validation work.
- Its template matches the approved wireframe/design direction.
- Relevant responsive and accessibility checks are complete.
- The GitHub issue and project documentation accurately reflect the result.

Keep three states distinct in the README and project board:
- **Designed/planned** — present in ERD, backlog or wireframes.
- **Implemented** — present in the Django application and database.
- **Tested/verified** — supported by passing automated tests and recorded manual checks.

## 10. Immediate next action

Start with Phase 0, not with styling or building every page. Inspect the actual ERD and relational schema images, compare them against the Must-have backlog, and produce a reviewed model-and-relationship decision table. Only then proceed to Django models and TDD tests. This avoids coding a draft schema that does not match the assessed feature scope.
