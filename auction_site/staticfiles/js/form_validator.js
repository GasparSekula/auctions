document.getElementById('registerForm').addEventListener('submit', function (event) {
    const password = document.getElementById('id_password1').value;
    const confirmPassword = document.getElementById('id_password2').value;

    if (password !== confirmPassword) {
        event.preventDefault();
        alert('Passwords do not match!');
    }
});
