<script>
  import { onMount } from "svelte";
  import Spinner from "./Spinner.svelte";
  import Input from "./Input.svelte";
  import RemoveButton from "./RemoveButton.svelte";

  let api = "./api";
  let items = [];
  let itemsCache = localStorage["items"];
  if (itemsCache) items = JSON.parse(itemsCache);

  onMount(async () => {
    items = await fetch(api).then((res) => res.json());
    localStorage["items"] = JSON.stringify(items);
  });
</script>

<main>
  <Input bind:items {api} />
  <div>
    {#each items as { name, id }}
      <div class="item">
        {#if id == -1}
          <Spinner />
        {:else}
          <RemoveButton bind:items {id} {api} />
        {/if}
        <div class="name">
          {name}
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
  div.item {
    display: flex;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 25px;
  }
  div.name {
    padding-left: 10px;
  }
</style>
