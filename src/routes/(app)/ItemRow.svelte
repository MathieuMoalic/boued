<script lang="ts">
    import { goto } from "$app/navigation";
    import Edit from "$icons/Edit.svelte";
    import ToggleActive from "./ToggleActive.svelte";

    export let item: {
        name: string;
        is_active: boolean;
        quantity: number | null;
        unit: string;
        notes: string;
        id: number;
        category_id: number | null;
    };
</script>

<li class="m-0 ml-3 flex justify-between items-center">
    <div
        class="flex items-center truncate overflow-hidden max-w-full {item.is_active
            ? 'text-gray-50'
            : 'text-gray-400'}"
    >
        <ToggleActive {item} />
        {#if item.quantity !== null && item.quantity !== 0}
            <div class="mr-1">{item.quantity}</div>
        {/if}
        {#if item.unit !== "None"}
            <div class="mr-2">{item.unit}</div>
        {/if}
        <span class="overflow-ellipsis">{item.name}</span>
        {#if item.notes !== ""}
            <span class="ml-2 text-gray-500 truncate">| {item.notes}</span>
        {/if}
    </div>
    <button
        on:click={() => goto(`/items/${item.id}`)}
        class="text-primary-500 rounded-md backdrop-blur-sm h-6 w-6"
    >
        <Edit />
    </button>
</li>
