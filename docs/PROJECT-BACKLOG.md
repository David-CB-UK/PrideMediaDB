# PrideMediaDB Project Backlog

## MoSCoW effort target

The PP3 planning baseline is prioritised by **effort**, not simply by the number of stories:

- **Must:** 18 points (60%)
- **Should:** 6 points (20%)
- **Could:** 6 points (20%)
- **Won't:** future development / deliberately outside the current assessed scope

This gives the project a clear 60/20/20 effort allocation while protecting core and assessment-critical work.

## Must — 18 points

1. Establish project foundation and planning — 1
2. Design and implement the database — 2
3. Implement the responsive application interface — 2
4. Browse and search films — 2
5. View film details — 2
6. Explore LGBTQ+ representation — 1
7. User registration and authentication — 2
8. Ratings and reviews CRUD — 2
9. Form validation and user feedback — 1
10. TDD and automated testing — 1
11. Secure cloud deployment — 1
12. Manage a personal Watchlist and watched status — 1
13. Suggest films for admin approval — 1

### Core data/features included within these stories

- Film/media records, including short films and short collections where required
- Genres, themes and categories
- Structured LGBTQ+ representation
- Age ratings
- Poster/artwork handling
- Spoken languages and English-subtitle availability
- Collections and series
- External identifiers needed for future/API enrichment
- Administrator data management and direct data entry
- User film suggestions with administrator approval/rejection
- Watchlist and watched status, including watched films without a rating/review
- Ratings and reviews, presented together in the user's My Reviews & Ratings area

## Should — 6 points

1. Filter films — 1
2. Integrate TMDb as the first external film API — 2
3. Add external film links and ratings — 1
4. Add additional film metadata — 1
5. Improve accessibility and usability — 1

## Could — 6 points

1. Integrate an additional film API — 2
2. Add content warnings and parental guidance — 1
3. Add Common Sense Media information — 1
4. Add awards and festival information — 1
5. Add richer collections and series ordering — 1

## Won't / Future Development

These ideas have been considered but are deliberately outside the current assessed PP3 scope:

- Where-to-watch / streaming aggregation
- Plex integration or synchronisation
- Separate favourites
- Personalised film recommendations
- Social/sharing functionality
- Notifications/messaging
- Comprehensive streaming aggregation
- Comprehensive awards database
- Full parental-guidance/classification system beyond the core age-rating requirement
- Extensive data provenance tracking
- Extensive multi-API/database integration
- Educational resources for teachers, schools and educational organisations
- Historical terminology/context as a broader future enhancement
- Advanced educational tooling or AI recommendations

## Epics

The project is organised into 15 epics _('epics' are there to group related areas of work into larger themes. They are a way of organising the project backlog, rather than individual tasks or user stories.)_ , each representing a major area of functionality or development within PrideMediaDB. These provide a high-level structure for grouping related user stories and development tasks.

1. Project Planning & UX
2. Database & Data Model
3. UX & Responsive Interface
4. Film Discovery
5. LGBTQ+ Representation
6. Age Ratings & Content Guidance
7. Accounts & Security
8. Ratings & Reviews
9. Watchlist & User Contributions
10. Film APIs & External Data
11. Administration
12. Accessibility & Usability
13. Testing & TDD
14. Deployment & Security
15. Future Development

## Planning and Agile approach

Planning and design activities support the development of the relevant epics and user stories. This includes creating wireframes, designing the database using ERDs, researching APIs and making technical decisions.

These activities are documented as part of the project planning and supporting evidence rather than being created as separate user stories where they do not represent a specific user requirement.

Existing design work, including the homepage and individual film page wireframes, will be used to inform implementation and project documentation rather than recreated unnecessarily.

As development progresses, requirements and priorities may be reviewed and refined. New features will normally be considered for the Should Have, Could Have or Won't Have categories before being added to the Must Have scope, helping to maintain a realistic development plan.

GitHub Issues are used to record individual user stories, their acceptance criteria and associated development tasks. The GitHub Project Board provides an overview of progress, while descriptive commits record changes made during development.

The GitHub issue history records user stories, acceptance criteria and tasks. Issues will be updated as development progresses, with small, descriptive commits for individual features and fixes.
