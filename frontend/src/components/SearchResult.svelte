<script lang="ts">
    import { searchResults } from "$lib/store";
    import { List } from "flowbite-svelte";
    import ItemComp from "$components/Item.svelte";
</script>

<main>
    {#if $searchResults.length > 0}
        <List tag="ul" class="space-y-1">
            {#each $searchResults as item}
                <ItemComp {item} />
            {/each}
        </List>
    {:else}
        No results found.
    {/if}
</main>
