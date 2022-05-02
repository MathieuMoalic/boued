<script lang="ts">
  import { onMount } from "svelte";
  import { getItems, deleteItem, postItem } from "./Crud";
  let newWord = "";

  let addItem = async () => {
    if (newWord != "") {
      items = await postItem(newWord);
      newWord = "";
    }
  };

  let removeItem = async (id: number) => {
    items = await deleteItem(id);
  };

  let items = [];
  onMount(async () => {
    items = await getItems();
  });
</script>

<main>
  <form type="submit" action="#" on:submit={addItem}>
    <input bind:value={newWord} placeholder=" Add item" />
  </form>
  <div>
    {#each items as item}
      <div class="item">
        <button
          type="submit"
          on:click|preventDefault={() => {
            removeItem(item.id);
          }}>x</button
        >
        <div class="name">
          {item.name}
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
    padding-bottom: 100%;
    /* background-image: url("background.png"); */
  }
  form {
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
    padding-left: 15px;

    font-size: larger;
    color: aliceblue;
    font-weight: 400;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }
  div.item {
    display: flex;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 25px;
  }
  button {
    font-size: large;
    background: none;
    border: 1px solid rgba(128, 128, 128, 0.432);
    border-radius: 4px;
    font-weight: 600;
  }
  div.name {
    padding-left: 10px;
  }
</style>
