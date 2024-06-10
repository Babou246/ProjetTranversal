// script.js
document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('myModal');
    const openModalButton = document.getElementById('openModalButton');
    const closeButton = document.querySelector('.close-button');

    openModalButton.addEventListener('click', (event) => {
        event.preventDefault();
        modal.style.display = 'block';
    });

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});
