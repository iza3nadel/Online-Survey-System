
if(document.querySelector('.admin-panel')){
    document.querySelector('.admin-panel').addEventListener('click', function(e) {
        e.preventDefault();
        document.body.style.transition = 'opacity 0.5s';
        document.body.style.opacity = 0;
        setTimeout(function() {
            window.location.href = '/main';
        }, 500);
    });
}

if(document.querySelector('.form')){
    document.querySelector('.form').addEventListener('click', function(e) {
        e.preventDefault();
        document.body.style.transition = 'opacity 0.5s';
        document.body.style.opacity = 0;
        setTimeout(function() {
            window.location.href = '/form';
        }, 500);
    });
}

if(document.body){
    document.body.style.opacity = 0;
    document.body.style.transition = 'opacity 0.5s';
    window.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            document.body.style.opacity = 1;
        }, 50);
    });
}
