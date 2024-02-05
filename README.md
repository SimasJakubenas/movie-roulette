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

![ERD diagram](https://github.com/SimasJakubenas/movie-roulette/assets/138577499/3018a969-6cbe-483b-a4d8-3aadb779beaa)

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
