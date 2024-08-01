(function () {
    'use strict';

    function validateInput(event) {
        const input = event.target;
        const pattern = new RegExp(input.pattern);
        if (!pattern.test(input.value)) {
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    }

    function handleFormSubmission(event) {
        const form = event.target;
        let isValid = true;

        // Recorre todos los campos con el atributo pattern
        const inputs = form.querySelectorAll('input[pattern]');
        inputs.forEach(function (input) {
            const pattern = new RegExp(input.pattern);
            if (!pattern.test(input.value)) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });

        // Añade la clase was-validated para mostrar los estilos de validación
        form.classList.add('was-validated');

        // Evita el envío del formulario si hay campos inválidos
        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
        }
    }

    window.addEventListener('load', function () {
        const forms = document.getElementsByClassName('needs-validation');
        Array.prototype.forEach.call(forms, function (form) {
            form.addEventListener('submit', handleFormSubmission, false);

            // Añade eventos de validación en tiempo real a los campos de entrada
            const inputs = form.querySelectorAll('input[pattern]');
            inputs.forEach(function (input) {
                input.addEventListener('input', validateInput);
            });
        });
    }, false);
})();



