<script lang="ts">
    import { Li } from "flowbite-svelte";

    import type { ItemRead } from "$lib/Api";
    import ToggleActive from "$components/ToggleActive.svelte";
    import EditItem from "./EditItem.svelte";

    export let item: ItemRead;
</script>

<Li icon class="m-0 flex justify-between items-center">
    <div
        class="flex items-center truncate overflow-hidden max-w-full {item.is_active
            ? 'text-gray-50'
            : 'text-gray-400'}"
    >
        <ToggleActive {item} />
        {#if item.quantity !== null}
            <div class="mr-1">
                {item.quantity}
            </div>
        {/if}
        {#if item.unit !== "None"}
            <div class="mr-2">
                {item.unit}
            </div>
        {/if}
        <span class="overflow-ellipsis">
            {item.name}
        </span>
        {#if item.notes !== ""}
            <div class="w-2"></div>
            <span class="text-gray-500 truncate overflow-hidden text-ellipsis">
                | {item.notes}
            </span>
        {/if}
    </div>

    <div class="ml-auto">
        <EditItem {item} />
    </div>
</Li>
