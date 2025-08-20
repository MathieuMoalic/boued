<script lang="ts">
    import { goto } from "$app/navigation";
    import Edit from "$icons/Edit.svelte";
    import ToggleActive from "./ToggleActive.svelte";

    export let category: { id: number | null; name: string };
    export let items: any[];
    export let collapsed: (number | null)[];
    export let toggleCategory: (id: number | null) => void;
</script>

{#if items.some((item) => item.category_id === category.id && item.is_active)}
    <li class="block">
        <button
            on:click={() => toggleCategory(category.id)}
            class="w-full text-left pl-2 flex items-center rounded-md"
        >
            <h5 class="text-lg font-bold text-gray-400">
                {category.name}
            </h5>
            <span class="ml-2">
                {#if collapsed.includes(category.id)}
                    ▲
                {:else}
                    ▼
                {/if}
            </span>
        </button>

        {#each items as item}
            {#if item.category_id === category.id && !collapsed.includes(category.id) && item.is_active}
                <div class="ml-3">
                    <li class="m-0 flex justify-between items-center">
                        <div
                            class="flex items-center truncate overflow-hidden max-w-full {item.is_active
                                ? 'text-gray-50'
                                : 'text-gray-400'}"
                        >
                            <ToggleActive bind:item />
                            {#if item.quantity !== null && item.quantity !== 0}
                                <div class="mr-1">{item.quantity}</div>
                            {/if}
                            {#if item.unit !== "None"}
                                <div class="mr-2">{item.unit}</div>
                            {/if}
                            <span class="overflow-ellipsis">{item.name}</span>
                            {#if item.notes !== ""}
                                <div class="w-2"></div>
                                <span
                                    class="text-gray-500 truncate overflow-hidden text-ellipsis"
                                >
                                    | {item.notes}
                                </span>
                            {/if}
                        </div>
                        <button
                            on:click={() => goto(`/items/${item.id}`)}
                            class="text-primary-500 rounded-md backdrop-blur-sm h-6 w-6"
                        >
                            <Edit />
                        </button>
                    </li>
                </div>
            {/if}
        {/each}
    </li>
{/if}
