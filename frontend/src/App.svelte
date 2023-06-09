<script>
  import { onMount } from "svelte";
  import Spinner from "./Spinner.svelte";
  import Input from "./Input.svelte";
  import RemoveButton from "./RemoveButton.svelte";
  import AddButton from "./AddButton.svelte";
  import Tab from "./Tab.svelte";

  let api = "./api";
  let category = "Groceries";
  let items = [];
  let loadingItems = [];
  let itemsCache = localStorage["items"];
  if (itemsCache) items = JSON.parse(itemsCache);

  onMount(async () => {
    items = await fetch(api).then((res) => res.json());
    localStorage["items"] = JSON.stringify(items);
  });
</script>

<main>
  <Tab bind:category />
  <Input bind:category bind:items bind:loadingItems {api} />
  <div class="active">
    {#each items as item}
      {#if item.active && item.category == category}
        <div class="item">
          {#if loadingItems.includes(item.name)}
            <Spinner />
          {:else}
            <RemoveButton
              bind:category
              bind:items
              bind:loadingItems
              {item}
              {api}
            />
          {/if}
          <div class="name">
            {item.name}{item.emoji}
          </div>
        </div>
      {/if}
    {/each}
  </div>
  <hr />
  <div class="inactive">
    {#each items as item}
      {#if !item.active && item.category == category}
        <div class="item">
          {#if loadingItems.includes(item.name)}
            <Spinner />
          {:else}
            <AddButton
              bind:category
              bind:items
              bind:loadingItems
              {item}
              {api}
            />
          {/if}
          <div class="name">
            <strike>{item.name}</strike>
          </div>
        </div>
      {/if}
    {/each}
  </div>
</main>

<style>
  :global(body) {
    margin: 0px;
    border: 0px;
    padding: 0px;
    color: hsl(208, 49%, 82%);
    font-size: large;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 400;
    padding-bottom: 90%;
    background-image: url("/background.avif");
    background-attachment: fixed;
  }
  hr {
    border: 1px gray solid;
  }
  div.item {
    display: flex;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 25px;
  }
  div.name {
    padding-left: 10px;
  }
  div.inactive {
    color: gray;
  }
</style>
