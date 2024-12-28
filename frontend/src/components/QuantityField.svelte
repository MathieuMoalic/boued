<script lang="ts">
    import { ws } from "$lib/store";
    import type { Item } from "$lib/types";
    export let item: Item;

    let editing = false;
    let newQuantity = item.quantity;

    async function saveQuantity() {
        if (newQuantity === item.quantity) {
            editing = false;
            return;
        }

        try {
            item.quantity = newQuantity;
            await $ws.updateItem(item.id, { quantity: newQuantity });
        } catch (error) {
            console.error(
                `Failed to update quantity for item '${item.name}':`,
                error,
            );
        } finally {
            editing = false;
        }
    }
</script>

<div>
    {#if item.quantity === null}
        <span class="text-gray-200"></span>
    {:else if editing}
        <input
            bind:value={newQuantity}
            class="w-12 h-6 mr-3 text-center rounded bg-red-700 text-gray-200"
            on:blur={saveQuantity}
            on:keydown={(e) => e.key === "Enter" && saveQuantity()}
        />
    {:else}
        <button
            type="button"
            on:click={() => (editing = true)}
            class="p-1"
            aria-label="Edit quantity"
        >
            {item.quantity}
        </button>
    {/if}
</div>
