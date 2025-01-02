<script lang="ts">
    import { addAlert } from "$lib/alert";
    import type { ItemRead } from "$lib/Api";
    import { api } from "$lib/auth";
    export let item: ItemRead;

    let editing = false;
    let newQuantity = item.quantity;

    async function saveQuantity() {
        api.itemUpdate(item.id, { quantity: newQuantity })
            .then((_) => {
                item.quantity = newQuantity;
                addAlert("Quantity updated", "success");
                editing = false;
            })
            .catch((res) => {
                addAlert(
                    res.error.detail || "Failed to update quantity",
                    "error",
                );
            });
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
