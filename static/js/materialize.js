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
        // Sends ID of the selected title to backend
        sendTitleID(titleID)
        let carouselIteNr = $('img').index($(this))
        let openOverlay = function (el) {
            $('.overlay').eq(el).css('display', 'unset')
        }
        openOverlay(carouselIteNr)
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
 */
function sendTitleID(titleID) {
    $.ajax({
        url: 'info/',
        type: 'POST',
        data: {
            'titleID': titleID
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        error: (error) => {
            console.log(error);
        }
    });
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