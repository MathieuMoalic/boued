<script lang="ts">
    import { onMount } from "svelte";
    import { categories, items } from "$lib/store";
    import { List } from "flowbite-svelte";
    import ItemComp from "$components/Item.svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";

    let collapsed: number[] = [];

    // Load collapsed state from localStorage on mount
    onMount(() => {
        const storedCollapsed = localStorage.getItem("collapsedCategories");
        if (storedCollapsed) {
            collapsed = JSON.parse(storedCollapsed);
        }
    });

    function toggleCategory(catId: number) {
        if (collapsed.includes(catId)) {
            collapsed = collapsed.filter((id) => id !== catId);
        } else {
            collapsed = [...collapsed, catId];
        }
        localStorage.setItem("collapsedCategories", JSON.stringify(collapsed));
    }
</script>

<main>
    <List tag="ul" class="text-gray-200">
        {#each $categories as category}
            {#if $items.some((item) => item.is_active && item.category_id === category.id)}
                <li class="block">
                    <button
                        on:click={() => toggleCategory(category.id)}
                        class="w-full text-left pl-2 flex items-center rounded-md"
                    >
                        <h5 class="text-lg font-bold text-gray-400">
                            {category.name}
                        </h5>
                        {#if collapsed.includes(category.id)}
                            <ChevronDownOutline
                                class="h-6 w-6 transform rotate-180"
                            />
                        {:else}
                            <ChevronDownOutline class="h-6 w-6" />
                        {/if}
                    </button>

                    {#each $items as item}
                        {#if item.is_active && item.category_id === category.id && !collapsed.includes(category.id)}
                            <div class="ml-3">
                                <ItemComp {item} />
                            </div>
                        {/if}
                    {/each}
                </li>
            {/if}
        {/each}
    </List>
</main>
