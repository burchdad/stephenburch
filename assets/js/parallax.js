document.addEventListener('scroll', function () {
    const layers = document.querySelectorAll('.parallax-layer');
    const top = window.pageYOffset;

    layers.forEach(layer => {
        const speed = layer.getAttribute('data-speed');
        const yPos = -(top * speed / 100);
        layer.style.transform = `translateY(${yPos}px)`;
    });
});
