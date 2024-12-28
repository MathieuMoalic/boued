<script lang="ts">
    import type { Item } from "$lib/types";
    import { Modal } from "flowbite-svelte";
    import { InfoCircleSolid } from "flowbite-svelte-icons";
    let clickOutsideModal = false;
    export let item: Item;
</script>

{#if item.notes !== ""}
    <button on:click={() => (clickOutsideModal = true)} class="ml-2">
        <InfoCircleSolid />
    </button>

    <Modal bind:open={clickOutsideModal} autoclose outsideclose size="xs">
        {item.notes}
    </Modal>
{/if}
