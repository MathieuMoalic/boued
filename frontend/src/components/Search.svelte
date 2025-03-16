<script lang="ts">
    import { searchTerm } from "$lib/store";
</script>

<div class="m-0 p-2">
    <input
        type="text"
        placeholder="Search items..."
        bind:value={$searchTerm}
        class="w-full p-2 bg-primary-900 border-gray-600 rounded
               placeholder-gray-400 border-0 focus:outline-none focus:ring-2 focus:ring-primary-500 text-primary-200"
    />
</div>
