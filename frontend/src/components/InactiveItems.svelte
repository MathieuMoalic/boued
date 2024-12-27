<script lang="ts">
    import { items } from "$lib/store";
    import { List, Heading } from "flowbite-svelte";
    import ItemComp from "$components/Item.svelte";
</script>

<main>
    <Heading tag="h5" class="text-gray-500">Inactive</Heading>
    <List tag="ul" class="space-y-1 text-gray-500">
        {#each $items as item}
            {#if !item.is_active}
                <ItemComp {item} onItemUpdated={() => {}} />
            {/if}
        {/each}
    </List>
</main>
