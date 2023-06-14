<script>
    import { category, api, loadingItems, items, matches } from "../store";
    export let match;

    let removeItem = async () => {
        match = encodeURIComponent(match);
        $loadingItems.push(match);
        $items = await fetch(
            $api + "/meili/" + $category + "/" + encodeURIComponent(match),
            {
                method: "delete",
            }
        ).then((r) => r.json());
        $matches.splice($matches.indexOf(match), 1);
        $matches = $matches;
    };
</script>

<button on:click={() => removeItem()}>x</button>

<style>
    button {
        width: 3rem;
        left: 0%;
        background-color: rgb(108, 44, 42);
        border: 1px solid rgba(169, 72, 61, 255);
        padding: 1rem;
        font-size: large;
        border-radius: 4px;
        font-weight: 600;
        color: hsl(208, 34%, 70%);
    }
</style>
