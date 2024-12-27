<script lang="ts">
    import { items, searching, searchResults } from "$lib/store";
    import Fuse from "fuse.js";
    let fuse: Fuse<any>;

    function searchItems(query: string) {
        let results = fuse.search(query);
        $searchResults = results.map((result) => result.item);
    }
    function onInput(e: Event) {
        const target = e.target as HTMLInputElement | null;
        if (target) {
            if (!fuse) {
                fuse = new Fuse($items, {
                    keys: ["name"],
                    threshold: 0.8,
                });
            }
            if (target.value === "") {
                $searching = false;
            } else {
                $searching = true;
            }
            searchItems(target.value);
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
