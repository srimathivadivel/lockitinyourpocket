document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('nav a');

  for (const link of links) {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const targetId = link.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);

      window.scrollTo({
        top: targetElement.offsetTop - document.querySelector('nav').offsetHeight,
        behavior: 'smooth'
      });
    });
  }
});

