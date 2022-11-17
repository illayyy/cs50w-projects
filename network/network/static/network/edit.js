const error_div = document.createElement('div');
error_div.className = "alert alert-danger";
error_div.innerHTML = "You do not have permission to edit this post";

document.addEventListener('DOMContentLoaded', () => {
    const edit_buttons = document.querySelectorAll('.edit-button');
    edit_buttons.forEach(button => button.addEventListener('click', edit));
});

function edit(event) {
    const cancel_buttons = document.querySelectorAll('.cancel-button');
    cancel_buttons.forEach(button => button.click());

    const error_messages = document.querySelectorAll('.alert-danger');
    error_messages.forEach(message => message.parentElement.removeChild(message));

    const edit_button = event.target;
    const edit_parent = edit_button.parentElement;
    const post_id = edit_button.dataset.post_id;
    const container_div = edit_parent.nextElementSibling;
    const like_div = container_div.nextElementSibling;
    const old_content = container_div.innerHTML;

    edit_parent.removeChild(edit_button);

    const form = document.createElement('form');
    const form_div = document.createElement('div');
    const textarea = document.createElement('textarea');
    const submit_button = document.createElement('input');
    const cancel_button = document.createElement('input');

    container_div.innerHTML = '';

    container_div.appendChild(form);
    form.appendChild(form_div);
    form_div.appendChild(textarea);
    form_div.appendChild(submit_button);
    form_div.appendChild(cancel_button);

    form_div.className = "form-group mb-0";
    textarea.className = "form-control";
    submit_button.className = "btn btn-primary mt-2";
    cancel_button.className = "btn btn-secondary mt-2 ml-2 cancel-button";
    like_div.style.display = 'none';

    textarea.value = old_content;

    submit_button.setAttribute('type', 'button');
    cancel_button.setAttribute('type', 'button');
    submit_button.setAttribute('value', 'Save');
    cancel_button.setAttribute('value', 'Cancel');

    cancel_button.addEventListener('click', () => {
        container_div.innerHTML = old_content;
        edit_parent.appendChild(edit_button);
        like_div.style.display = 'block';
    })

    submit_button.addEventListener('click', () => {
        const new_content = textarea.value;
        fetch(`/edit/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: new_content
            })
        })
        .then(response => {
            if (response.ok) {
                container_div.innerHTML = new_content;
                edit_parent.appendChild(edit_button);
            } else {
                container_div.innerHTML = old_content;
                container_div.parentElement.appendChild(error_div);
            }
            like_div.style.display = 'block';
        });
    });
}
