window.onload = function() {
    var navItems = document.querySelectorAll('.nav-bar ul li a');

    navItems.forEach(function(item) {
        item.addEventListener('mouseover', function() {
            this.style.color = "#80ffb3";
        });

        item.addEventListener('mouseout', function() {
            this.style.color = 'white';
        });
    });
};