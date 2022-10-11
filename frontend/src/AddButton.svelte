<script>
    export let items;
    export let item;
    export let api;
    export let loadingItems;

    let addItem = async () => {
        loadingItems.push(item.name)
        loadingItems = loadingItems
        items = await fetch(api + "/" + item.name, { method: "post" }).then((r) =>
            r.json()
        );
        localStorage["items"] = JSON.stringify(items);
        loadingItems = loadingItems.filter(x => x != item.name)
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
