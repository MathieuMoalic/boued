<script lang="ts">
	import { ws } from "$lib/store";
	import type { Item } from "$lib/types";
	import { onMount } from "svelte";
	import SomeItems from "$lib/SomeItems.svelte";
	import ItemComp from "$lib/Item.svelte";

	let items: Item[] = [];
	let loading = true;
	onMount(() => {
		$ws.readAllItems()
			.then((result: Item[]) => {
				items = result;
			})
			.catch((error: any) => {
				console.error("Failed to fetch items:", error);
			})
			.finally(() => {
				loading = false;
			});
	});
</script>

<main>
	{#if loading}
		<div>Loading...</div>
	{:else if items.length === 0}
		<div>No items found.</div>
	{:else}
		{#each items as item}
			<ItemComp {item} />
		{/each}
	{/if}
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
	/* div.item {
		display: flex;
		padding-top: 5px;
		padding-bottom: 5px;
		padding-left: 25px;
	}
	div.name {
		padding-left: 10px;
	} */
</style>
