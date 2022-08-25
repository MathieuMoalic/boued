<script>
    export let items;
    export let id;
    export let api;
    let removeItem = async (id) => {
        for (let i = 0; i < items.length; i++) {
            if (items[i].id == id) {
                items[i].id = -1;
            }
        }
        items = await fetch(api + "/" + id, { method: "delete" }).then((r) =>
            r.json()
        );
        localStorage["items"] = JSON.stringify(items);
    };
</script>

<button on:click={() => removeItem(id)}>x</button>

<style>
    button {
        font-size: large;
        background: none;
        border: 1px solid rgba(128, 128, 128, 0.432);
        border-radius: 4px;
        font-weight: 600;
    }
</style>
