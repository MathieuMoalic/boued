<script lang="ts">
    import { categories, categoryFormOpen } from "$lib/store";
    import { Modal } from "flowbite-svelte";
    import { EditOutline } from "flowbite-svelte-icons";
    import CategoryFormAdd from "./CategoryFormAdd.svelte";
    import CategoryFormLine from "./CategoryFormLine.svelte";
</script>

<button on:click={() => ($categoryFormOpen = true)}>
    <EditOutline size="md" />
</button>

<Modal
    bind:open={$categoryFormOpen}
    size="xs"
    outsideclose
    class="bg-gray-800 text-gray-100 rounded-lg"
>
    <section>
        {#each $categories as category, index (category.order)}
            <CategoryFormLine {category} />
        {/each}
    </section>
    <CategoryFormAdd />
</Modal>

<style>
    /* Example: remove scrolling so drag works on touch devices more cleanly */
    section {
        overflow: visible;
    }
</style>
