<script lang="ts">
  import { onMount } from "svelte";
  import Spinner from "./lib/Spinner.svelte";
  import Input from "./lib/Input.svelte";
  import RemoveButton from "./lib/RemoveButton.svelte";
  import Tab from "./lib/Tab.svelte";
  import { items, category, api, loadingItems } from "./store";

  let itemsCache = localStorage["items"];
  if (itemsCache) $items = JSON.parse(itemsCache);

  onMount(async () => {
    $items = await fetch($api).then((res) => res.json());
    localStorage["items"] = JSON.stringify($items);
  });
</script>

<main>
  <Tab />
  <Input />
  <div class="active">
    {#each $items[$category] as item}
      <div class="item">
        {#if $loadingItems.includes(item.name)}
          <Spinner />
        {:else}
          <RemoveButton {item} />
        {/if}
        <div class="name">
          {item}
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
    color: hsl(208, 49%, 82%);
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
