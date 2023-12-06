// respond to like button clicks
document.addEventListener('DOMContentLoaded', function() {
    // get all like buttons
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(function(button) {
        // get review id of button clicked
        var reviewId = button.getAttribute('review-id');
        // make an AJAX request to check if the review has been liked
        $.ajax({
            url: '/check_like?id=' + encodeURIComponent(reviewId),
            method: 'GET',
            success: function(response) {
                // set button text and class based on response
                if (response.liked) {
                    button.innerHTML='&#128147;';
                    button.classList.add('liked');
                } else {
                    button.innerHTML='&#129293;';
                    button.classList.remove('liked');
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
        // add event listener for click to each button
        button.addEventListener('click', function() {
            // make an AJAX request to like or unlike the review
            $.ajax({
                url: '/like_rating?id=' + encodeURIComponent(reviewId),
                method: 'POST',
                success: function(response) {
                    // update like count and button text and class based on response
                    $('#likes-' + reviewId).text(response.likes);
                    if (button.classList.contains('liked')) {
                        button.innerHTML='&#129293;';
                        button.classList.remove('liked');
                    } else {
                        button.innerHTML='&#128147;';
                        button.classList.add('liked');
                    }
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        });
    });
});