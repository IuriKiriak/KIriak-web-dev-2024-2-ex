function closeToastDuration() {
    let toasts = document.querySelectorAll('.alert');
    toasts.forEach(toast => {
        let durationBar = toast.querySelector('.toast-duration');
        if (durationBar) {
            setTimeout(() => {
                toast.remove();
            }, 10000);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    closeToastDuration();

    let mutationObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            closeToastDuration();
        });
    });

    if (document.getElementById('alert-container')) {
        mutationObserver.observe(document.getElementById('alert-container'), {
            attributes: true,
            characterData: true,
            childList: true,
            subtree: true,
            attributeOldValue: true,
            characterDataOldValue: true
        });
    }
});

//////////////////////////////////////////////////////////////////////////////////////////////////

//var myModal = new bootstrap.Modal(document.getElementById('loginModal'), {
//    keyboard: false
//})
//myModal.show()

//{% if session['login_error'] == True %}
//    <script>
//        var myModal = new bootstrap.Modal(document.getElementById('loginModal'), {
//            keyboard: false
//        })
//        myModal.show()
//    </script>
//{% endif %}