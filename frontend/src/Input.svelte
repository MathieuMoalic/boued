<script>
    export let items;
    export let loadingItems;
    export let api;

    let addItem = async (input) => {
        let item = input.value;
        if (item != "") {
            item = item[0].toUpperCase() + item.slice(1).toLowerCase();
            // if item already in active list
            if (items['active'].includes(item)) {
                // remove it from the list
                items = {'active':items['active'].filter((x) => x != item), 'inactive':items['inactive']};
                // if item already in inactive list
            } else if (items['inactive'].includes(item)) {
                items = {'active':items['active'],'inactive':items['inactive'].filter((x) => x != item) };
            }
            // add it at the beginning
            items['active'].unshift(item)
            items = {'active':items['active'], 'inactive':items['inactive']};
            loadingItems.push(item);
            loadingItems = loadingItems
            input.value = "";
            items = await fetch(api + "/" + item, { method: "post" }).then(
                (res) => res.json()
            );
            localStorage["items"] = JSON.stringify(items);
            loadingItems = loadingItems.filter((x) => x != item);
        }
    };
</script>

<div class="input">
    <input
        placeholder="Add item"
        on:keydown={(event) => event.key === "Enter" && addItem(event.target)}
    />
</div>

<style>
    div.input {
        display: flex;
        padding: 15px;
        border: 0px;
    }
    input {
        flex-grow: 1;
        background-color: rgb(131, 35, 0);
        border: 0px;
        border-radius: 5px;
        padding: 5px;
        padding-left: 25px;

        font-size: larger;
        color: aliceblue;
        font-weight: 400;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
