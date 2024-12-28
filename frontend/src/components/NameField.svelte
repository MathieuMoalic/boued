<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { ws } from "$lib/store";
    import type { Item } from "$lib/types";
    export let item: Item;

    let editing = false;
    let newName = item.name;

    async function saveName() {
        if (newName === item.name) {
            editing = false;
            return;
        }

        try {
            item.name = newName;
            await $ws.updateItem(item.id, { name: newName });
        } catch (error) {
            console.error(
                `Failed to update name for item '${item.name}':`,
                error,
            );
            addAlert("Failed to update the name", "error");
        } finally {
            editing = false;
        }
    }
</script>

<div>
    {#if editing}
        <input
            bind:value={newName}
            class="w-12 h-6 mr-3 text-center rounded bg-red-700 text-gray-200"
            on:blur={saveName}
            on:keydown={(e) => e.key === "Enter" && saveName()}
        />
    {:else}
        <button
            type="button"
            on:click={() => (editing = true)}
            class="pl-1"
            aria-label="Edit name"
        >
            {item.name}
        </button>
    {/if}
</div>
