<script lang="ts">
    export let className: string = "w-6 h-6";
    export let color: string = "red";
</script>

<svg class={className} fill="none" stroke={color} viewBox="0 0 24 24">
    <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M6 18L18 6M6 6l12 12"
    />
</svg>
