(function() {
    const display = document.getElementById('display');
    const keys = document.querySelector('.keys');

    keys.addEventListener('click', function(e) {
        const target = e.target;
        if (!target.classList.contains('key')) return;

        const value = target.dataset.value;
        const action = target.dataset.action;

        if (action === 'clear') {
            display.value = '';
            return;
        }
        if (action === 'delete') {
            display.value = display.value.slice(0, -1);
            return;
        }
        if (action === 'calculate') {
            try {
                display.value = eval(display.value) || '';
            } catch {
                display.value = 'Error';
            }
            return;
        }

        display.value += value;
    });
})();
