<script lang="ts">
    import { ws } from "$lib/store";
    import type { Item, ItemFilter } from "$lib/types";
    import { List, Heading } from "flowbite-svelte";
    import ItemComp from "$components/Item.svelte";
    import { onMount } from "svelte";

    let filter: ItemFilter = { is_active: true };
    let items_active: Item[] = [];
    let items_inactive: Item[] = [];
    let categories: string[] = [];
    let loading = true;

    // Function to fetch items based on the filter
    async function fetchItems() {
        loading = true;
        try {
            const activeResult = await $ws.readFilteredItems(filter);
            items_active = activeResult;
            categories = []; // Reset categories
            items_active.forEach((item) => {
                if (!categories.includes(item.category)) {
                    categories = [...categories, item.category];
                }
            });

            const inactiveResult = await $ws.readFilteredItems({
                is_active: false,
            });
            items_inactive = inactiveResult;
        } catch (error) {
            console.error("Failed to fetch items:", error);
        } finally {
            loading = false;
        }
    }

    // Update the lists dynamically when items are activated or deactivated
    function handleItemUpdated(updatedItem: Item) {
        if (updatedItem.is_active) {
            // Move item to the active list
            items_inactive = items_inactive.filter(
                (item) => item.id !== updatedItem.id,
            );
            if (!items_active.find((item) => item.id === updatedItem.id)) {
                items_active = [...items_active, updatedItem];
            }

            // Add the item's category to categories if it doesn't exist
            if (!categories.includes(updatedItem.category)) {
                categories = [...categories, updatedItem.category];
            }
        } else {
            // Move item to the inactive list
            items_active = items_active.filter(
                (item) => item.id !== updatedItem.id,
            );
            if (!items_inactive.find((item) => item.id === updatedItem.id)) {
                items_inactive = [...items_inactive, updatedItem];
            }

            // Remove the category from categories if no active items belong to it
            const remainingItemsInCategory = items_active.filter(
                (item) => item.category === updatedItem.category,
            );
            if (remainingItemsInCategory.length === 0) {
                categories = categories.filter(
                    (category) => category !== updatedItem.category,
                );
            }
        }
    }

    onMount(fetchItems);
</script>

<main>
    {#if loading}
        <div>Loading...</div>
    {:else}
        <List tag="ul" class="space-y-1 text-gray-300" list="none">
            {#each categories as category}
                <Heading tag="h5" class="text-gray-200">
                    {category}
                </Heading>
                {#each items_active as item}
                    {#if item.category === category}
                        <ItemComp {item} onItemUpdated={handleItemUpdated} />
                    {/if}
                {/each}
            {/each}
        </List>
    {/if}
    <hr />
    <Heading tag="h5" class="text-gray-500">Inactive items</Heading>
    <List tag="ul" class="space-y-1 text-gray-500" list="none">
        {#each items_inactive as item}
            <ItemComp {item} onItemUpdated={handleItemUpdated} />
        {/each}
    </List>
</main>
