<script lang="ts">
    import { searchTerm } from "$lib/store";

    function onInput(e: Event) {
        const target = e.target as HTMLInputElement | null;
        if (target) {
            searchTerm.set(target.value);
        }
    }
</script>

<div class="m-0 p-2">
    <input
        type="text"
        placeholder="Search items..."
        on:input={onInput}
        class="w-full p-2 bg-red-700 border border-gray-700 rounded
               placeholder-gray-200"
    />
</div>
