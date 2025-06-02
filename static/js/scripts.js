// static/js/scripts.js
// Example: Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', () => {
  const anchors = document.querySelectorAll('a[href^="#"]');
  anchors.forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const targetID = anchor.getAttribute('href').substring(1);
      const targetElem = document.getElementById(targetID);
      if (targetElem) {
        window.scroll({
          top: targetElem.offsetTop - 60,
          behavior: 'smooth'
        });
      }
    });
  });
});

/*-----------------------------------------------
EMAIL CONTACT FUNCTIONALITY
*/

// Function to handle email contact form submission
function sendMail() {
  let params = {
    name : document.getElementById("name").value,
    email : document.getElementById("email").value,
    subject : document.getElementById("subject").value,  
    message : document.getElementById("message").value
  }

  email.send("service_1x3k2qj", "template_9g4v5zj", params).then(alert("Your inquiry has been sent successfully!"))
}

