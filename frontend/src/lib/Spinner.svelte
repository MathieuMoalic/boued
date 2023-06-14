<div>
    <div id="html-spinner" />
</div>

<style>
    #html-spinner {
        width: 15px;
        height: 15px;
        border: 3px solid #ffffff;
        border-top: 3px solid rgb(0, 0, 0);
        border-radius: 50%;
        transition-property: transform;
        animation-name: rotate;
        animation-duration: 0.6s;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
    }
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>
