<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import Plus from "$icons/Plus.svelte";
	import Search from "./Search.svelte";
	import ItemList from "./ItemList.svelte";
	import { searchTerm } from "$lib/client/store";
	import type { PageData } from "./$types";
	import fuzzysort from "fuzzysort";
	import ItemRow from "./ItemRow.svelte";

	export let data: PageData;

	let items = data.items;
	let categories = data.categories;
	$: ({ items, categories } = data);

	$: filtered = $searchTerm
		? fuzzysort
				.go($searchTerm, items, { keys: ["name"], threshold: -10000 })
				.map((r) => r.obj)
		: items;

	let collapsed: (number | null)[] = [];

	onMount(() => {
		const raw = localStorage.getItem("collapsedCategories");
		if (raw) {
			const parsed = JSON.parse(raw);
			if (Array.isArray(parsed)) {
				const valid = new Set<number | null>([
					null,
					...categories.map((c) => c.id),
				]);
				collapsed = parsed
					.filter((id) => id === null || typeof id === "number")
					.filter((id) => valid.has(id));
			}
		}
	});

	function toggleCategory(catId: number | null) {
		if (collapsed.includes(catId)) {
			collapsed = collapsed.filter((id) => id !== catId);
		} else {
			collapsed = [...collapsed, catId];
		}
		localStorage.setItem("collapsedCategories", JSON.stringify(collapsed));
	}
</script>

<main class="px-1.5">
	<Search />
	{#if $searchTerm}
		<button
			class="bg-primary-700 mx-2 my-2 font-semibold rounded-md flex items-center justify-center p-2 w-[calc(100%-1rem)] text-gray-100 hover:bg-primary-600 transition"
			on:click={() => goto("/items/new")}
		>
			<div class="mr-2"><Plus /></div>
			{$searchTerm}
		</button>

		<ul class="text-gray-200">
			{#each filtered as item}
				<ItemRow bind:item />
			{/each}
		</ul>
	{:else}
		<ul class="text-gray-200">
			<ItemList
				category={{ id: null, name: "Other" }}
				{items}
				{collapsed}
				{toggleCategory}
			/>

			{#each categories as category}
				<ItemList {category} {items} {collapsed} {toggleCategory} />
			{/each}
		</ul>
	{/if}
</main>
