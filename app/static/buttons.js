// add event listeners for edit buttons
document.addEventListener('DOMContentLoaded', function() {
    var editReviewButtons = document.querySelectorAll('.edit-review-button');
    editReviewButtons.forEach(function(button){
        button.addEventListener('click', editButtonClicked)
    });
});

// add event listeners for delete buttons
document.addEventListener('DOMContentLoaded', function() {
    var deleteReviewButtons = document.querySelectorAll('.delete-review-button');
    deleteReviewButtons.forEach(function(button){
        button.addEventListener('click', deleteButtonClicked)
    });
});

// respond to edit button click
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

// respond to delete button click
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