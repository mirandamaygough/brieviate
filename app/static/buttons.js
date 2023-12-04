// add event listeners for buttons
document.addEventListener('DOMContentLoaded', function() {
    var editReviewButtons = document.querySelectorAll('.edit-review-button');
    editReviewButtons.forEach(function(button){
        button.addEventListener('click', editButtonClicked)
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var deleteReviewButtons = document.querySelectorAll('.delete-review-button');
    deleteReviewButtons.forEach(function(button){
        button.addEventListener('click', deleteButtonClicked)
    });
});

function editButtonClicked(){
    // get review of button clicked and its id
    var reviewId=this.closest('.card').dataset.id;
    // construct url to send to server
    var url = '/edit_rating_handler?id=' + encodeURIComponent(reviewId);
    // send url to server
    fetch(url)
    .then(response => {
        // navigate to redirected url
        if (response.redirected) {
            window.location.href = response.url;
        }
        })
        .catch(error => console.error('Error:', error));
}

function deleteButtonClicked(){
    // get review of button clicked and its id
    var reviewId=this.closest('.card').dataset.id;
    // construct url to send to server
    var url = '/delete_rating?id=' + encodeURIComponent(reviewId);
    // send url to server
    fetch(url)
    .then(response => {
        // navigate to redirected url
        if (response.redirected) {
            window.location.href = response.url;
        }
        })
        .catch(error => console.error('Error:', error));
}