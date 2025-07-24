document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Você deseja realmente enviar este formulário?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    }
});
