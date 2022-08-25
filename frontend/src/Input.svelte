<script>
    export let items;
    export let api;

    let addItem = async (input) => {
        let word = input.value;
        if (word != "") {
            items = [{ name: word, id: -1 }, ...items];
            input.value = "";
            items = await fetch(api + "/" + word, { method: "post" }).then(
                (res) => res.json()
            );
            // console.log("saving items in cache ...");
            // localStorage["items"] = JSON.stringify(items);
            // console.log("saved.");
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
