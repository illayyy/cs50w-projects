document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#email-archive-button').addEventListener('click', archive_email);
  document.querySelector('#email-reply-button').addEventListener('click', reply_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  load_mailbox('inbox');
});


function archive_email(event) {
  const email = event.target
  const email_id = email.dataset.email_id;
  const archived = (email.dataset.archived === 'true');
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archived
    })
  })
  .then(() => load_mailbox('inbox'));
}


function reply_email(event) {
  const email = event.target
  const sender = email.dataset.sender;
  const subject = `RE: ${email.dataset.subject}`;
  const body = `${sender} ${email.dataset.timestamp}:\n${email.dataset.body}\n\n`;

  compose_email(event, sender, subject, body);
}


function compose_email(event, recipients='', subject='', body='') {
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

  document.querySelector('#compose-error').style.display = 'none';

  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
}


function load_mailbox(mailbox) {
  document.querySelector('#mailbox-view').innerHTML = `<h3>${mailbox[0].toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => emails.forEach(display_email_item))
  .then(() => {
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#mailbox-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
  });
}


function display_email_item(email) {
  const container = document.createElement('div');
  const sender = document.createElement('div');
  const subject = document.createElement('div');
  const timestamp = document.createElement('div');
  const linebreak = document.createElement('div');

  container.className = "item-container";
  sender.className = "item-sender";
  subject.className = "item-subject";
  timestamp.className = "item-timestamp";
  linebreak.className = "item-linebreak";

  sender.innerHTML = email.sender;
  subject.innerHTML = email.subject;
  timestamp.innerHTML = email.timestamp;

  container.append(sender, subject, timestamp, linebreak);
  container.addEventListener('click', view_email);
  container.id = email.id;
  if (email.read) {
    container.className += " item-read";
  }

  document.querySelector('#mailbox-view').append(container);
}


function view_email(event) {
  const email_id = event.currentTarget.id;
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
    .then(() => {

      document.querySelector('#email-sender').innerHTML = `<strong>From: </strong>${email.sender}`;
      document.querySelector('#email-recipients').innerHTML = `<strong>To: </strong>${email.recipients}`;
      document.querySelector('#email-subject').innerHTML = `<strong>Subject: </strong>${email.subject}`;
      document.querySelector('#email-timestamp').innerHTML = `<strong>Timestamp: </strong>${email.timestamp}`;
      document.querySelector('#email-body').innerHTML = email.body;

      const reply_button = document.querySelector('#email-reply-button');
      reply_button.setAttribute('data-subject', email.subject);
      reply_button.setAttribute('data-sender', email.sender);
      reply_button.setAttribute('data-timestamp', email.timestamp);
      reply_button.setAttribute('data-body', email.body);

      const archive_button = document.querySelector('#email-archive-button');
      if (email.sender === document.querySelector('#user-email').innerHTML) {
        archive_button.style.display = 'none';
      } else {
        archive_button.style.display = 'inline-block';
        archive_button.setAttribute('data-email_id', email_id);
        archive_button.setAttribute('data-archived', email.archived);
        if (email.archived) {
          archive_button.innerHTML = "Unarchive";
        } else {
          archive_button.innerHTML = "Archive";
        }
      }

      document.querySelector('#email-view').style.display = 'block';
      document.querySelector('#mailbox-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
    });
  });
}


function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => {
    if (response.ok) {
      load_mailbox('sent')
    }
    else {
      document.querySelector('#compose-error').style.display = 'block';
    }
  })
}