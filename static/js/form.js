const form = document.getElementById('contact-form');

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(form);

  const name = formData.get('name');
  const email = formData.get('email');
  const phone = formData.get('phone');
  const message = formData.get('message');

  if (!name || !email || !phone || !message) {
    alert('Please, fill all fields!');
    return;
  }

  const contactData = {
    name: name,
    email: email,
    phone: phone,
    message: message
  }
  submitFormData(contactData);
});

const form_messages = document.getElementById('form-messages');

const submitFormData = async (formData) => {
  try {
    const response = await fetch('/api/v1/shekharsikku/portfolio/users', {
      'method': 'POST',
      'headers': { 'Content-Type': 'application/json' },
      'body': JSON.stringify(formData)
    });
    if (response) {
      const data = await response.json();

      const name = document.getElementById('contact-name');
      const email = document.getElementById('contact-email');
      const phone = document.getElementById('contact-phone');
      const message = document.getElementById('contact-message');

      if (data) {
        name.value = '';
        email.value = '';
        phone.value = '';
        message.value = '';

        form_messages.innerText = data.message;

        setTimeout(() => {
          form_messages.innerText = '';
          console.log(data);
        }, 10000);
      }
    } else {
      throw new Error('Oops! It seems there was an issue with your submission!')
    }
  } catch (error) {
    form_messages.innerText = error.message;

    setTimeout(() => {
      form_messages.innerText = '';
      console.error(error.message)
    }, 10000);
  }
}
