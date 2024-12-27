<script lang="ts">
    import type { Item } from "$lib/types";
    import { ws } from "$lib/store";
    import {
        CloseCircleSolid,
        CirclePlusSolid,
        InfoCircleSolid,
    } from "flowbite-svelte-icons";
    import { Li } from "flowbite-svelte";
    export let item: Item;
    export let onItemUpdated: (updatedItem: Item) => void;

    async function deactivateItem() {
        if (item.id === undefined) {
            console.error("Item ID is undefined.");
            return;
        }
        try {
            await $ws.updateItem(item.id, { is_active: false });
            item.is_active = false;
            onItemUpdated(item);
        } catch (error) {
            console.error(`Failed to deactivate item '${item.name}':`, error);
        }
    }

    async function activateItem() {
        if (item.id === undefined) {
            console.error("Item ID is undefined.");
            return;
        }
        try {
            await $ws.updateItem(item.id, { is_active: true });
            item.is_active = true;
            onItemUpdated(item);
        } catch (error) {
            console.error(`Failed to activate item '${item.name}':`, error);
        }
    }

    function showInfo() {
        console.log("i");
    }
</script>

<Li icon>
    {#if item.is_active}
        <button on:click={deactivateItem}>
            <CloseCircleSolid />
        </button>
    {:else}
        <button on:click={activateItem}>
            <CirclePlusSolid />
        </button>
    {/if}
    {item.quantity}
    {item.unit}
    {item.name}
    {#if item.notes !== ""}
        <button on:click={showInfo}>
            <InfoCircleSolid />
        </button>
    {/if}
</Li>
