<script lang="ts">
    import { items as items_store, searchResults } from "$lib/store";
    import { List } from "flowbite-svelte";
    import ItemComp from "$components/Item.svelte";
    import { onMount } from "svelte";
</script>

<main>
    {#if $searchResults.length > 0}
        <List tag="ul" class="space-y-1 text-gray-500">
            {#each $searchResults as item}
                <ItemComp {item} onItemUpdated={() => {}} />
            {/each}
        </List>
    {:else}
        No results found.
    {/if}
</main>
