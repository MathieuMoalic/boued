<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { api } from "$lib/auth";
    import { categories, items } from "$lib/store";

    import {
        BanOutline,
        CaretDownSolid,
        CaretUpSolid,
        CheckOutline,
        CloseOutline,
        EditOutline,
    } from "flowbite-svelte-icons";
    import type { CategoryRead } from "$lib/Api";

    let editCategory = "";
    let editCategoryInput = "";

    export let category: CategoryRead;

    async function editCategoryName(id: number) {
        if (!editCategoryInput) return;

        api.categoryUpdate(id, { name: editCategoryInput })
            .then((_) => {
                editCategory = "";
                editCategoryInput = "";
            })
            .catch((res) => {
                addAlert(
                    res.error.detail || "Failed to edit category",
                    "error",
                );
            });
    }

    async function removeCategory(id: number) {
        if (id === 1) {
            addAlert("Cannot delete this category", "error");
            return;
        }
        api.categoryDelete(id).catch((res) => {
            addAlert(res.error.detail || "Failed to delete category", "error");
        });
    }

    async function moveCategory(id: number, direction: "up" | "down") {
        api.categoryReorder(id, { direction }).catch((res) => {
            addAlert(res.error.detail || "Failed to move category", "error");
        });
    }
</script>

<div class="m-2">
    {#if editCategory !== category.name}
        <div
            class="flex ml-2 bg-primaryBg rounded mr-12 p-2"
            data-id={category.id}
        >
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
            <div class="ml-auto">
                <button
                    on:click={() => {
                        moveCategory(category.id, "up");
                    }}
                >
                    <CaretUpSolid size="md" color="green" />
                </button>
                <button
                    on:click={() => {
                        moveCategory(category.id, "down");
                    }}
                >
                    <CaretDownSolid size="md" color="red" />
                </button>
                <button
                    on:click={() => {
                        editCategory = category.name;
                        editCategoryInput = category.name;
                    }}
                >
                    <EditOutline size="md" color="orange" />
                </button>
            </div>
        </div>
    {:else}
        <div class="flex ml-2 bg-primaryBg rounded mr-12 p-2">
            <input
                type="text"
                class="bg-primaryBg border-inputBorderColor rounded-md primaryText w-full h-7"
                bind:value={editCategoryInput}
                on:keydown={(e) =>
                    e.key === "Enter" && editCategoryName(category.id)}
            />
            <button
                class="w-2/12 flex justify-center items-center"
                on:click={() => {
                    editCategory = "";
                    editCategoryInput = "";
                }}
            >
                <BanOutline color="red" />
            </button>
            <button
                class="w-2/12 flex justify-center items-center"
                on:click={() => {
                    editCategoryName(category.id);
                }}
            >
                <CheckOutline color="green" />
            </button>
        </div>
    {/if}
</div>
