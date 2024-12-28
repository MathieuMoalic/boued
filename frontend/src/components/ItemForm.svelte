<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { ws, items, modal } from "$lib/store";
    import { possibleCategories, possibleUnits } from "$lib/types";
    import { Button, Modal, Label, Input } from "flowbite-svelte";

    async function submitItem() {
        if ($modal.mode == "edit") {
            try {
                let item = await $ws.updateItem($modal.itemID, $modal.item);
                for (let i = 0; i < $items.length; i++) {
                    if ($items[i].id == item.id) {
                        $items[i] = item;
                        break;
                    }
                }
                $modal.isOpen = false;
                $modal.itemID = -1;
                addAlert("Item updated", "success");
            } catch (error) {
                console.error(
                    `Failed to update the item '${$modal.item.name}':`,
                    error,
                );
                addAlert("Failed to update the item", "error");
            }
            $modal.isOpen = false;
            return;
        } else if ($modal.mode == "add") {
            $modal.mode = "edit";
            try {
                let item = await $ws.createItem($modal.item);
                items.update((items) => [...items, item]);
                $modal.isOpen = false;
                addAlert("Item created", "success");
            } catch (error) {
                console.error(
                    `Failed to create the item '${$modal.item.name}':`,
                    error,
                );
                addAlert("Failed to create the item", "error");
            }
        }
    }
    async function deleteItem() {
        try {
            await $ws.deleteItem($modal.itemID);
            items.update((items) =>
                items.filter((item) => item.id != $modal.itemID),
            );
            $modal.isOpen = false;
            $modal.itemID = -1;
            addAlert("Item deleted", "success");
        } catch (error) {
            console.error(
                `Failed to delete the item '${$modal.item.name}':`,
                error,
            );
            addAlert("Failed to delete the item", "error");
        }
    }
</script>

<Modal bind:open={$modal.isOpen} size="xs" outsideclose>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <div
        class="flex flex-col space-y-6"
        role="dialog"
        on:click={(e) => e.stopPropagation()}
    >
        <h3 class="mb-4 text-xl font-medium text-gray-900">
            {#if $modal.mode == "edit"}
                Edit item
            {:else}
                Add a new item
            {/if}
        </h3>

        <Label class="space-y-2">
            <span>Name</span>
            <Input
                type="text"
                name="name"
                bind:value={$modal.item.name}
                placeholder="Click to enter a name"
                required
            />
        </Label>

        <Label class="space-y-2">
            <span>Quantity (Optional)</span>
            <Input
                type="number"
                name="quantity"
                bind:value={$modal.item.quantity}
                placeholder="Click to enter a quantity"
            />
        </Label>

        <div class="text-gray-900">
            <span>Unit (Optional)</span>
            <div class="m-1 grid grid-cols-4 gap-2">
                {#each possibleUnits as choice}
                    <label
                        class="inline-flex items-center p-1 cursor-pointer {choice ==
                        $modal.item.unit
                            ? 'bg-gray-50'
                            : 'bg-gray-500'}"
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => ($modal.item.unit = choice)}
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
                        $modal.item.category
                            ? 'bg-gray-50'
                            : 'bg-gray-500'}"
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => ($modal.item.category = choice)}
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
                bind:value={$modal.item.notes}
                placeholder="Click to enter notes"
            />
        </Label>

        <Button type="submit" class="w-full" on:click={submitItem}>
            {#if $modal.mode == "edit"}
                Edit item
            {:else}
                Add item
            {/if}
        </Button>
        {#if $modal.mode == "edit"}
            <Button type="submit" class="w-full" on:click={deleteItem}>
                Delete item
            </Button>
        {/if}
    </div>
</Modal>
