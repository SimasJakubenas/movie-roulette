### The Strategy Plane

For my personal project 4 with [Code Institute](https://codeinstitute.net/) I decided to tackle a simple yet very annoying and persistent problem my partner and I encounter on a weekly basis - picking a movie or a new TV show to watch on a sunday.
Even thought I'm sure we're not the only ones having this problem, I conducted several interviews to get an idea of how others go about deciding what the next movie they are going to watch is and if that's an issue for them also. These were some of the questions I asked:
* How often do you watch movies / TV shows? 
* What streaming providers are you using in your household?
* Do you find it difficult to pick your next watch?
* How much time do you think you spend picking a movie / TV show?
* Does this event cause any friction between you and your partner / family?
* What are your methods of picking a movie?

These are my findings:
* Most people I've spoken to watch movies / TV shows on a weekly basis.
* Most of them use one of the big streaming providers (Netflix, Amason Prime), some use 'of the market' free alternatives.
* Having to pick a movie is a problem of varying degree for different people, however the problem does arise at least sometimes and is some cases can cause arguments.
* The note worthy methods for picking your next watch were:
    * scrolling through different list on the streaming provider of choice
    * friends suggestions
    * using the search features to look for a specific actor / year of release

#### Problem Statement

"I'm a movie lover who wants a simple solution to be able to pick my next watch quickly, but I'm not able to do so, because of endless options available and lack of decisiveness, which at times can cause arguments in my household"

#### Target Audience

This website is for anyone who loves watching movies or TV shows and who at any time runs into an issue of actually pcking their next watch.

#### Competitor Analysis

To give me a better understanding of what my website would actually look like and where I could have an edge in, I've looked into 2 types of services.

##### Big name streaming providers

* Hight quality and well structured. +
* Full streaming service and good selection. +
* Narrowing down the offerrings to lists (like 'Popular') is good, but doesn't solve the issue we're trying to adress. +-
* No way to check for movies available on other platforms. -

##### Movie / TV show tracker websites

These are websites that access wast amounts of movie data by utilizing API's. A couple stood out from the ones I've investigated. Notably [MovieOfTheNight](https://www.movieofthenight.com/) and [Reelgood](https://reelgood.com/) latter of which is far more developed and has a movie randomiser feature I'm in search of. How ever I feel theres alot more functionality that could be added which would benefit the user. These would be my direct competitors.

## The Scope Plane

The scope is defined by  the user stories that were extracted from the problem statement in [the strategy plane](#the-strategy-plane) of  this readme. the user stories are organised into EPICS bellow.

### EPIC - New User Experience

<details>
<summary>
View User Stories
</summary>

As a **new user** I can **recognise the purpose of the site immediately** so that I can **be sure I'm in the right place**.

As a **new user** I can **navigate the site effortlessly** so that I can **get to the area of interest quickly**.

As a **new user** I have **a way of contacting the site admin** in case I have **any site related queries**.

As a **signed in user** I can **visit about page** so that I can **find out more about the site**.

</details>

### EPIC - Developer

<details>
<summary>
View User Stories
</summary>

As a **site developer** I can **showcase sites functionality prior to signing up** so that I have **a way of displaying what the site is all about to a potential user**.

As a **site developer** I can **display relevant links** so that I can **navigate a potential employer to my GitHub/LinkedIn**.

</details>

### EPIC - Authentication

<details>
<summary>
View User Stories
</summary>

As a **new user** I can **sign up my account** so that I have **an ability to use provided services**.

As a **new user** I can **log in to my accout** so that I can **use provided services**.

As a **signed in user** I can **log out my accound** so that **it remains secure**.

As a **registered user** I can **restore my password** so that **do so incase I forget it**.

</details>

### EPIC - Movies

<details>
<summary>
View User Stories
</summary>

As a **signed in user** I can **view lists of movies available to watch on the platforms that I use** so that I can **potentialy pick one of them to watch**.

As a **signed in user** I can **see more details about the movie** so that I can **decide if it's a right fit for me**.

</details>

### EPIC - TV Shows

<details>
<summary>
View User Stories
</summary>

As a **signed in user** I can **view lists of TV shows available to watch on the platforms that I use** so that I can **potentialy pick one of them to watch**.

As a **signed in user** I can **see more details about a TV show** so that I can **decide if it's a right fit for me**.

</details>

### EPIC - Search

<details>
<summary>
View User Stories
</summary>

As a **signed in user** I can **search movies or TV / shows by name** so that I can **locate it**.

As a **signed in user** I can **use an advanced search feature** so that I can **get suggestions based on my input**.

As a **search tool user** I can **choose weather I want movies or TV shows being displayed** so that I can **pick whats suitable for me**.

As a **search tool user** I can **choose a genre of my next watch** so that I can **narrow down the search results**.

As a **search tool user** I can **choose a release/aired year of my next watch** so that I can **narrow down the search results**.

As a **search tool user** I can **choose a runtime of of my next watch** so that I can **narrow down the search results**.

As a **search tool user** I can **creadible rating of my next watch** so that I can **narrow down the search results**.

As a **search tool user** I can **choose age restriction of my next watch** so that I can **narrow down the search results**.

As a **search tool user** I can **search for actors name** so that I can **narrow down the search results**.

As a **search tool user** I can **search for a word or a phrase** so that I can **narrow down the search results**.

</details>

### EPIC - My Lists

<details>
<summary>
View User Stories
</summary>

As a **signed in user** I can **add titles to my list** so that I can **keep a record of my intentions with those titles**.

As a **signed in user** I can **add remove titles from my lists** so that I can **keep my lists up to date**.

As a **signed in user** I can **add titles to a "don't show" list** so that I can **remove those titles from appearing on search and suggestions**.

</details>

### EPIC - Decision Maker

<details>
<summary>
View User Stories
</summary>

As a **signed in user** I can **use a randomising feature** so that I **don't have to make a decision myself**.

As a **roulette user** I can **select wheather I want the tool to show movies or TV shows** so that I **pick what's more suitable for me**.

As a **roulette user** I can **select wheather I want this tool to only select titles from my lists** so that I **can narrow down the possible outcomes greatly**.

    As a **roulette user** I can **manually add and remove titles to and from this tool** so that I **can have more control over it**.

As a **signed in user** I can **ask ChatGPT for suggestions** so that I have **a better time making a decision**.

</details>

### EPIC - Profile

<details>
<summary>
View User Stories
</summary>

As a **signed in user** I can **view my profile** so that I can **check if I'm happy woth my current details**.

As a **signed in user** I can **edit profile** so that I can **update my account details**.

As a **signed in user** I can **change my profile picture** so that I can **make my account more personalised**.

As a **signed in user** I can **delete profile** so that I can **stop using this service should I wish to do so**.

As the **site admin** I can **delete accounts** so that I can **remove users if a need for it arises**.

</details>

## The Structure Plane

the following diagrams depicts the information flow of the website.

<details>
<summary>
FlowChart
</summary>

![FlowChart for websites information flow](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/a1c245d8-8dfa-470c-ac10-a3053987843b)

</details>

<details>
<summary>
FlowChart Keys
</summary>

![flowchart keys](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/7aba63e5-01f0-4670-b514-8b192e8878a3)

</details>

<details>
<summary>
FlowChart
</summary>

the following ERD depicts relationships between database tables.

![ERD diagram](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/3973a2a4-8da2-4852-af4f-546b28bbdd21)

</details>

### Database Models

## The Skeleton Plane

The following wireframes demonstrate the intended design for the website for both mobile and desktop.

The website is split into two sections:
* Pre-authenticated User Experience (part of the website that can be accessed without logging in)
* Authenticated User Experience (unique to each user and can only be accessed by logging in)

### Pre-authenticated User Experience

This section consist of 4 pages and one modal each sharing the same header, footer and background.

<details>
<summary>
Landing Page
</summary>

Accessed by visiting main URL and pressing on the website logo in the top left corner.

![Wireframes for a Landing Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/9897a46e-4be4-4452-9907-3814f394a428)

</details>

<details>
<summary>
Sign In Page
</summary>

Accessed through menu on a button on the landing page.

![Wireframes for a Sign In Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/ebcf2ade-1449-42c7-8480-bc2c575465a8)

</details>

<details>
<summary>
Sign Up Page
</summary>

Accessed through menu.

![Wireframes for a Sign Up Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/583514a9-d674-47d6-ad86-07b55e05a0d3)

<details>
<summary>
Contact Page
</summary>

Accessed through menu on a link in the sign in page.

![Wireframes for a Contact Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/924688b5-c18f-4dfb-bf73-60150f44dee8)

</details>

### Authenticated User Experience

This section consists of 7 pages and 2 overlays each sharing the same header, footer and background.

<details>
<summary>
Movies Page
</summary>

Is navigated to once signed in. Can be accessed via the menu.

![Wireframes for a Movies Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/3165de47-1b94-488e-95eb-50f2a0739633)

</details>

<details>
<summary>
TV Shows Page
</summary>

Can be accessed via the menu.

![Wireframes for a TV Shows Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/80054b40-ea57-4a23-9d7b-91f78294d903)
</details>

<details>
<summary>
Roulette Page
</summary>

Can be accessed via the menu.

![Wireframes for a Roulette Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/eb63da99-8621-4a38-8606-9753c4ff3789)

</details>

</details>

<details>
<summary>
My Lists Page
</summary>

Can be accessed via the menu.

![Wireframes for a My Lists Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/0b06a80d-4540-4912-bd82-3d7a71136810)

</details>

<details>
<summary>
About Page
</summary>

Can be accessed via the menu.

![Wireframes for a About Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/60ce2732-6328-4200-aaf1-98cd7d0a163d)

</details>

<details>
<summary>
Search Page
</summary>

Can be accessed via the menu.

![Wireframes for a Search Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/d18a782a-6080-430a-b23c-791add117ba4)

</details>

<details>
<summary>
Profile Page
</summary>

Can be accessed via the menu for mobile or a link in the right top corner for desktop.

![Wireframes for a Profile Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/9171fd9e-60f8-40c1-93c5-8efac5dc0731)

</details>

<details>
<summary>
Watch Now Page
</summary>

Can be accessed by pressing on a movie in all pages that display movie posters.

![Wireframes for a Watch Now Page](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/d04f89b1-867e-4b29-95de-891260d81253)

</details>

## The Surface Plane

### Typography

As there's a lot of imagery on the site my main criteria for the fonts were: simplicity and readability. I've chosen sans serif fonts named bellow.

#### Headings

For headings accross the website **Be Vietnam Pro** was selected. I feel it stands out well amongs all the imagery that's present on the site and is clear to read.

(Insert Image)

#### Other Text

For any other text **Montserrat** font was selected. This font gives great seperation between headings and regular text with thinner letter without sacrificing readibility for the user.

(Insert Image)

### Colour Scheme

It's a no brainer to go for a dark theme when building a website of similar nature as is an industry standart and it sets the tone for a 'movie night'. The colour scheme for this website consists of range of different shades of gray and 2 highlight colours.

![Colour scheme for the website](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/10a17331-c1ce-4923-ad4a-0fe067fac5dc)

Background colours:
* dark-grey (54,54,54) user for background on all pages
* darker-gray (44, 42, 42, 0.94) user for overlay background
* highlight-blue (108, 229, 232, 0.1) user to highlight content background
* highlight-blue (108, 229, 232) used to highlight most button backgrounds
* highlight-red (232, 115, 108) used to highlight background of buttons with significant inpack on user experience

Text colours:
* off-white (250, 250, 250) for most text
* off-white (250, 250, 250, 0.85) for unselected menu items
* highlight-blue (108, 229, 232) user to highlight selected main menu item

## Agile Methodology

Agile values and principleswhile were followed (where possible) during developing of this project. However I have to admit working on a project as a solo contributer I was constantly fiting the urge to neglect these.

The Agile practices I've utilised were: user stories, story points and team velocity, product backlog, time boxing, prioritization and information radiators.

### User Stories

The User Storries are defined in The Scope Plane of this README. They were derived by breakdown the Epics detailing the main features of the platform into parts suitable for iterations..

The issues tool on GitHub has been used to record all user stories. I made a mistake of breaking down EPICS and defining User Stories acceptance criteria and tasks at the begining of the development which caused some inaccuracies (for expample allauth authomaticly generating certain things that I've listed in User Stories tasks).

### Story Points and Team Velocity

Story Points were used as an estimate to how long it would take to complete it. I used Fibonacci numbers (1, 2, 3, 5, 8) as a reference. Story points were recorded using labels attached to the user story. 

Team velocity was estimated and set to 25 for the first iteration and was lowered to 20 afterwards as I struggled more than I enticipated and didn't compleate all the 'must haves' on time. All of this was a shot in the dark at the beginning but got easier as I got more comfortable with Django.

### Product Backlog

A product backlog was used in which User Stories were stored and from which these User Stories were assigned to iterations. At the end of the iteration any User Stories that weren't closed were transfered back to backlog. I have to admit I could have done a better job at managing and prioritasing (this goes hand in hand with my mistake of breaking down EPICs at the start of the development)

The product backlog is visible on GitHub through the use of a milestone titled "Backlog" and a specific backlog column in the project board.

### Final Backlog

<details>
<summary>
Final Backlog
</summary>

![Final Backlog](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/67dc8c5e-a487-421a-9973-690b0c029da7)

</details>

### Time Boxing

Developement of the project was split into five iterations. Each iteration (with exeption of iteration IV which was shorted due to me having more free tiem) was set to a period of one week.
And I managed to go over the set time period for every iteration which I need to tighten up in the future work.

### Iteration I

<details>
<summary>
Closed Issues
</summary>

![Iteration I closed issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/5da266c0-ef80-4412-b1e4-b2c015b66a07)

<details>

<details>
<summary>
Open Issues
</summary>

![Iteration I open issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/ea3e325f-565a-4425-800c-4928e1dc5e37)

<details>

### Iteration II

<details>
<summary>
Closed Issues
</summary>

![Iteration II closed issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/90104c9b-be6f-4ef6-9104-9573cc47577f)

<details>

<details>
<summary>
Open Issues
</summary>

![Iteration II open issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/eeaf4543-ddea-415a-9a52-8983ef2e71c5)

<details>

### Iteration III

<details>
<summary>
Closed Issues
</summary>

![Iteration III closed issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/8ddf23f1-3a77-45b8-b781-2120c9720d4a)

<details>

<details>
<summary>
Open Issues
</summary>

![Iteration III open issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/735e1029-f0c8-4c0a-a19c-00ef5c23c92f)

<details>

### Iteration IV

<details>
<summary>
Closed Issues
</summary>

![Iteration IV closed issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/c1c121de-9780-445a-b30f-e30bffe1b073)

<details>

<details>
<summary>
Open Issues
</summary>

![Iteration IV open issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/86718e8f-98c8-47b7-ba28-05f3ec29cdeb)

<details>

### Iteration V

<details>
<summary>
Closed Issues
</summary>

![Iteration V closed issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/ce3a3ea5-a571-4af9-a612-5ecdd9519063)

<details>

<details>
<summary>
Open Issues
</summary>

![Iteration V open issues](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/89704025-31d3-4e6d-899c-02af1b4d7a35)

<details>

#### MoSCoW Prioritisation

MoSCoW prioritisation was used throughout the project. At the beginning of each new iteration the project backlog was assessed and each user story categorised for the current iteration, thus allowing for the correct balance of prioritisation for each iteration. This process was repeated for each new iteration, being mindful at all times of the overall remaining project time left.

These are the prioritisation tags

* 'Must Have' the user stories essential for compleating iteration.

* 'Should Have' the user stories important, but not essential for compleating iteration.

* 'Could Have' user stories with low importance to compleating iteration.

* 'Wont Have' user stories that won't be completed in this iteration.

### Information Radiators

GitHub projects was utilised as a kanban board for this project.

![Kanban board](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/7772dd8d-422e-4851-9dee-d947e8225f43)