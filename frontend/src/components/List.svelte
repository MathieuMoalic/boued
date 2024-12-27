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
            const result = await $ws.readFilteredItems(filter);
            items_active = result;
            categories = []; // Reset categories
            items_active.forEach((item) => {
                if (!categories.includes(item.category)) {
                    categories = [...categories, item.category];
                }
            });
        } catch (error) {
            console.error("Failed to fetch items:", error);
        } finally {
            loading = false;
        }
        try {
            const result = await $ws.readFilteredItems({ is_active: false });
            items_inactive = result;
        } catch (error) {
            console.error("Failed to fetch items:", error);
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
                        <ItemComp {item} />
                    {/if}
                {/each}
            {/each}
        </List>
    {/if}
    <hr />
    <Heading tag="h5" class="text-gray-500">Inactive items</Heading>
    <List tag="ul" class="space-y-1 text-gray-500" list="none">
        {#each items_inactive as item}
            <ItemComp {item} />
        {/each}
    </List>
</main>
