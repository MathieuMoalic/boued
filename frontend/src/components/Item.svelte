<script lang="ts">
    import type { Item } from "$lib/types";
    import { items, ws } from "$lib/store";
    import { CloseCircleSolid, CirclePlusSolid } from "flowbite-svelte-icons";
    import { Li, Dropdown, DropdownItem, Button } from "flowbite-svelte";
    import Notes from "$components/Notes.svelte";
    export let item: Item;
    let editingQuantity = false;
    let newQuantity = item.quantity;
    let editingUnit = false;
    let newUnit = item.unit;
    let editingName = false;
    let newName = item.name;
    let possibleUnits = ["kg", "g", "l", "ml", "pcs", "cans", "bottles"];

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

    async function saveQuantity() {
        if (newQuantity === item.quantity) {
            editingQuantity = false;
            return; // No changes made
        }

        try {
            for (let i = 0; i < $items.length; i++) {
                if ($items[i].id === item.id) {
                    $items[i].quantity = newQuantity;
                    if (item.id === undefined) {
                        console.error("Item ID is undefined.");
                        return;
                    }
                    await $ws.updateItem(item.id, { quantity: newQuantity });
                    item = $items[i];
                    break;
                }
            }
            $items = [...$items];
        } catch (error) {
            console.error(
                `Failed to update quantity for item '${item.name}':`,
                error,
            );
        } finally {
            editingQuantity = false;
        }
    }

    async function saveUnit() {
        if (newUnit === item.unit) {
            editingUnit = false;
            return; // No changes made
        }

        try {
            for (let i = 0; i < $items.length; i++) {
                if ($items[i].id === item.id) {
                    $items[i].unit = newUnit;
                    if (item.id === undefined) {
                        console.error("Item ID is undefined.");
                        return;
                    }
                    await $ws.updateItem(item.id, { unit: newUnit });
                    item = $items[i];
                    break;
                }
            }
            $items = [...$items];
        } catch (error) {
            console.error(
                `Failed to update unit for item '${item.name}':`,
                error,
            );
        } finally {
            editingUnit = false;
        }
    }

    async function saveName() {
        if (newName === item.name) {
            editingName = false;
            return; // No changes made
        }

        try {
            for (let i = 0; i < $items.length; i++) {
                if ($items[i].id === item.id) {
                    $items[i].name = newName;
                    if (item.id === undefined) {
                        console.error("Item ID is undefined.");
                        return;
                    }
                    await $ws.updateItem(item.id, { name: newName });
                    item = $items[i];
                    break;
                }
            }
            $items = [...$items];
        } catch (error) {
            console.error(
                `Failed to update name for item '${item.name}':`,
                error,
            );
        } finally {
            editingName = false;
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

    <!-- Quantity Field -->
    {#if editingQuantity}
        <input
            bind:value={newQuantity}
            class="w-12 h-6 mr-3 text-center rounded bg-red-700 text-gray-200"
            on:blur={saveQuantity}
            on:keydown={(e) => e.key === "Enter" && saveQuantity()}
        />
    {:else}
        <button
            type="button"
            on:click={() => {
                editingQuantity = true;
            }}
            on:keydown={(e) => e.key === "Enter" && (editingQuantity = true)}
            aria-label="Edit quantity"
            class="w-12 mr-3 p-1"
        >
            {item.quantity}
        </button>
    {/if}

    <!-- Unit Field -->
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
                    newUnit = unit;
                    saveUnit();
                }}>{unit}</DropdownItem
            >
        {/each}
    </Dropdown>

    {#if editingName}
        <input
            bind:value={newName}
            class="w-12 h-6 mr-3 text-center rounded bg-red-700 text-gray-200"
            on:blur={saveName}
            on:keydown={(e) => e.key === "Enter" && saveName()}
        />
    {:else}
        <button
            type="button"
            on:click={() => {
                editingName = true;
            }}
            on:keydown={(e) => e.key === "Enter" && (editingName = true)}
            aria-label="Edit quantity"
            class="pl-1"
        >
            {item.name}
        </button>
    {/if}
    {#if item.notes !== ""}
        <Notes notes={item.notes} />
    {/if}
</Li>
