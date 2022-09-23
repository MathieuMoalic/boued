<script>
  import { onMount } from "svelte";
  import Spinner from "./Spinner.svelte";
  import Input from "./Input.svelte";
  import RemoveButton from "./RemoveButton.svelte";
  import AddButton from "./AddButton.svelte";

  let api = "./api";
  let items = {
    'active': [],
    'inactive': [],
  }
  let loadingItems = [];
  let itemsCache = localStorage["items"];
  if (itemsCache) items = JSON.parse(itemsCache);

  onMount(async () => {
    items = await fetch(api).then((res) => res.json());
    localStorage["items"] = JSON.stringify(items);
  });
</script>

<main>
  <Input bind:items bind:loadingItems {api} />
  <div class="active">
    {#each items.active as item}
      <div class="item">
        {#if loadingItems.includes(item)}
          <Spinner />
        {:else}
          <RemoveButton bind:items bind:loadingItems {item} {api} />
        {/if}
        <div class="name">
          {item}
        </div>
      </div>
    {/each}
  </div>
  <hr />
  <div class="inactive">
    {#each items.inactive as item}
      <div class="item">
        {#if loadingItems.includes(item)}
          <Spinner />
        {:else}
          <AddButton bind:items bind:loadingItems {item} {api} />
        {/if}
        <div class="name">
        <strike>{item}</strike>
        </div>
      </div>
    {/each}
  </div>
</main>

<style>
  :global(body) {
    margin: 0px;
    border: 0px;
    padding: 0px;
    color: aliceblue;
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
  div.active {
    color: black;
  }
  div.inactive {
    color: gray;
  }
</style>
