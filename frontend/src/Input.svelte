<script>
    export let items;
    export let loadingItems;
    export let api;

    let addItem = async (input) => {
        let item_name = input.value;
        if (item_name != "") {
            item_name =
                item_name[0].toUpperCase() + item_name.slice(1).toLowerCase();
            let found = false;
            // if the item was already added, put it as active and at the top of the list
            items.forEach((item) => {
                if (item.name == item_name) {
                    items.unshift(item);
                    items[0].active = true;
                    found = true;
                }
            });
            // if it's a new item, create it
            if (!found) {
                items.unshift({
                    name: item_name,
                    active: true,
                    category: "",
                    emoji: "",
                });
            }
            items = items;
            loadingItems.push(item_name);
            loadingItems = loadingItems;
            input.value = "";
            items = await fetch(api + "/" + item_name, { method: "post" }).then(
                (res) => res.json()
            );
            localStorage["items"] = JSON.stringify(items);
            loadingItems = loadingItems.filter((x) => x != item_name);
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
