<script lang="ts">
    import type { Item } from "$lib/types";
    import { Modal } from "flowbite-svelte";
    let clickOutsideModal = false;
    export let item: Item;
</script>

{#if item.notes !== ""}
    <div class="flex items-center pl-2 overflow-hidden">
        <button
            on:click={() => (clickOutsideModal = true)}
            class="ml-1 flex-shrink-0 text-gray-500 truncate overflow-hidden text-ellipsis whitespace-nowrap max-w-xs"
            title={item.notes}
        >
            | {item.notes}
        </button>

        <Modal bind:open={clickOutsideModal} autoclose outsideclose>
            <div class="pr-1">
                {item.notes}
            </div>
        </Modal>
    </div>
{/if}
