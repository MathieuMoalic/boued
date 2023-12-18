<script lang="ts">
    import { onMount } from "svelte";
    import { items, category, loadingItems, api, matches } from "../store";
    import RemoveMeiliButton from "./RemoveMeiliButton.svelte";

    let input_field: string = "";

    let onKeyDown = async (event: KeyboardEvent) => {
        if (event.key == "Enter" && input_field != "") {
            addItem(input_field);
        }
        if (event.key == "Escape") {
            $matches = [];
            input_field = "";
        }
    };
    let onInput = async () => {
        if (input_field != "") {
            await search();
        } else {
            $matches = [];
        }
    };
    let search = async () => {
        let path =
            $api +
            "/search/" +
            $category +
            "/" +
            encodeURIComponent(encodeURIComponent(input_field));
        $matches = await fetch(path).then((res) => res.json());
    };
    let addItem = async (item_to_add: string) => {
        item_to_add = encodeURIComponent(encodeURIComponent(item_to_add));
        input_field = "";
        $matches = [];
        item_to_add =
            item_to_add[0].toUpperCase() + item_to_add.slice(1).toLowerCase();
        let found = false;
        // if the item was already added, put it as active and at the top of the list
        $items[$category].every((item: string) => {
            if (item == item_to_add) {
                $items[$category].unshift(item);
                found = true;
                return false;
            }
        });
        // if it's a new item, create it
        if (!found) {
            $items[$category].unshift(item_to_add);
        }
        $loadingItems.push(item_to_add);
        $items = await fetch($api + "/" + $category + "/" + item_to_add, {
            method: "post",
        }).then((res) => res.json());
        localStorage["items"] = JSON.stringify($items);
        $loadingItems = $loadingItems.filter((x) => x != item_to_add);
    };
    let inputElement: HTMLInputElement;
    onMount(() => {
        inputElement.focus();
    });
</script>

<div class="container">
    <div class="input">
        <input
            placeholder="Add item"
            on:keydown={(event) => onKeyDown(event)}
            bind:value={input_field}
            bind:this={inputElement}
            on:input={() => onInput()}
        />
    </div>
    <div class="matches">
        {#each $matches as match}
            <div class="match">
                <RemoveMeiliButton {match} />
                <div
                    class="match_button"
                    on:keydown={() => {}}
                    on:click={() => {
                        addItem(match);
                    }}
                >
                    {match}
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .container {
        position: relative;
    }
    .matches {
        position: absolute;
        width: 80%;
        top: 4rem;
        left: 10%;
        z-index: 1;
    }
    .match {
        display: flex;
    }
    .match_button {
        border-radius: 0.4rem;
        border: 1px solid rgba(169, 72, 61, 255);
        padding: 1rem;
        width: 70%;
        overflow: hidden;
        background-color: rgb(108, 44, 42);
    }
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
