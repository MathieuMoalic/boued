<script>
    import { items, category, api, loadingItems } from "./store";
    export let item;
    let removeItem = async () => {
        item = encodeURIComponent(item);
        $loadingItems.push(item);
        $items = await fetch(
            $api + "/" + $category + "/" + encodeURIComponent(item),
            {
                method: "delete",
            },
        ).then((r) => r.json());
        localStorage["items"] = JSON.stringify($items);
        $loadingItems = $loadingItems.filter((x) => x != item);
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
        color: hsl(208, 34%, 70%);
    }
</style>
