<script lang="ts">
    import { Button, Modal } from "flowbite-svelte";
    import { InfoCircleSolid } from "flowbite-svelte-icons";
    let clickOutsideModal = false;
    export let notes: string | undefined;
</script>

<button on:click={() => (clickOutsideModal = true)} class="ml-2">
    <InfoCircleSolid />
</button>

<Modal bind:open={clickOutsideModal} autoclose outsideclose size="xs">
    {notes}
</Modal>
