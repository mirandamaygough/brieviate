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

function validateRegisterForm(){
    // get values entered into form
    var valid = true;
    var email = document.getElementById('email').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var emailRegex = /^\S+@\S+\.\S+$/;
    var passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    // check email is valid
    if (!emailRegex.test(email) || email.length >= 50){
        valid = false;
        alert("Please enter a valid email address between 0 and 50 characters long");
    }
    // check username is valid by removing extra whitespace and checking length
    var usernameTextLength = username.replace(/\s/g, '').length;
    if (username.length >= 25 || usernameTextLength == 0){
        valid = false;
        alert("Please enter a username between 0 and 25 characters long")
    }
    // check password is valid
    if (!passwordRegex.test(password)|| password.length >= 25){
        valid = false;
        alert("Please enter a password that is between 8 and 25 characters long and contains at least one letter and one number");
    }
    // return whether to submit form or not
    return valid;
}

function validateLoginForm(){
    // get values entered into form
    var valid = true;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var emailRegex = /^\S+@\S+\.\S+$/;
    // check email is valid
    if (!emailRegex.test(email) || email.length >= 50){
        valid = false;
        alert("Please enter a valid email address between 0 and 50 characters long");
    }
    // check password is valid
    if (password.length <8 || password.length >= 25){
        valid = false;
        alert("Please enter a password that is between 8 and 25 characters long");
    }
    // return whether to submit form or not
    return valid;
}