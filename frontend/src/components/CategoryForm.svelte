<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { api, categories, categoryFormOpen, items } from "$lib/store";

    import { Input, Modal } from "flowbite-svelte";
    import {
        CloseOutline,
        EditOutline,
        PlusOutline,
    } from "flowbite-svelte-icons";

    let inputValue = "";
    async function addCategory() {
        if (!inputValue) return;

        api.categories
            .createCategory({ name: inputValue })
            .then((res) => {
                categories.update((cats) => [...cats, res.data]);
                inputValue = "";
                addAlert("Category created", "success");
            })
            .catch((res) => {
                addAlert(
                    res.error.detail || "Failed to create category",
                    "error",
                );
            });
    }

    async function removeCategory(id: number) {
        if (id === 1) {
            addAlert("Cannot delete this category", "error");
            return;
        }
        api.categories
            .deleteCategory(id)
            .then((_) => {
                categories.update((cats) =>
                    cats.filter((cat) => cat.id !== id),
                );
                addAlert("Category deleted", "success");
                // change the category of all the items that had this category to the default category using a for loop
                for (let i = 0; i < $items.length; i++) {
                    if ($items[i].category_id === id) {
                        $items[i].category_id = 1;
                    }
                }
            })
            .catch((res) => {
                addAlert(
                    res.error.detail || "Failed to delete category",
                    "error",
                );
            });
    }
</script>

<button on:click={() => ($categoryFormOpen = true)}>
    <EditOutline size="md" />
</button>

<Modal
    bind:open={$categoryFormOpen}
    size="xs"
    outsideclose
    class="bg-secondaryBg text-gray-100 rounded-lg"
>
    {#each $categories as category}
        <div class="flex ml-2">
            <button
                on:click={() => {
                    removeCategory(category.id);
                }}
            >
                <CloseOutline color="red" />
            </button>
            <div class="ml-3">
                {category.name}
            </div>
        </div>
    {/each}
    <div class="flex">
        <Input
            placeholder="Add category"
            bind:value={inputValue}
            class="bg-primaryBg border-inputBorderColor rounded-md primaryText`"
            on:keydown={(e) => e.key === "Enter" && addCategory()}
        />
        <button on:click={addCategory}>
            <PlusOutline size="md" class="ml-2 self-center" />
        </button>
    </div>
</Modal>
