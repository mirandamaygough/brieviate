// respond to star clicks
document.addEventListener('DOMContentLoaded', function() {
    // get initial rating value
    const current = parseInt(document.getElementById('rating-value').value); 
    // get stars list
    const stars = document.querySelectorAll('.rating-stars span');
    // set initial active stars based on the current rating
    for (let i = 0; i < current; i++) {
        stars[i].classList.add('active');
    }
    // add event listener for click to each star
    stars.forEach(function(star) {
        star.addEventListener('click', function() {
            // get value of clicked star
            var value = this.getAttribute('data-value');
            if (value == document.getElementById('rating-value').value) {
                // if clicked star is same as current rating, set value to 0
                value = 0;
            }
            // set value of rating to clicked star value
            document.getElementById('rating-value').value = value;
            // remove active class from all stars
            stars.forEach(function(star) {
                star.classList.remove('active');
            });
            // add active class to clicked star and all stars before it
            for (let i = 0; i < value; i++) {
                stars[i].classList.add('active');
            };
        });
    });
});