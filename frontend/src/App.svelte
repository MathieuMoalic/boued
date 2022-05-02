<script>
  import { onMount } from "svelte";

  let api = "https://groceriesapi.matmoa.xyz";
  let newWord = "";
  let items = [];

  let addItem = async () => {
    if (newWord != "") {
      let res = await fetch(api + "/" + newWord, { method: "post" });
      items = await res.json();
      newWord = "";
    }
  };

  let removeItem = async (id) => {
    let res = await fetch(api + "/" + id, { method: "delete" });
    items = await res.json();
  };

  onMount(async () => {
    let res = await fetch(api);
    items = await res.json();
  });
</script>

<main>
  <form type="submit" action="#" on:submit={addItem}>
    <input bind:value={newWord} placeholder=" Add item" />
  </form>
  <div>
    {#each items.reverse() as item}
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
    background-image: url("/background.png");
    background-attachment: fixed;
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
