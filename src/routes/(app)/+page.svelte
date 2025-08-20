<script lang="ts">
	import { goto } from "$app/navigation";
	import Edit from "$icons/Edit.svelte";
	import Plus from "$icons/Plus.svelte";
	import Search from "./Search.svelte";
	import ToggleActive from "./ToggleActive.svelte";
	import ItemList from "./ItemList.svelte";
	import { searchTerm } from "$lib/client/store";
	import type { PageData } from "./$types";
	import fuzzysort from "fuzzysort";
	import { derived } from "svelte/store";
	import ItemRow from "./ItemRow.svelte";

	export let data: PageData;

	let { categories, items } = data;

	const matched = derived([searchTerm], ([$searchTerm]) =>
		$searchTerm
			? fuzzysort
					.go($searchTerm, items, {
						keys: ["name"],
						threshold: -10000,
					})
					.map((r) => r.obj)
			: items,
	);

	let collapsed: (number | null)[] = [];

	function toggleCategory(catId: number | null) {
		if (collapsed.includes(catId)) {
			collapsed = collapsed.filter((id) => id !== catId);
		} else {
			collapsed = [...collapsed, catId];
		}
		localStorage.setItem("collapsedCategories", JSON.stringify(collapsed));
	}
</script>

<main>
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
			{#each $matched as item}
				<ItemRow {item} />
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
