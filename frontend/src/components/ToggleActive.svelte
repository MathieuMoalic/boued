<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { items } from "$lib/store";
    import type { ItemRead } from "$lib/Api";
    import { CloseOutline, PlusOutline } from "flowbite-svelte-icons";
    export let item: ItemRead;

    async function toggleActive() {
        // try {
        //     item.is_active = !item.is_active;
        //     for (let i = 0; i < $items.length; i++) {
        //         if ($items[i].id === item.id) {
        //             $items[i].is_active = item.is_active;
        //             break;
        //         }
        //     }
        //     await $ws.updateItem(item.id, { is_active: item.is_active });
        // } catch (error) {
        //     console.error(
        //         `Failed to toggle active status for item '${item.name}':`,
        //         error,
        //     );
        //     addAlert("Failed to toggle the active status", "error");
        // }
    }
</script>

<div class="mr-1 mt-1.5">
    {#if item.is_active}
        <button on:click={toggleActive}>
            <CloseOutline />
        </button>
    {:else}
        <button on:click={toggleActive}>
            <PlusOutline />
        </button>
    {/if}
</div>
