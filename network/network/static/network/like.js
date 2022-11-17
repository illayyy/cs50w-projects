document.addEventListener('DOMContentLoaded', () => {
    const like_buttons = document.querySelectorAll('.fa-heart');
    like_buttons.forEach(button => button.addEventListener('click', like));
});

function like(event) {
    const like_button = event.target;
    const post_id = like_button.dataset.post_id;
    const like_count = like_button.nextElementSibling;
    fetch(`/like/${post_id}`)
    .then(response => response.text())
    .then((data) => {
        if (data === 'liked') {
            like_button.classList.add("fa-solid");
            like_count.innerText = parseInt(like_count.innerText) + 1;
        } else {
            like_button.classList.remove("fa-solid");
            like_count.innerText = parseInt(like_count.innerText) - 1;
        }
    });
}