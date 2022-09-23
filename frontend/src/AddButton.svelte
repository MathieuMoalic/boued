<script>
    export let items;
    export let item;
    export let api;
    export let loadingItems;

    let addItem = async () => {
        loadingItems.push(item)
        loadingItems = loadingItems
        items = await fetch(api + "/" + item, { method: "post" }).then((r) =>
            r.json()
        );
        localStorage["items"] = JSON.stringify(items);
        loadingItems = loadingItems.filter(x => x != item)
    };
</script>

<button on:click={() => addItem()}>+</button>

<style>
    button {
        font-size: large;
        background: none;
        border: 1px solid rgba(128, 128, 128, 0.432);
        border-radius: 4px;
        font-weight: 600;
    }
</style>
