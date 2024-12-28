<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { modal } from "$lib/store";
    import type { Item } from "$lib/types";

    export let item: Item;
</script>

<Button
    size="xs"
    class="right-4"
    on:click={() => {
        $modal.mode = "edit";
        $modal.item = item;
        $modal.isOpen = true;
        $modal.itemID = item.id;
    }}
>
    x
</Button>
