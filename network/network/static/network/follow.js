document.addEventListener('DOMContentLoaded', () => {
    const followers_count = document.querySelector('#followers-count');
    let count = parseInt(followers_count.innerHTML);
    document.querySelector('#follow-button').addEventListener('click', (event) => {
        const follow_button = event.target;
        const profile_id = follow_button.dataset.profile_id;
        fetch(`/follow/${profile_id}`)
        .then(response => response.text())
        .then((data) => {
            if (data === 'followed') {
                follow_button.innerHTML = "Unfollow";
                count += 1;
            } else {
                follow_button.innerHTML = "Follow";
                count -= 1;
            }
            followers_count.innerHTML = count;
        });
    });
});