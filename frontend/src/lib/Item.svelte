<script lang="ts">
    import type { Item } from "$lib/types";
    import { ws } from "$lib/store";
    export let item: Item;

    function deactivateItem() {
        if (item.id === undefined) {
            console.error("Item ID is undefined.");
            return;
        }
        $ws.updateItem(item.id, { is_active: false }).catch((error: any) => {
            console.error(`Failed to deactivate item '${item.name}':`, error);
        });
    }

    function showInfo() {
        console.log("i");
    }
</script>

<div class="item-row">
    <button class="delete-button" on:click={deactivateItem}>x</button>
    <div class="item-content">
        <!-- Display quantity, unit, then name -->
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

    .delete-button,
    .info-button {
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        font-size: 1rem;
        border: none;
        background-color: #f0f0f0;
        border-radius: 4px;
    }

    .delete-button {
        margin-right: 1rem;
    }

    .item-content {
        flex-grow: 1;
    }

    .info-button {
        margin-left: auto;
    }
</style>
