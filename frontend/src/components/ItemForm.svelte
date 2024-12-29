<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { ws, items, modal } from "$lib/store";
    import { possibleCategories, possibleUnits } from "$lib/types";
    import { Button, Modal, Label, Input } from "flowbite-svelte";

    let textColor = "text-gray-300";
    let backgroundColor = "bg-gray-900";
    let inputBgColor = "bg-gray-800";
    let inputBorderColor = "border-gray-700";
    let primaryColor = "bg-primary-600";
    let primaryHoverColor = "bg-primary-700";
    let primaryRingColor = "focus:ring-primary-500";
    let dangerColor = "bg-red-600";
    let dangerHoverColor = "bg-red-700";

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

<Modal
    bind:open={$modal.isOpen}
    size="xs"
    outsideclose
    class={`${backgroundColor} text-gray-100 rounded-lg`}
>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <div
        class={`flex flex-col space-y-4 p-3 rounded-lg shadow-lg ${backgroundColor} ${textColor}`}
        role="dialog"
        on:click={(e) => e.stopPropagation()}
    >
        <h3 class="text-lg font-semibold text-gray-100">
            {#if $modal.mode == "edit"}
                Edit Item
            {:else}
                Add a New Item
            {/if}
        </h3>

        <Label class={`space-y-1 text-sm ${textColor}`}>
            <span>Name</span>
            <Input
                type="text"
                name="name"
                bind:value={$modal.item.name}
                class={`${inputBgColor} ${inputBorderColor} rounded-md ${primaryRingColor} ${textColor}`}
                placeholder="Enter a name"
                required
            />
        </Label>

        <Label class={`space-y-1 text-sm ${textColor}`}>
            <span>Quantity</span>
            <Input
                type="number"
                name="quantity"
                bind:value={$modal.item.quantity}
                class={`${inputBgColor} ${inputBorderColor} rounded-md ${primaryRingColor} ${textColor}`}
                placeholder="Enter quantity"
            />
        </Label>

        <div>
            <span class={`block text-sm font-medium ${textColor}`}>Unit</span>
            <div class="m-1 grid grid-cols-4 gap-1">
                {#each possibleUnits as choice}
                    <label
                        class={`inline-flex items-center justify-center p-1 cursor-pointer rounded-md
                        ${choice == $modal.item.unit ? primaryColor : inputBgColor}
                        ${choice == $modal.item.unit ? "text-gray-100" : textColor}
                        hover:${primaryHoverColor}`}
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => ($modal.item.unit = choice)}
                            name="unit"
                            class="hidden"
                        />
                        {choice}
                    </label>
                {/each}
            </div>
        </div>

        <div>
            <span class={`block text-sm font-medium ${textColor}`}
                >Category</span
            >
            <div class="m-1 grid grid-cols-3 gap-1">
                {#each possibleCategories as choice}
                    <label
                        class={`inline-flex items-center justify-center p-1 cursor-pointer rounded-md
                        ${choice == $modal.item.category ? primaryColor : inputBgColor}
                        ${choice == $modal.item.category ? "text-gray-100" : textColor}
                        hover:${primaryHoverColor}`}
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => ($modal.item.category = choice)}
                            name="category"
                            class="hidden"
                        />
                        {choice}
                    </label>
                {/each}
            </div>
        </div>

        <Label class={`space-y-1 text-sm ${textColor}`}>
            <span>Notes</span>
            <Input
                type="text"
                name="notes"
                bind:value={$modal.item.notes}
                class={`${inputBgColor} ${inputBorderColor} rounded-md ${primaryRingColor} ${textColor}`}
                placeholder="Enter notes"
            />
        </Label>

        <Button
            type="submit"
            class={`w-full py-2 ${primaryColor} hover:${primaryHoverColor} text-gray-100 font-semibold rounded-md`}
            on:click={submitItem}
        >
            {#if $modal.mode == "edit"}
                Save
            {:else}
                Add Item
            {/if}
        </Button>

        {#if $modal.mode == "edit"}
            <Button
                type="button"
                class={`w-full py-2 ${dangerColor} hover:${dangerHoverColor} text-gray-100 font-semibold rounded-md`}
                on:click={deleteItem}
            >
                Delete
            </Button>
        {/if}
    </div>
</Modal>
