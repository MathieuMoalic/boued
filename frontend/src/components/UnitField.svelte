<script lang="ts">
    import { Dropdown, DropdownItem, Button } from "flowbite-svelte";

    import { possibleUnits } from "$lib/types";
    import type { ItemRead } from "$lib/Api";
    import { addAlert } from "$lib/alert";
    import { api } from "$lib/store";

    export let item: ItemRead;

    let editingUnit = false;

    async function saveUnit(unit: string) {
        if (unit === item.unit) return;
        api.items
            .update(item.id, { unit })
            .then((_) => {
                item.unit = unit;
                addAlert("Unit updated", "success");
            })
            .catch((res) => {
                addAlert(res.error.detail || "Failed to update unit", "error");
            });
    }
</script>

<div>
    {#if item.unit === "None"}
        <span class="text-gray-200"></span>
    {:else}
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
    {/if}
</div>
