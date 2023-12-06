// check review form has been filled in correctly
function validateReviewForm(){
    // get values entered into form
    var valid = true;
    var brand = document.getElementById('brand').value;
    var review = document.getElementById('review').value;
    // remove extra whitespace and check length
    var brandTextLength = brand.replace(/\s/g, '').length;
    if (brand.length >= 50 || brandTextLength == 0){
        valid = false;
        alert("Please enter a brand between 0 and 50 characters long")
    }
    // remove extra whitespace and check length
    var reviewTextLength = review.replace(/\s/g, '').length;
    if (review.length >= 500 || reviewTextLength == 0){
        valid = false;
        alert("Please enter a review between 0 and 500 characters long");
    }
    // return whether to submit form or not
    return valid;
}