/**
 * Controls carousel ite movement and placement
 * Copied and adjusted as required from Materialize official docs 
 * https://materializecss.com/carousel.html
 */
$(document).ready(function () {
    $('.carousel-item').on('click', function (e) {
        e.stopPropagation()
    })
    $('.carousel').carousel({
        dist: -50,
        padding: 60
    });
    // Reveals overlay based on the clicked carousels item
    $('.carousel-item img').on('click', function () {
        let titleID = $(this).attr('data-titleID')
        let titleType = $(this).attr('data-titleType')
        // Sends ID of the selected title to backend
        let carouselIteNr = $('img').index($(this))
        sendTitleInfo(titleID, titleType, carouselIteNr)
    });
    // Closes the overlay
    $('.close-button').on('click', function () {
        $(this).parent().parent().css('display', 'none')
    });
    spinRoulette()
    // Confirmation modal to clear all button
    $('.btn-red').on('click', function () {
        let confirmClearAll = confirm('Are you sure you want to clear the roulette?')
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
        success: function (get_title) {
            let openOverlay = function (index, get_title) {
                $('.overlay').eq(index).css('display', 'unset');
                let title_info = JSON.parse(get_title)
                let genreList = []
                let castList = []
                $.each(title_info.genres, function(key, value) {
                    genreList.push(value.name)
                });
                $('.genres').eq(index).html(`${genreList.join(', ')}`)
                if (titleType == 0) {
                    fill_movie_details(index, title_info, castList)
                }
                else {
                    fill_tv_details(index, title_info, castList)
                }
            }
            openOverlay(carouselIteNr, get_title)
        },
        error: (error) => {
            console.log(error);
        }
    });
}

function fill_movie_details(index, title_info, castList) {
    /**
     * Fills respective html elements with recieved data from ajax request responce
     */
    let directorList = []
    $('.runtime').eq(index).html(`${title_info.runtime}`)
    $('.age-limit').eq(index).html(`${title_info.releases.countries[0].certification}`)
    $.each(title_info.casts.cast, function(key, value) {
        castList.push(value.name)
    });
    $('.cast').eq(index).html(`${castList.join(', ')}`)
    $(title_info.casts.crew).each(function () {
        if ($(this)[0].job === 'Director') {
            directorList.push($(this)[0].name)
        } 
    });
    $('.director').eq(index).html(`${directorList.join(', ')}`)
}

function fill_tv_details(index, title_info, castList) {
    /**
     * Fills respective html elements with recieved data from ajax request responce
     */
    let creatorList = []
    $('.seasons').eq(index).html(`${title_info.last_episode_to_air.season_number}`)
    $('.status').eq(index).html(`${title_info.status}`)
    $.each(title_info.credits.cast, function(key, value) {
        castList.push(value.name)
    });
    $('.cast').eq(index).html(`${castList.join(', ')}`)
    $(title_info.created_by).each(function () {
        creatorList.push($(this)[0].name)
    });
    $('.creator').eq(index).html(`${creatorList.join(', ')}`)
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