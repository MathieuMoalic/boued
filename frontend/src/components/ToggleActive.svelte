<script lang="ts">
    import { ws, items } from "$lib/store";
    import type { Item } from "$lib/types";
    import { CloseCircleSolid, CirclePlusSolid } from "flowbite-svelte-icons";
    export let item: Item;

    async function toggleActive() {
        try {
            item.is_active = !item.is_active;
            for (let i = 0; i < $items.length; i++) {
                if ($items[i].id === item.id) {
                    $items[i].is_active = item.is_active;
                    break;
                }
            }
            await $ws.updateItem(item.id, { is_active: item.is_active });
        } catch (error) {
            console.error(
                `Failed to toggle active status for item '${item.name}':`,
                error,
            );
        }
    }
</script>

<div class="mr-2">
    {#if item.is_active}
        <button on:click={toggleActive}>
            <CloseCircleSolid />
        </button>
    {:else}
        <button on:click={toggleActive}>
            <CirclePlusSolid />
        </button>
    {/if}
</div>
