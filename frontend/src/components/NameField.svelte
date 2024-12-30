<script lang="ts">
    import { addAlert } from "$lib/alert";
    import type { ItemRead } from "$lib/Api";
    import { api } from "$lib/store";
    export let item: ItemRead;

    let editing = false;
    let newName = item.name;

    async function saveName() {
        if (newName === item.name) {
            editing = false;
            return;
        }
        api.items
            .update(item.id, { name: newName })
            .then((_) => {
                item.name = newName;
                addAlert("Name updated", "success");
                editing = false;
            })
            .catch((res) => {
                addAlert(res.error.detail || "Failed to update name", "error");
            });
    }
</script>

<div>
    {#if editing}
        <input
            bind:value={newName}
            class="w-12 h-6 mr-3 text-center rounded bg-red-700 text-gray-200"
            on:blur={saveName}
            on:keydown={(e) => e.key === "Enter" && saveName()}
        />
    {:else}
        <button
            type="button"
            on:click={() => (editing = true)}
            class="pl-1"
            aria-label="Edit name"
        >
            {item.name}
        </button>
    {/if}
</div>
