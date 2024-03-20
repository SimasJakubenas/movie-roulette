// const signUpForm = document.getElementById("signup_form");

/**
 * Controls carousel ite movement and placement
 * Copied and adjusted as required from Materialize official docs 
 * https://materializecss.com/carousel.html
 */
$(document).ready(function () {
    $(".dropdown-trigger").dropdown();
    $('.carousel-item').on('click', function (e) {
        e.stopPropagation()
    })
    $('.carousel').carousel({
        dist: -50,
        padding: 60
    });
    $('.carousel.carousel-slider').carousel({
        fullWidth: true
    });
    // Reveals overlay based on the clicked carousels item
    $('.carousel-item img').on('click', function () {
        let titleID = $(this).attr('data-titleID')
        let titleType = $(this).attr('data-titleType')
        // Sends ID of the selected title to backend
        let carouselIteNr = ($('img').index($(this)) - 1)
        sendTitleInfo(titleID, titleType, carouselIteNr)
    });
    // Closes the overlay
    $('.close-button').on('click', function () {
        $(this).parent().parent().css('display', 'none')
    });
    $('.contact-btn').on('click', function () {
        $('.contact').css('display', 'unset')
    })
    $('#id_streams').select2({
        theme: "material",
        width: "100%"
    })
    // Reveals confirmation modal for updating profile picture
    $('#id_profile_pic').on('change', function () {
        $('#edit-profile-pic-confirm').css('display', 'unset')
    })
    // Reloads the page when 'No' button is clicked in confirmation modal
    $('.deny-button').on('click', function () {
        location.reload();
    })
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
                console.log(data)
            }
        });

    });
    // $('#edit-profile').on('click', function () {
    //     signUpForm.setAttribute("action", `edit_comment/${commentId}`);
    // });
    listIconToggle(this)
    spinRoulette()
    movieShowToggle()
    removeFromList()
    // Confirmation modal to clear all button
    $('.btn-red').on('click', function () {
        let confirmClearAll = confirm('Are you sure you want to do this?')
        if (confirmClearAll == false) event.preventDefault()
    });
    // Add classes to form imputs for responsivness
    $('.individual-select').children('select').removeClass('col xl6 push-xl3 m10 push-m1')
    // This is used to change forms boolean logic
    // It allows for differentiation of actions in one view (load one title/load many titles)
    $('.main-select:last').children('input:last').attr('checked', 'checked')
});

/**
 * Picks a random number and sets the carousel in motion
 * Disables 'Spin It!!!' button and changes it's value
 * Selects the carousel item
 */
function spinRoulette() {
    $('#spin-it').on('click', function (e) {
        let totalSlides = 0;
        let oneSlide = setInterval(individualSpin, 300);
        let randomPick = Math.floor(Math.random() * 10) + 5
        $("#spin-it").attr("disabled", 'disabled')
        $('#spin-it').html('In Motion!');

        // Traverses through carousel items and stops it based on random number
        function individualSpin() {
            $('.carousel').carousel('prev');
            totalSlides++;
            if (totalSlides > randomPick) {
                clearInterval(oneSlide);
                // Enables 'Spin It!!!' button and changes it's value back
                $("#spin-it").removeAttr("disabled", 'disabled')
                $('#spin-it').html('Spin It!!!');
            }
        }
    })
}

/**
 * Sends POST request with ajax
 * Transfers data (title ID) from frontend to backend
 * Taken and altered to suit the need from
 * https://copyprogramming.com/howto/pass-array-to-backend-using-ajax-django
 * Returns data from the backend and fills in required title info
 */
function sendTitleInfo(titleID, titleType, carouselIteNr) {
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
            let openOverlay = function (index, getTitle) {
                $('.overlay').eq(index).css('display', 'unset');
                let titleInfo = JSON.parse(getTitle)
                let genreList = []
                let castList = []
                $.each(titleInfo.genres, function (key, value) {
                    genreList.push(value.name)
                });
                $('.genres').eq(index).html(`${genreList.join(', ')}`)
                if (titleType == 0) {
                    fill_movie_details(index, titleInfo, castList)
                } else {
                    fill_tv_details(index, titleInfo, castList)
                }
                compileStreamList(index, titleInfo)
            }
            openOverlay(carouselIteNr, getTitle)
        },
        error: (error) => {
            console.log(error);
        }
    });
}

/**
 * Sends POST request with ajax
 * Transfers data (title ID and type of list) from frontend to backend
 * Toggles background colour
 */
function listIconToggle() {
    $('.add-to-list').on('click', function () {
        let titleID = $(this).attr('data-titleID')
        let list = $(this).attr('data-in-list')

        if ($(this).attr('data-listed')) {
            $(this).removeAttr('data-listed')
            $(this).css('background-color', 'unset')
            $('.listed-title img').each(function () {
                if ($(this).attr('data-titleID') == titleID) {
                    $(this).css('display', 'none')
                    $(this).siblings().css('display', 'none')
                }
            })
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
            $(this).attr('data-listed', 'true')
            $(this).css('background-color', '#6CE5E8')
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
    })
};

function fill_movie_details(index, titleInfo, castList) {
    /**
     * Fills respective html elements with recieved data from ajax request responce
     */
    let directorList = []
    $('.runtime').eq(index).html(`${titleInfo.runtime}`)
    $('.age-limit').eq(index).html(`${titleInfo.releases.countries[0].certification}`)
    $.each(titleInfo.casts.cast, function (key, value) {
        castList.push(value.name)
    });
    $('.cast').eq(index).html(`${castList.join(', ')}`)
    $(titleInfo.casts.crew).each(function () {
        if ($(this)[0].job === 'Director') {
            directorList.push($(this)[0].name)
        }
    });
    $('.director').eq(index).html(`${directorList.join(', ')}`)
}

function fill_tv_details(index, titleInfo, castList) {
    /**
     * Fills respective html elements with recieved data from ajax request responce
     */
    let creatorList = []
    $('.seasons').eq(index).html(`${titleInfo.last_episode_to_air.season_number}`)
    $('.status').eq(index).html(`${titleInfo.status}`)
    $.each(titleInfo.credits.cast, function (key, value) {
        castList.push(value.name)
    });
    $('.cast').eq(index).html(`${castList.join(', ')}`)
    $(titleInfo.created_by).each(function () {
        creatorList.push($(this)[0].name)
    });
    $('.creator').eq(index).html(`${creatorList.join(', ')}`)
}

/**
 * Loops through different sections of ajax request responce
 * Fills providers container with images of service providers
 */
function compileStreamList(index, titleInfo) {
    let streamContainer = $('.providers').eq(index)
    let streamList = []
    $.each(titleInfo.results.IE.flatrate, function (key, value) {
        if (streamList.includes(value.provider_id)) {} else {
            appendStreamList(value, streamList, streamContainer)
        }
    });
    $.each(titleInfo.results.IE.rent, function (key, value) {
        if (streamList.includes(value.provider_id)) {} else {
            appendStreamList(value, streamList, streamContainer)
        }
    });
    $.each(titleInfo.results.IE.buy, function (key, value) {
        if (streamList.includes(value.provider_id)) {} else {
            appendStreamList(value, streamList, streamContainer)
        }
    });
}

/**
 * Acuires forms type value and displays/hides titles accordingly
 */
function movieShowToggle() {
    $('.list-type select').addClass('type-select')
    type = $('.type-select').val()
    displayFavouriteTypeOfTitle(type)
    $('.type-select').on('change', function () {
        type = $(this).val()
        displayFavouriteTypeOfTitle(type)
    })
}

function displayFavouriteTypeOfTitle(type) {
    if (type === 'Movies') {
        $('.movies-list').css('display', 'unset')
        $('.shows-list').css('display', 'none')
    } else {
        $('.shows-list').css('display', 'unset')
        $('.movies-list').css('display', 'none')
    }
}

/**
 * Adds streaming providers logos to providers container 
 */
function appendStreamList(value, streamList, streamContainer) {
    streamList.push(value.provider_id)
    streamContainer.append(`<img src="https://image.tmdb.org/t/p/h100${value.logo_path}">`)
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
    $('.remove-one-title').on('click', function () {
        let titleID = $(this).attr('data-titleID')
        let list = $(this).attr('data-in-list')
        $(this).parent().css('display', 'none')
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
    })
}