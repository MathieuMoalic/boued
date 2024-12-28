<script lang="ts">
    import { Dropdown, DropdownItem, Button } from "flowbite-svelte";

    import { ws } from "$lib/store";
    import type { Item } from "$lib/types";

    export let item: Item;

    let possibleUnits = ["kg", "g", "l", "ml", "pcs", "cans", "bottles"];
    let editingUnit = false;

    async function saveUnit(unit: string) {
        if (unit === item.unit) return;

        try {
            item.unit = unit;
            await $ws.updateItem(item.id, { unit });
        } catch (error) {
            console.error(
                `Failed to update unit for item '${item.name}':`,
                error,
            );
        }
    }
</script>

<div>
    <Button
        outline
        class="m-0 p-0 border-opacity-0 {item.is_active
            ? 'text-gray-50'
            : 'text-gray-500'}
        text-lg rounded-sm
        "
    >
        {item.unit}
    </Button>
    <Dropdown bind:open={editingUnit}>
        {#each possibleUnits as unit}
            <DropdownItem
                class="text-gray-200 bg-red-800"
                on:click={() => {
                    saveUnit(unit);
                    editingUnit = false;
                }}>{unit}</DropdownItem
            >
        {/each}
    </Dropdown>
</div>
