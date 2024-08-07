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
