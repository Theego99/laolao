// scripts.js

// Example: Smooth scroll for internal anchor links
document.addEventListener('DOMContentLoaded', function() {
  const anchors = document.querySelectorAll('a[href^="#"]');
  for (let anchor of anchors) {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetID = this.getAttribute('href').substring(1);
      const targetElem = document.getElementById(targetID);
      if (targetElem) {
        window.scroll({
          top: targetElem.offsetTop - 60,
          behavior: 'smooth'
        });
      }
    });
  }
});
