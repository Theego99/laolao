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

/*  EMAIL CONTACT FUNCTIONALITY  */

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

// SCRIPT TO TOGGLE MODE LIGHT/DARK
;(function() {
  const toggleBtn = document.getElementById('themeToggle');
  const bodyEl    = document.body;
  const DARK_CLASS = 'dark-mode';
  const STORAGE_KEY = 'laolaoTheme';

  const savedTheme = localStorage.getItem(STORAGE_KEY);
  if (savedTheme === 'dark') {
    bodyEl.classList.add(DARK_CLASS);
    toggleBtn.textContent = '☀️';
  } else {
    bodyEl.classList.remove(DARK_CLASS);
    toggleBtn.textContent = '🌙';
  }

  function switchTheme() {
    const isDark = bodyEl.classList.toggle(DARK_CLASS);
    if (isDark) {
      toggleBtn.textContent = '☀️';
      localStorage.setItem(STORAGE_KEY, 'dark');
    } else {
      toggleBtn.textContent = '🌙';
      localStorage.setItem(STORAGE_KEY, 'light');
    }
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', switchTheme);
  }
})();