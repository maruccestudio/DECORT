(function () {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return; // deja el toggle nativo instantaneo, sin JS de por medio
    }

    var EASE_OUT = 'cubic-bezier(0.16, 1, 0.3, 1)'; // este proyecto's ease-out - ver DESIGN.md / index.html --ease-out
    var DURATION = 350; // ms - dentro del rango 200-500ms de AUDIT.md para drawers

    document.querySelectorAll('details').forEach(function (details) {
        var summary = details.querySelector('summary');
        var content = details.querySelector('summary + *');
        if (!summary || !content) return;
        var animating = false;

        summary.addEventListener('click', function (e) {
            e.preventDefault();
            if (animating) return;
            animating = true;

            if (!details.open) {
                details.style.overflow = 'hidden';
                details.open = true;
                var contentHeight = content.getBoundingClientRect().height;
                var anim = details.animate(
                    { height: [summary.getBoundingClientRect().height + 'px', (summary.getBoundingClientRect().height + contentHeight) + 'px'] },
                    { duration: DURATION, easing: EASE_OUT }
                );
                anim.onfinish = function () {
                    details.style.height = '';
                    details.style.overflow = '';
                    animating = false;
                };
            } else {
                details.style.overflow = 'hidden';
                var startHeight = details.getBoundingClientRect().height;
                var endHeight = summary.getBoundingClientRect().height;
                var anim = details.animate(
                    { height: [startHeight + 'px', endHeight + 'px'] },
                    { duration: DURATION, easing: EASE_OUT }
                );
                anim.onfinish = function () {
                    details.open = false;
                    details.style.height = '';
                    details.style.overflow = '';
                    animating = false;
                };
            }
        });
    });
})();
