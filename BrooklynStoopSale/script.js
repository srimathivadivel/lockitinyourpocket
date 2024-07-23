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

function getTimeRemaining(endTime) {
    const total = Date.parse(endTime) - Date.parse(new Date());
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
    const days = Math.floor(total / (1000 * 60 * 60 * 24));

    return {
        total, 
        days,
        hours,
        minutes,
        seconds
    };
}


function initializeClock(id, endTime) {
    const clock = document.getElementById(id);
    const daysSpan = clock.querySelector('#days');
    const hoursSpan = clock.querySelector('#hours');
    const minutesSpan = clock.querySelector('#minutes');
    const secondsSpan = clock.querySelector('#seconds');

    function updateClock() {
        const t = getTimeRemaining(endTime);

        daysSpan.innerHTML = t.days;
        hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
        minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
        secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

        if (t.total <= 0) {
            clearInterval(timeinterval);
            clock.innerHTML = "EXPIRED";
        } else {
            daysSpan.innerHTML = ('0' + t.days).slice(-2);
            hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
            minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
            secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);
        }
    }

    updateClock();
    const timeinterval = setInterval(updateClock, 1000);
}

const now = new Date();
const deadline = new Date(Date.parse(now) + 34 * 24 * 60 * 60 * 1000);
initializeClock('countdown', deadline);
