<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { items, itemForm, api, categories } from "$lib/store";
    import { possibleUnits } from "$lib/types";
    import { Button, Modal, Label, Input } from "flowbite-svelte";
    import CategoryForm from "./CategoryForm.svelte";

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
        if ($itemForm.mode == "edit") {
            let res = await api.items.update($itemForm.itemID, $itemForm.item);
            if (!res.ok) {
                addAlert(
                    `Failed to update the item '${$itemForm.item.name}':${res.error}`,
                    "error",
                );
                return;
            } else {
                let item = res.data;
                for (let i = 0; i < $items.length; i++) {
                    if ($items[i].id == item.id) {
                        $items[i] = item;
                        break;
                    }
                }
                $itemForm.isOpen = false;
                $itemForm.itemID = -1;
                addAlert("Item updated", "success");
            }
            return;
        } else if ($itemForm.mode == "add") {
            if (!$itemForm.item.name) {
                addAlert("Name is required", "error");
                return;
            }
            if (!$itemForm.item.category_id) {
                addAlert("Category is required", "error");
                return;
            }
            let res = await api.items.create({
                name: $itemForm.item.name,
                notes: $itemForm.item.notes,
                quantity: $itemForm.item.quantity,
                unit: $itemForm.item.unit,
                category_id: $itemForm.item.category_id,
            });
            if (!res.ok) {
                addAlert(
                    `Failed to update the item '${$itemForm.item.name}':${res.error}`,
                    "error",
                );
                return;
            } else {
                items.update((items) => [...items, res.data]);
                $itemForm.isOpen = false;
                addAlert("Item created", "success");
            }
        } else {
            addAlert(`Invalid mode: ${$itemForm.mode}`, "error");
        }
    }

    async function deleteItem() {
        let res = await api.items.delete($itemForm.itemID);
        if (!res.ok) {
            addAlert(
                `Failed to delete the item '${$itemForm.item.name}':${res.error}`,
                "error",
            );
            return;
        } else {
            items.update((items) =>
                items.filter((item) => item.id != $itemForm.itemID),
            );
            $itemForm.isOpen = false;
            $itemForm.itemID = -1;
            addAlert(`"${$itemForm.item.name}" deleted`, "success");
        }
    }
</script>

<Modal
    bind:open={$itemForm.isOpen}
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
            {#if $itemForm.mode == "edit"}
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
                bind:value={$itemForm.item.name}
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
                bind:value={$itemForm.item.quantity}
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
                        ${choice == $itemForm.item.unit ? primaryColor : inputBgColor}
                        ${choice == $itemForm.item.unit ? "text-gray-100" : textColor}
                        hover:${primaryHoverColor}`}
                    >
                        <input
                            type="radio"
                            value={choice}
                            on:click={() => ($itemForm.item.unit = choice)}
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
                {#each $categories as category}
                    <label
                        class={`inline-flex items-center justify-center p-1 cursor-pointer rounded-md
                        ${category.id == $itemForm.item.category_id ? primaryColor : inputBgColor}
                        ${category.id == $itemForm.item.category_id ? "text-gray-100" : textColor}
                        hover:${primaryHoverColor}`}
                    >
                        <input
                            type="radio"
                            value={category}
                            on:click={() =>
                                ($itemForm.item.category_id = category.id)}
                            name="category"
                            class="hidden"
                        />
                        {category.name}
                    </label>
                {/each}
                <label
                    class={`inline-flex items-center justify-center p-1 cursor-pointer rounded-md ${inputBgColor}
                        text-gray-100 hover:${primaryHoverColor}`}
                >
                    <CategoryForm />
                </label>
            </div>
        </div>

        <Label class={`space-y-1 text-sm ${textColor}`}>
            <span>Notes</span>
            <Input
                type="text"
                name="notes"
                bind:value={$itemForm.item.notes}
                class={`${inputBgColor} ${inputBorderColor} rounded-md ${primaryRingColor} ${textColor}`}
                placeholder="Enter notes"
            />
        </Label>

        <Button
            type="submit"
            class={`w-full py-2 ${primaryColor} hover:${primaryHoverColor} text-gray-100 font-semibold rounded-md`}
            on:click={submitItem}
        >
            {#if $itemForm.mode == "edit"}
                Save
            {:else}
                Add Item
            {/if}
        </Button>

        {#if $itemForm.mode == "edit"}
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
