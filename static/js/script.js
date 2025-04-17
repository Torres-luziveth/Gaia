const monthSelector = document.getElementById('month-selector');
const calendar = document.getElementById('calendar');

let markedDays = JSON.parse(localStorage.getItem('markedDays')) || {};

function saveMarkedDays() {
    localStorage.setItem('markedDays', JSON.stringify(markedDays));
}

function getDaysInMonth(month, year) {
    return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfMonth(month, year) {
    const day = new Date(year, month, 1).getDay();
    return (day === 0) ? 6 : day - 1;
}

function generateCalendar(month, year) {
    while (calendar.children.length > 7) {
        calendar.removeChild(calendar.lastChild);
    }

    const daysInMonth = getDaysInMonth(month, year);
    const firstDay = getFirstDayOfMonth(month, year);

    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.classList.add('day', 'empty');
        calendar.appendChild(emptyDay);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day');
        dayElement.setAttribute('data-day', day);
        dayElement.textContent = day;

        const key = `${year}-${month}-${day}`;
        if (markedDays[key] === 'x') {
            dayElement.classList.add('marked-x');
        } else if (markedDays[key] === 'check') {
            dayElement.classList.add('marked-check');
        }

        calendar.appendChild(dayElement);
    }

    document.querySelectorAll('.day:not(.header):not(.empty)').forEach(day => {
        day.addEventListener('click', () => {
            const dayNum = day.getAttribute('data-day');
            const key = `${year}-${month}-${dayNum}`;

            if (day.classList.contains('marked-x')) {
                day.classList.remove('marked-x');
                day.classList.add('marked-check');
                markedDays[key] = 'check';
            } else if (day.classList.contains('marked-check')) {
                day.classList.remove('marked-check');
                delete markedDays[key];
            } else {
                day.classList.add('marked-x');
                markedDays[key] = 'x';
            }

            saveMarkedDays();
        });
    });
}

generateCalendar(2, 2025);

monthSelector.addEventListener('change', () => {
    const selectedMonth = parseInt(monthSelector.value);
    generateCalendar(selectedMonth, 2025);
});

function mostrar() {
    
    const input = document.getElementById("password");
    input.type = input.type === "password" ? "text" : "password";
}