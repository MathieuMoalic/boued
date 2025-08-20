<script lang="ts">
    import Edit from "$icons/Edit.svelte";
    import type { PageData } from "./$types";
    import Plus from "$icons/Plus.svelte";
    import CaretDownSolid from "$icons/CaretDownSolid.svelte";
    import CaretUpSolid from "$icons/CaretUpSolid.svelte";
    import Close from "$icons/Close.svelte";
    import Check from "$icons/Check.svelte";
    import Ban from "$icons/Ban.svelte";
    import { enhance } from "$app/forms";
    import type { SubmitFunction } from "@sveltejs/kit";
    import { addAlert } from "$lib/client/alert";
    import Undo from "$icons/Undo.svelte";
    export let data: PageData;
    let categories = data.categories;
    let editCategory = "AA";
    let editCategoryInput = "AA";
    let newCategoryInput = "";

    const handleEnhance: SubmitFunction = () => {
        return async ({ result }) => {
            switch (result.type) {
                case "success": {
                    if (result.data && result.data.categories) {
                        categories = result.data.categories;
                    }
                    editCategory = "";
                    editCategoryInput = "";
                    newCategoryInput = "";
                    break;
                }
                case "failure": {
                    addAlert(result.data?.error ?? "Unknown error", "error");
                    break;
                }
            }
        };
    };
</script>

<form
    method="POST"
    use:enhance={handleEnhance}
    class="flex items-center space-x-2 mb-4 w-full"
>
    <section class="p-4 w-full">
        <h1 class="text-2xl text-primary-200 font-bold mb-4">Categories</h1>
        {#each categories as category (category.id)}
            <div
                class="flex items-center bg-primary-900 rounded p-2 mb-4 h-10 w-full"
            >
                {#if editCategory !== category.name}
                    <div class="flex items-center w-full">
                        <button
                            class="text-red-500 h-6 w-6"
                            formaction="?/delete"
                            type="submit"
                            name="id"
                            value={category.id}
                        >
                            <Close />
                        </button>
                        <div class="ml-3 text-primary-200 text-lg">
                            {category.name}
                        </div>
                        <div class="ml-auto flex items-center space-x-2">
                            <button>
                                <CaretUpSolid
                                    className="w-6 h-6 text-green-600"
                                />
                            </button>
                            <button>
                                <CaretDownSolid
                                    className="w-6 h-6 text-red-500"
                                />
                            </button>
                            <button
                                on:click={() => {
                                    editCategory = category.name;
                                    editCategoryInput = category.name;
                                }}
                                class="text-orange-500 h-5 w-5"
                            >
                                <Edit />
                            </button>
                        </div>
                    </div>
                {:else}
                    <input
                        type="text"
                        class="bg-primary-700 text-primary-200 border border-primary-700 rounded-md w-full p-2 h-6"
                        bind:value={editCategoryInput}
                        name="new-name"
                    />
                    <button
                        class="ml-2 p-2"
                        on:click={() => {
                            editCategory = "";
                            editCategoryInput = "";
                        }}
                        type="button"
                    >
                        <Undo className="w-6 h-6 text-red-500" />
                    </button>
                    <button
                        class="ml-2 p-2"
                        formaction="?/rename"
                        type="submit"
                        name="id"
                        value={category.id}
                    >
                        <Check className="w-6 h-6 text-green-500" />
                    </button>
                {/if}
            </div>
        {/each}
        <div class="flex items-center space-x-2 mb-4 w-full">
            <input
                placeholder="Add category"
                name="input-name"
                bind:value={newCategoryInput}
                class="bg-primary-800 text-primary-200 placeholder-gray-400 border border-primary-700 rounded-md p-2 w-full"
                on:keydown={(e) => e.key === "Enter"}
            />
            <button
                class="p-2 bg-primary-700 rounded-md text-primary-200 hover:bg-primary-600 transition-colors w-10 h-10 flex items-center justify-center"
                type="submit"
                formaction="?/create"
            >
                <Plus className="w-6 h-6" />
            </button>
        </div>
    </section>
</form>
