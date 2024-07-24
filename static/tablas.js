(function () {
    'use strict';

    function validarNombres() {
        const nombresInput = document.getElementById('nombres');
        const feedbackVacio = document.getElementById('feedback-vacio');
        const feedbackInvalido = document.getElementById('feedback-invalido');
        const nombres = nombresInput.value.trim();
        const regex = /^[a-zA-ZÀ-ÿ\s]{1,40}$/;
        let isValid = true;

        feedbackVacio.style.display = 'none';
        feedbackInvalido.style.display = 'none';
        nombresInput.classList.remove('is-invalid');

        if (nombres === '') {
            nombresInput.classList.add('is-invalid');
            feedbackVacio.style.display = 'block';
            isValid = false;
        } else if (!regex.test(nombres)) {
            nombresInput.classList.add('is-invalid');
            feedbackInvalido.style.display = 'block';
            isValid = false;
        }

        return isValid;
    }

    window.addEventListener('load', function () {
        var forms = document.getElementsByClassName('needs-validation');
        Array.prototype.forEach.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity() || !validarNombres()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

