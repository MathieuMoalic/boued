<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { api, items } from "$lib/store";
    import type { ItemRead } from "$lib/Api";
    import { CloseOutline, PlusOutline } from "flowbite-svelte-icons";
    export let item: ItemRead;

    async function toggleActive() {
        api.items
            .update(item.id, { is_active: !item.is_active })
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
            });
    }
</script>

<div class="mr-1 mt-1.5">
    {#if item.is_active}
        <button on:click={toggleActive}>
            <CloseOutline />
        </button>
    {:else}
        <button on:click={toggleActive}>
            <PlusOutline />
        </button>
    {/if}
</div>
