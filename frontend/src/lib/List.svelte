<script lang="ts">
    import { ws, tab } from "$lib/store";
    import type { Item, ItemFilter } from "$lib/types";
    import { onMount } from "svelte";
    import ItemComp from "$lib/Item.svelte";

    let filter: ItemFilter = {};
    let items: Item[] = [];
    let categories: string[] = [];
    let loading = true;

    // Function to fetch items based on the filter
    async function fetchItems() {
        loading = true;
        try {
            const result = await $ws.readFilteredItems(filter);
            items = result;
            categories = []; // Reset categories
            items.forEach((item) => {
                if (!categories.includes(item.category)) {
                    categories = [...categories, item.category];
                }
            });
        } catch (error) {
            console.error("Failed to fetch items:", error);
        } finally {
            loading = false;
        }
    }

    // Reactively update the filter and fetch items when `$tab` changes
    $: {
        if ($tab === "Active") {
            filter = { is_active: true };
        } else if ($tab === "Inactive") {
            filter = { is_active: false };
        }
        fetchItems();
    }

    function onUpdate(updatedItem: Item) {
        items = items.filter((item) => item.id !== updatedItem.id);
    }
</script>

<main>
    {#if loading}
        <div>Loading...</div>
    {:else}
        {#each categories as category}
            <h2>{category}</h2>
            {#each items as item}
                {#if item.category === category}
                    <ItemComp {item} {onUpdate} />
                {/if}
            {/each}
        {/each}
    {/if}
</main>
