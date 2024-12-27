<script lang="ts">
    import type { Item } from "$lib/types";
    import { items, ws, searching } from "$lib/store";
    import { CloseCircleSolid, CirclePlusSolid } from "flowbite-svelte-icons";
    import { Li } from "flowbite-svelte";
    import Notes from "$components/Notes.svelte";
    export let item: Item;

    async function onclick() {
        if (item.id === undefined) {
            console.error("Item ID is undefined.");
            return;
        }
        try {
            for (let i = 0; i < $items.length; i++) {
                if ($items[i].id === item.id) {
                    $items[i].is_active = !$items[i].is_active;
                    $ws.updateItem(item.id, { is_active: !item.is_active });
                    item = $items[i];
                    break;
                }
            }
            $items = [...$items];
        } catch (error) {
            console.error(`Failed to deactivate item '${item.name}':`, error);
        }
    }
</script>

<Li icon class="m-2 {item.is_active ? 'text-gray-50' : 'text-gray-500'}" id="1">
    <div class="mr-2">
        {#if item.is_active}
            <button on:click={onclick}>
                <CloseCircleSolid />
            </button>
        {:else}
            <button on:click={onclick}>
                <CirclePlusSolid />
            </button>
        {/if}
    </div>
    {item.quantity}
    {item.unit}
    {item.name}
    {#if item.notes !== ""}
        <Notes notes={item.notes} />
    {/if}
</Li>
