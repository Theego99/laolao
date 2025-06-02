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
