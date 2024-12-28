<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { modal } from "$lib/store";
    import type { Item } from "$lib/types";
    import { EditOutline } from "flowbite-svelte-icons";

    export let item: Item;
</script>

<Button
    size="sm"
    class="m-1 p-1 border-0"
    outline
    on:click={() => {
        $modal.mode = "edit";
        $modal.item = item;
        $modal.isOpen = true;
        $modal.itemID = item.id;
    }}
>
    <EditOutline size="md" />
</Button>
