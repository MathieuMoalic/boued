<script lang="ts">
    import { units } from "$lib/client/units";
    import Minus from "$icons/Minus.svelte";
    import Plus from "$icons/Plus.svelte";
    export let item: {
        name: string;
        quantity: number;
        unit: string;
        category_id: number | null;
        notes: string;
    } = {
        name: "Item not found",
        quantity: 0,
        unit: "pcs",
        category_id: null,
        notes: "",
    };
    export let categories: { id: number; name: string }[] = [];
    export let mode: "create" | "edit" = "create";
</script>

<main class="flex flex-col space-y-4 p-4 text-primary-200">
    <label class="space-y-1 text-sm text-primary-200">
        <span>Name</span>
        <input
            type="text"
            name="name"
            bind:value={item.name}
            class="w-full bg-primary-700 border border-primary-600 rounded text-primary-200 p-2 placeholder-gray-400 focus:outline-none focus:ring focus:border-primary-500"
            placeholder="Enter a name"
            required
        />
    </label>

    <label class="space-y-1 text-sm text-primary-200">
        <span>Quantity</span>
        <div class="flex items-center space-x-2">
            <button
                on:click={() =>
                    (item.quantity = Math.max(0, (item.quantity ?? 0) - 1))}
                class="flex items-center justify-center px-3 py-1 bg-primary-700 hover:bg-primary-600 text-primary-200 rounded w-14 h-10"
            >
                <Minus />
            </button>
            <input
                name="quantity"
                bind:value={item.quantity}
                class="flex-1 min-w-0 text-center bg-primary-700 border border-primary-600 rounded text-primary-200 p-2 placeholder-gray-400 focus:outline-none"
                placeholder="Enter quantity"
            />
            <button
                on:click={() => (item.quantity = (item.quantity ?? 0) + 1)}
                class="flex items-center justify-center px-3 py-1 bg-primary-800 hover:bg-primary-700 text-primary-200 rounded w-14 h-10"
            >
                <Plus />
            </button>
        </div>
    </label>

    <div>
        <span class="block text-sm font-medium text-primary-200">Unit</span>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-1 mt-1">
            {#each units as unit}
                <label
                    class={`inline-flex items-center justify-center p-1 cursor-pointer rounded text-primary-200 
					${unit == item.unit ? "bg-primary-600" : "bg-primary-800 hover:bg-primary-700"}`}
                >
                    <input
                        type="radio"
                        value={unit}
                        on:click={() => (item.unit = unit)}
                        name="unit"
                        class="hidden"
                    />
                    {unit}
                </label>
            {/each}
        </div>
    </div>

    <div>
        <span class="block text-sm font-medium text-primary-200">Category</span>
        <div class="grid grid-cols-3 gap-1 mt-1">
            {#each categories as category}
                <label
                    class={`inline-flex items-center justify-center p-1 cursor-pointer rounded text-primary-200 max-w-[120px] truncate
						${category.id == item.category_id ? "bg-primary-600" : "bg-primary-800 hover:bg-primary-700"}`}
                    title={category.name}
                >
                    <input
                        type="radio"
                        value={category.id}
                        on:click={() => (item.category_id = category.id)}
                        name="category"
                        class="hidden"
                    />
                    <span class="truncate w-full text-center"
                        >{category.name}</span
                    >
                </label>
            {/each}
        </div>
    </div>

    <label class="space-y-1 text-sm text-primary-200">
        <span>Notes</span>
        <input
            type="text"
            name="notes"
            bind:value={item.notes}
            class="w-full bg-primary-700 border border-primary-600 rounded text-primary-200 p-2 placeholder-gray-400 focus:outline-none"
            placeholder="Enter notes"
        />
    </label>

    {#if mode === "edit"}
        <button
            type="submit"
            class="w-full py-2 bg-primary-600 hover:bg-primary-500 text-primary-200 font-semibold rounded"
        >
            Save
        </button>

        <button
            type="button"
            class="w-full py-2 bg-red-700 hover:bg-red-600 text-primary-200 font-semibold rounded"
        >
            Delete
        </button>
    {:else}
        <button
            type="submit"
            class="w-full py-2 bg-primary-600 hover:bg-primary-500 text-primary-200 font-semibold rounded"
        >
            Add
        </button>
    {/if}
</main>
