<div class="gdl-glow"></div>

<style>
    .gdl-glow {
        position: fixed;
        top: 110%;
        left: 50%;
        width: 50px;
        height: 50px;
        box-shadow: inset 0 0 400px 400px rgba(255, 255, 255, 0.1);
        filter: blur(10px);
        z-index: -1;
        scale: 10;
        animation: blur 5s infinite alternate;
    }

    @keyframes blur {
        0% {
            opacity: 0.0;
        }
        100% {
            opacity: 0.4;
        }
    }
</style>