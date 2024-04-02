  /**
   * Controls carousel ite movement and placement
   * Copied and adjusted as required from Materialize official docs 
   * https://materializecss.com/carousel.html
   */
  $(document).ready(function () {
    menuFadeInAndOut();
    $('.modal').modal();
    $(".dropdown-trigger").dropdown();
    $('.carousel-item').on('click', function (e) {
        e.stopPropagation();
    });
    carouselControls();
    // Reveals overlay based on the clicked carousels item
    overlayTrigger();
    // Closes the overlay
    $('.close-button').on('click', function () {
        $(this).parent().parent().css('display', 'none');
        $('#providers').html('');
    });
    $('.contact-btn').on('click', function () {
        $('.contact').css('display', 'unset');
    });
    $('#id_streams').select2({
        theme: "material",
        width: "100%"
    });
    // Reveals confirmation modal for updating profile picture
    $('#id_profile_pic').on('change', function () {
        $('#edit-profile-pic-confirm').css('display', 'unset');
    });
    // Reloads the page when 'No' button is clicked in confirmation modal
    $('.deny-button').on('click', function () {
        location.reload();
    });
    $('#outer').on('click', function () {
        $('.type-toggle').each(function () {
            if ($((this)).hasClass('type-active')) {
                $((this)).removeClass('type-active');
                $('#inner').css('left', '0');
                $('#inner').css('right', 'unset');
            } else {
                $((this)).addClass('type-active');
                $('#inner').css('right', '0');
                $('#inner').css('left', 'unset');
            }
        });
        let url = $("#genre-container").attr("data-search-genres-url");
        let type = $('.type-active').attr('data-search-type');
        $.ajax({
            url: url,
            data: {
                'type': type,
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (data) {
                $("#genre-container").html(data);
            },
            error: (error) => {
                console.log(error);
            }
        }).then(() => genreToggle());
    });
    searchFunctionality();
    genreToggle();
    countryStreamingProviders();
    listMenuToggle();
    listTypeToggle();
    listIconToggle();
    spinRoulette();
    // movieShowToggle()
    removeFromList();
    // Confirmation modal to clear all button
    $('.btn-red').on('click', function () {
        let confirmClearAll = confirm('Are you sure you want to do this?');
        if (confirmClearAll == false) event.preventDefault();
    });
    // Add classes to form imputs for responsivness
    $('.individual-select').children('select').removeClass('col xl6 push-xl3 m10 push-m1');
    // This is used to change forms boolean logic
    // It allows for differentiation of actions in one view (load one title/load many titles)
    $('.main-select:last').children('input:last').attr('checked', 'checked');
});

/**
 * Gathers all data from user input and sends it to backend via async function
 * Recieves relevant data back and fills search results container
 */
function searchFunctionality() {
    $('#search-btn').on('click', function () {
        // let url = $("#search-form").attr("data-search-results-url");
        let url = $("#search-form").attr("data-search-results-url");
        let year = $('#id_year').val();
        let rating = $('#id_rating').val();
        let runtime = $('#id_runtime').val();
        let titleType = '';
        let cast = $('#id_cast').val();
        let genreList = [];
        let jointGenreList = "";
        $('.genre-box.genre-active').each(function () {
            genreList.push($(this).attr('data-genre-id'));
            jointGenreList = genreList.join();
        });
        $('.type-active').each(function () {
            titleType = $(this).attr('data-search-type');
        });

        $.ajax({
            url: url,
            data: {
                'year': year,
                'rating': rating,
                'runtime': runtime,
                'cast': cast,
                'titleType': titleType,
                'jointGenreList': jointGenreList
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (data) {
                $("#search-results-container").html(data);
            },
            error: (error) => {
                console.log(error);
            }
        }).then(() => overlayTrigger());
    });
  }

/**
 * Adds or removes active class for genres
 */
function genreToggle() {
    $('.genre-box').on('click', function () {
        if ($(this).hasClass('genre-active')) {
            $(this).removeClass('genre-active');
        } else {
            $(this).addClass('genre-active');
        }
    });
}

/**
 * Runs async function triggered by title type select element change
 * Passed data to backend which in turn returns data to be fild in streming providers select element
 * * Awaits resutls and runs overlayTrigger and removeFromList functions
 */
function listTypeToggle() {
    $("#id_type").change(function () {
        let url = $("#list-type-form").attr("data-list-type-url");
        let type = $(this).val();
              let list 
        $(".list-menu-item").each(function () {
            if ($(this).hasClass('list-active')) {
                list = $(this).attr('data-list');
            }
        });
        $.ajax({
            url: url,
            data: {
                'type': type,
                'list': list
            },
            success: function (data) {
                $("#list-container").html(data);
            }
        }).then(() => overlayTrigger()).then(() => removeFromList());
    });
}

/**
 * Runs async function triggered by country select element change
 * Passed data to backend which in turn returns data to be fild in streming providers select element
 */
function countryStreamingProviders() {
    $("#id_country").change(function () {
        var url = $("#signup_form").attr("data-providers-url");
        var countryName = $(this).val();
        $.ajax({
            url: url,
            data: {
                'country': countryName
            },
            success: function (data) {
                $("#id_streams").html(data);
            }
        });
    });
}

/**
 * Creates functionality for toggling list menu with async function
 * Passes data to backend  which in turn returns data to be loaded on the page
 * Awaits resutls and runs overlayTrigger and removeFromList functions
 */
function listMenuToggle() {
    $(".list-menu-item").on('click', function () {
        let type = $('#id_type').val();
        let list = $(this).attr("data-list");
        let url = $("#list-type-form").attr("data-list-type-url");
        $(".list-menu-item").each(function () {
            $(this).removeClass('list-active');
        });
        $(this).addClass('list-active');
        $.ajax({
            url: url,
            data: {
                'type': type,
                'list': list
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (data) {
                $("#list-container").html(data);

            },
            error: (error) => {
                console.log(error);
            }
        }).then(() => overlayTrigger()).then(() => removeFromList())
    });
}

function overlayTrigger() {
    $('.overlay-trigger').on('click', function () {
        let titleID = $(this).attr('data-titleID')
        let titleType = $(this).attr('data-titleType');
        // Sends ID of the selected title to backend
        sendTitleInfo(titleID, titleType);
    });
}

/**
 * Initiates all carousels and add controls
 */
function carouselControls() {
    $('#roulette').carousel({
        dist: -50,
        padding: 60
    });
    $('#carousel-popular').carousel({
        dist: 0,
        padding: 20
    });
    $('#carousel-top-rated').carousel({
        dist: 0,
        padding: 20
    });
    $('.popular-container .fa-chevron-left').on("click", function () {
        $('#carousel-popular').carousel('prev');
    });
    $('.popular-container .fa-chevron-right').on("click", function () {
        $('#carousel-popular').carousel('next');
    });
    $('.top-rated-container .fa-chevron-left').on("click", function () {
        $('#carousel-top-rated').carousel('prev');
    });
    $('.top-rated-container .fa-chevron-right').on("click", function () {
        $('#carousel-top-rated').carousel('next');
    });
    $('.carousel.carousel-slider').carousel({
        fullWidth: true
    });
    $('.carousel-main .fa-chevron-left').on("click", function () {
        $('.carousel-main').carousel('prev');
    });
    $('.carousel-main .fa-chevron-right').on("click", function () {
        $('.carousel-main').carousel('next');
    });
}

/**
 * Changes menu visibility with mouse wheel
 * Taken and altered from https://stackoverflow.com/questions/8189840/get-mouse-wheel-events-in-jquery
 */
function menuFadeInAndOut() {
    $('body').on('wheel', function (event) {
        if (event.originalEvent.wheelDelta <= 0) {
            $('.nav-content ul').css('position', 'absolute');
            $('.nav-content ul').css('top', '-10vh');
            $('.nav-wrapper').css('background-color', '#000');
            $('.nav-wrapper').on('mouseenter', function () {
                $('.nav-content ul').css('position', 'unset');
                $('.nav-content ul').css('top', '0');
            });
            $('nav').on('mouseleave', function () {
                $('.nav-content ul').css('position', 'absolute');
                $('.nav-content ul').css('top', '-10vh');
                $('.nav-wrapper').css('background-color', '#000');
            });
        } else
            // Menu is made visible on scrolling to top of the page
            // Taken from https://stackoverflow.com/questions/15123081/how-can-i-launch-a-javascript-or-jquery-event-when-i-reach-the-top-of-my-page
            $(window).on('scroll', function () {
                if ($(this).scrollTop() == 0) {
                    $('.nav-content ul').css('position', 'unset');
                    $('.nav-content ul').css('top', '0');
                    $('.nav-wrapper').css('background-color', 'unset');
                }
            });
    })
}

/**
 * Picks a random number and sets the carousel in motion
 * Disables 'Spin It!!!' button and changes it's value
 * Selects the carousel item
 */
function spinRoulette() {
    $('#spin-it').on('click', function (e) {
        let totalSlides = 0;
        let oneSlide = setInterval(individualSpin, 300);
        let randomPick = Math.floor(Math.random() * 10) + 5;
        $("#spin-it").attr("disabled", 'disabled');
        $('#spin-it').html('In Motion!');

        // Traverses through carousel items and stops it based on random number
        function individualSpin() {
            $('.carousel').carousel('prev');
            totalSlides++;
            if (totalSlides > randomPick) {
                clearInterval(oneSlide);
                // Enables 'Spin It!!!' button and changes it's value back
                $("#spin-it").removeAttr("disabled", 'disabled');
                $('#spin-it').html('Spin It!!!');
            }
        }
    });
}

/**
 * Sends POST request with ajax
 * Transfers data (title ID) from frontend to backend
 * Taken and altered to suit the need from
 * https://copyprogramming.com/howto/pass-array-to-backend-using-ajax-django
 * Returns data from the backend and fills in required title info
 */
function sendTitleInfo(titleID, titleType) {
    $.ajax({
        url: 'info/',
        type: 'POST',
        data: {
            'titleID': titleID,
            'titleType': titleType
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function (getTitle) {
            let openOverlay = function (getTitle) {
                $('.overlay').css('display', 'unset');
                let titleInfo = JSON.parse(getTitle);
                let genreList = [];
                let castList = [];
                $('.add-to-list').each(function () {
                    $(this).css('background-color', 'unset');
                });
                $('.add-to-list').attr('data-titleID', titleInfo.id);
                if (titleInfo.videos.results > 0) {
                    $('#trailer-button').attr(
                    'href', 'https://www.youtube.com/watch?v=' + titleInfo.videos.results[0].key
                    );
                }
                else {
                    $('#trailer-button').attr('href', 'https://www.youtube.com/');
                }
                
                $('#title-description').expander('destroy');
                $('#cast').expander('destroy');
                $('#crew-list').expander('destroy');
                $('#title-description').html(titleInfo.overview).expander();

                $('.overlay-img').attr('src', 'https://image.tmdb.org/t/p/w154' + titleInfo.poster_path);
                $('#rating').html(Math.round(titleInfo.vote_average * 10) / 10);
                $.each(titleInfo.genres, function (key, value) {
                    genreList.push(value.name);
                });
                $('#genres').html(genreList.join(', '));
                if (titleType == 0 || titleType == 'movie' ) {
                    fill_movie_details(titleInfo, castList);
                } else {
                    fill_tv_details(titleInfo, castList);
                }
                  compileStreamList(titleInfo)
                // changes background color of list icons if title in that list
                if (titleInfo.is_in_favourites === true) {
                    $('.add-to-favourites').css('background-color', '#6CE5E8');
                }
                if (titleInfo.is_in_watchlist === true) {
                    $('.add-to-watchlist').css('background-color', '#6CE5E8');
                }
                if (titleInfo.is_in_seen_it === true) {
                    $('.add-to-seen-it').css('background-color', '#6CE5E8');
                }
                if (titleInfo.is_in_dont_show === true) {
                    $('.add-to-dont-show').css('background-color', '#6CE5E8');
                }
            };
            openOverlay(getTitle);
        },
        error: (error) => {
            console.log(error);
        }
    });
    console.log('safasd');
}

/**
 * Sends POST request with ajax
 * Transfers data (title ID and type of list) from frontend to backend
 * Toggles background colour
 */
function listIconToggle() {
    $('.add-to-list').on('click', function () {
        let titleID = $(this).attr('data-titleID');
        let list = $(this).attr('data-in-list');

        if ($(this).attr('data-listed')) {
            $(this).removeAttr('data-listed');
            $(this).css('background-color', 'unset');
            if (list !== 'roulette') {
                
                $('.listed-title img').each(function () {
                    if ($(this).attr('data-titleID') == titleID) {
                        $(this).css('display', 'none');
                        $(this).siblings().css('display', 'none');
                    }
                });
            }
            $.ajax({
                url: 'remove/',
                type: 'POST',
                data: {
                    'list': list,
                    'titleID': titleID,
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },

                error: (error) => {
                    console.log(error);
                }
            });
        } else {
            $(this).attr('data-listed', 'true');
            if (list !== 'roulette') {
                $(this).css('background-color', '#6CE5E8');
            }
            $.ajax({
                url: 'add/',
                type: 'POST',
                data: {
                    'list': list,
                    'titleID': titleID,
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },

                error: (error) => {
                    console.log(error);
                }
            });
        }
    });
}

function fill_movie_details(titleInfo, castList) {
    /**
     * Fills respective html elements with recieved data from ajax request responce
     */
    let directorList = [];
    $('#overlay-heading span').html(titleInfo.title);
    $('#release-year').html('Release Year');
    $('#first-aired').html('');
    $('#seasons').html('');
    $('#seasons-count').css('display', 'none');
    $('#status').css('display', 'none');
    $('#date').html((titleInfo.release_date).slice(0, 4));
    $('#runtime').html('Runtime');
    $('#runtime-minutes').css('display', 'unset');
    $('#runtime-minutes').html(titleInfo.runtime);
    $('#age-limit').css('display', 'unset');
    $('#age-limit').html(titleInfo.releases.countries[0].certification);
    $.each(titleInfo.casts.cast, function (key, value) {
        castList.push(value.name);
    });
    $('#cast').html(castList.join(', ')).expander();
    $(titleInfo.casts.crew).each(function () {
        if ($(this)[0].job === 'Director') {
            directorList.push($(this)[0].name);
        }
    });
    $('#crew').html('Directed By:').expander();
    $('#crew-list').html(directorList.join(', '));
}

function fill_tv_details(titleInfo, castList) {
    /**
     * Fills respective html elements with recieved data from ajax request responce
     */
    let creatorList = [];
    $('#overlay-heading span').html(titleInfo.name);
    $('#first-aired').html('First Aired');
    $('#date').html((titleInfo.first_air_date).slice(0, 4));
    $('#seasons').html('Seasons');
    $('#seasons-count').css('display', 'unset');
    $('#seasons-count').html(titleInfo.last_episode_to_air.season_number);
    $('#status').css('display', 'unset');
    $('#status').html(titleInfo.status);
    $('#runtime').html('');
    $('#runtime-minutes').css('display', 'none');
    $('#age-limit').css('display', 'none');
    $.each(titleInfo.credits.cast, function (key, value) {
        castList.push(value.name);
    });
    $('#cast').html(castList.join(', '));
    $(titleInfo.created_by).each(function () {
        creatorList.push($(this)[0].name);
    });
    $('#crew').html('Created By:');
    $('#crew-list').html(creatorList.join(', '));
}

/**
 * Loops through different sections of ajax request responce
 * Fills providers container with images of service providers
 */
function compileStreamList(titleInfo) {
    let titleStreams = titleInfo['provider_name'];
    let userCountry = titleInfo['user_country'];
    let streamContainer = $('#providers');
    let streamList = [];
    $.each(titleInfo.results[userCountry].flatrate, function (key, value) {
        if (streamList.includes(value.provider_id)) {} else {
            appendStreamList(titleStreams, value, streamList, streamContainer);
        }
    });
    $.each(titleInfo.results[userCountry].rent, function (key, value) {
        if (streamList.includes(value.provider_id)) {} else {
            appendStreamList(titleStreams, value, streamList, streamContainer);
        }
    });
    $.each(titleInfo.results[userCountry].buy, function (key, value) {
        if (streamList.includes(value.provider_id)) {} else {
            appendStreamList(titleStreams, value, streamList, streamContainer);
        }
    });
}

/**
 * Adds streaming providers logos to providers container 
 */
function appendStreamList(titleStreams, value, streamList, streamContainer) {
    if (titleStreams.includes(value.provider_name)) {

        streamList.push(value.provider_id);
        streamContainer.append(`<img src="https://image.tmdb.org/t/p/h100${value.logo_path}">`);
    }
}

/**
 * Function used to get csrf token value when a post request is send without a form element
 * Taken from django documentation https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Async function that sends POST request with data which then in turn
 * is used to carry out CRUD funtionalities on the backend
 */
function removeFromList() {
    let list = 'roulette';
    $('.remove-one-title').on('click', function () {
        let titleID = $(this).attr('data-titleID');
        $('.list-menu-item').each(function () {
            if ($(this).hasClass('list-active')) {
                list = $(this).attr('data-list');
            }
        });
        $(this).parent().css('display', 'none');
        $.ajax({
            url: 'remove/',
            type: 'POST',
            data: {
                'list': list,
                'titleID': titleID,
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            error: (error) => {
                console.log(error);
            }
        });
    });
}