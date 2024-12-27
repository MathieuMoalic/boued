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

    function deactivateItem() {
        if (item.id === undefined) {
            console.error("Item ID is undefined.");
            return;
        }
        $ws.updateItem(item.id, { is_active: false })
            .catch((error: any) => {
                console.error(
                    `Failed to deactivate item '${item.name}':`,
                    error,
                );
            })
            .then(() => {
                item.is_active = false;
            });
    }
    function activateItem() {
        if (item.id === undefined) {
            console.error("Item ID is undefined.");
            return;
        }
        $ws.updateItem(item.id, { is_active: true })
            .catch((error: any) => {
                console.error(`Failed to activate item '${item.name}':`, error);
            })
            .then(() => {
                item.is_active = true;
            });
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
