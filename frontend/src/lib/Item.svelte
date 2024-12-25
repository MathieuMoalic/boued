<script lang="ts">
    import type { Item } from "$lib/types";
    import { ws } from "$lib/store";
    export let item: Item;
    export let onUpdate: (item: Item) => void; // Callback passed from parent

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
                onUpdate(item); // Notify parent
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
                onUpdate(item); // Notify parent
            });
    }

    function showInfo() {
        console.log("i");
    }
</script>

<div class="item-row">
    {#if item.is_active}
        <button class="deactivate-button" on:click={deactivateItem}>x</button>
    {:else}
        <button class="activate-button" on:click={activateItem}>+</button>
    {/if}
    <div class="item-content">
        {item.quantity}
        {item.unit}
        {item.name}
    </div>
    <button class="info-button" on:click={showInfo}>i</button>
</div>

<style>
    .item-row {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
    }

    .deactivate-button,
    .activate-button,
    .info-button {
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        font-size: 1rem;
        border: none;
        background-color: #f0f0f0;
        border-radius: 4px;
    }

    .deactivate-button,
    .activate-button {
        margin-right: 1rem;
    }

    .item-content {
        flex-grow: 1;
    }

    .info-button {
        margin-left: auto;
    }
</style>
