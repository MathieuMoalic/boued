<script lang="ts">
    import { ws, items } from "$lib/store";
    import { possibleCategories, possibleUnits } from "$lib/types";
    import { SpeedDial, Button, Modal, Label, Input } from "flowbite-svelte";
    let open = false;
    let name = "";
    let quantity: number | undefined;
    let category = possibleCategories[0];
    let unit = possibleUnits[0];
    let notes = "";
    let submitItem = async () => {
        try {
            let item = await $ws.createItem({
                name,
                quantity,
                category,
                unit,
                notes,
            });
            items.update((items) => [...items, item]);
        } catch (error) {
            console.error(`Failed to create the item '${name}':`, error);
        }
        open = false;
    };
</script>

<SpeedDial trigger="click" bind:open></SpeedDial>

<Modal bind:open size="xs">
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <div
        class="flex flex-col space-y-6"
        role="dialog"
        on:click={(e) => e.stopPropagation()}
    >
        <h3 class="mb-4 text-xl font-medium text-gray-900">Add a new item</h3>

        <Label class="space-y-2">
            <span>Name</span>
            <Input
                type="text"
                name="name"
                bind:value={name}
                placeholder="Click to enter a name"
                required
            />
        </Label>

        <Label class="space-y-2">
            <span>Quantity (Optional)</span>
            <Input
                type="number"
                name="quantity"
                bind:value={quantity}
                placeholder="Click to enter a quantity"
            />
        </Label>

        <div class="text-gray-900">
            <span>Unit (Optional)</span>
            <div class="m-1 grid grid-cols-4 gap-2">
                {#each possibleUnits as choice}
                    <label
                        class="inline-flex items-center p-1 cursor-pointer {choice ==
                        unit
                            ? 'bg-gray-50'
                            : 'bg-gray-500'}"
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => (unit = choice)}
                            name="unit"
                            class="hidden"
                        />
                        <span class="text-gray-700">{choice}</span>
                    </label>
                {/each}
            </div>
        </div>

        <div class="text-gray-900">
            <span>Category (Optional)</span>
            <div class="m-1 grid grid-cols-3 gap-2">
                {#each possibleCategories as choice}
                    <label
                        class="inline-flex items-center p-1 cursor-pointer {choice ==
                        category
                            ? 'bg-gray-50'
                            : 'bg-gray-500'}"
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => (category = choice)}
                            name="category"
                            class="hidden"
                        />
                        <span class="text-gray-700">{choice}</span>
                    </label>
                {/each}
            </div>
        </div>

        <Label class="space-y-2">
            <span>Notes (Optional)</span>
            <Input
                type="text"
                name="notes"
                bind:value={notes}
                placeholder="Click to enter notes"
            />
        </Label>

        <Button type="submit" class="w-full" on:click={submitItem}
            >Add item</Button
        >
    </div>
</Modal>
