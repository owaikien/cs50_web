document.addEventListener('DOMContentLoaded', function() {
  console.log('Script loaded!')

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  const form = document.querySelector('#compose-form');

  // Check if the form exists
  if (!form) {
    console.log('Form not found!');
  } else {
    console.log('Form found! Adding submit event listener...');
    // send email
    form.addEventListener('submit', send_email);
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email=null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // for replying emails
  if(email) {
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = email.subject.startsWith('Re: ')  ? email.subject : `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;  
  }
}

let currentMailbox = 'inbox';
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Update the current mailbox
  currentMailbox = mailbox;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // use a for loop for each email
      emails.forEach(email => {

        // create a new div for each email
        const emailDiv = document.createElement('div');
        emailDiv.className = 'email';
        emailDiv.style.border = '1px solid black';
        emailDiv.style.marginBottom = '10px';

        // set its innerHTML to contain information about the email
        emailDiv.innerHTML = `
        <div class = 'email-recipients'>${email.recipients} </div>
        <div class = 'email-subject'>${email.subject} </div>
        <div class = 'email-timestamp'>${email.timestamp} </div>
        `;

        // set its background colour whether it is read or not 
        emailDiv.style.backgroundColor = email.read ? 'grey': 'white';

        // add view individual email event listener to the div
        emailDiv.addEventListener('click', () => load_email(email.id, currentMailbox));

        // append to emailsView
        document.querySelector('#emails-view').appendChild(emailDiv);
      })
  });
}

function send_email(event){

  // Prevent form deafult behaviour
  event.preventDefault();

    // Store fields
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent');
    });
}

function load_email(id, mailbox){
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })

      // load the email view
      .then(() => {
        // hide other views
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';

        // create new email view
        const emailView = document.querySelector('#email-view');
        emailView.style.display = 'block';

        // clear out previus view
        emailView.innerHTML = '';

        // add details of HTML
        emailView.innerHTML = `
          <button id ='back-to-inbox'>Back</button><br>
          <button id = 'reply'>Reply</button><br>
          <button id ='archive-unarchive-inbox'></button><br>
          <b>From:</b> ${email.sender}<br>
          <b>To:</b> ${email.recipients}<br>
          <b>Subject:</b> ${email.subject}<br>
          <b>Timestamp:</b> ${email.timestamp}<br>
          <hr>
          <b>Body:</b><br>
          ${email.body}
        `;

        // Send the text and action of button depending on the mailbox
        const archiveButton = document.querySelector('#archive-unarchive-inbox');
        if (mailbox === 'inbox'){
          archiveButton.textContent = 'Archive';
          archiveButton.addEventListener('click', () => archive_email(id, true));
        } else if (mailbox === 'archive'){
          archiveButton.textContent = 'Unarchive';
          archiveButton.addEventListener('click', () => archive_email(id, false));
        } else {
          archiveButton.style.display = 'none';
        }
        
        // Add event listener to the "Back to Inbox" button
        document.querySelector('#back-to-inbox').addEventListener('click', () => load_mailbox(mailbox));

        // Add even listener to the "Reply" button
        document.querySelector('#reply').addEventListener('click', () => compose_email(email))
    });
  });
}

function archive_email(id, archive){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archive
    })
  })
  .then(() => load_mailbox('inbox'));
}