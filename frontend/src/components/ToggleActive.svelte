<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { items } from "$lib/store";

    import type { ItemRead } from "$lib/Api";
    import { CloseOutline, PlusOutline } from "flowbite-svelte-icons";
    import { api } from "$lib/auth";
    import { Spinner } from "flowbite-svelte";
    export let item: ItemRead;
    let loading = false;

    async function toggleActive() {
        loading = true;
        api.itemUpdate(item.id, { is_active: !item.is_active })
            .then((_) => {
                item.is_active = !item.is_active;
                for (let i = 0; i < $items.length; i++) {
                    if ($items[i].id === item.id) {
                        $items[i].is_active = item.is_active;
                    }
                }
            })
            .catch((res) => {
                addAlert(
                    res.error.detail || "Failed to toggle the active status",
                    "error",
                );
            })
            .finally(() => {
                loading = false;
            });
    }
</script>

{#if loading}
    <Spinner class="h-6" />
{:else if item.is_active}
    <div class="mr-3 mt-1.5">
        <button on:click={toggleActive}>
            <CloseOutline />
        </button>
    </div>
{:else}
    <div class="mr-3 mt-1.5">
        <button on:click={toggleActive}>
            <PlusOutline />
        </button>
    </div>
{/if}
