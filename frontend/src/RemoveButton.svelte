<script>
    export let items;
    export let loadingItems;
    export let item;
    export let api;

    let removeItem = async () => {
        loadingItems.push(item.name)
        loadingItems = loadingItems
        items = await fetch(api + "/" + item.name, { method: "delete" }).then((r) =>
            r.json()
        );
        localStorage["items"] = JSON.stringify(items);
        loadingItems = loadingItems.filter(x => x != item.name)
    };
</script>

<button on:click={() => removeItem()}>x</button>

<style>
    button {
        font-size: large;
        background: none;
        border: 1px solid rgba(128, 128, 128, 0.432);
        border-radius: 4px;
        font-weight: 600;
    }
</style>
