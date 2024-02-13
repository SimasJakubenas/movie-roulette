/**
 * Controls carousel ite movement and placement
 * Copied and adjusted as required from Materialize official docs 
 * https://materializecss.com/carousel.html
 */
$(document).ready(function () {
    $('.carousel').carousel({
        dist: -50,
        padding: 60,
    });
    
    spinRoulette()

});

/**
 * Picks a random number and sets the carousel in motion
 * Disables 'Spin It!!!' button and changes it's value
 * Selects the carousel item
 */
function spinRoulette() {
    $('#spin-it').on('click', function(e) {
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
