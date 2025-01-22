<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { api } from "$lib/auth";
    import { categories } from "$lib/store";
    import { Input } from "flowbite-svelte";
    import { PlusOutline } from "flowbite-svelte-icons";

    let inputValue = "";
    async function addCategory() {
        if (!inputValue) return;

        api.categoryCreate({ name: inputValue })
            .then((_) => {
                inputValue = "";
            })
            .catch((res) => {
                addAlert(
                    res.error.detail || "Failed to create category",
                    "error",
                );
            });
    }
</script>

<div class="flex ml-4 mr-7">
    <Input
        placeholder="Add category"
        bind:value={inputValue}
        class="bg-primaryBg border-inputBorderColor rounded-md text-primaryText`"
        on:keydown={(e) => e.key === "Enter" && addCategory()}
    />
    <button on:click={addCategory}>
        <PlusOutline size="md" class="ml-2 self-center" />
    </button>
</div>
