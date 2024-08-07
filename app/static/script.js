document.addEventListener('DOMContentLoaded', function() {
    var signUpBtn = document.getElementById('signUpBtn');
    var modal = document.getElementById('signUpModal');
    var closeBtn = document.querySelector('.close');

    signUpBtn.onclick = function() {
        modal.style.display = 'block';
    }

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});

$(document).ready(function () {
    var passwordField = $('#password');
    var confirmPasswordField = $('#confirm_password');
    var message = $('#passwordMatchMessage');

    // Check if passwords match while typing
    function checkPasswords() {
        var password = passwordField.val();
        var confirmPassword = confirmPasswordField.val();

        if (password === confirmPassword) {
            message.text("Passwords match").css('color', 'green');
        } else {
            message.text("Passwords do not match!").css('color', 'red');
        }
    }

    passwordField.on('input', checkPasswords);
    confirmPasswordField.on('input', checkPasswords);
});

