<script lang="ts">
	import { goto } from "$app/navigation";
	import Edit from "$icons/Edit.svelte";
	import Plus from "$icons/Plus.svelte";
	import Search from "./Search.svelte";
	import ToggleActive from "./ToggleActive.svelte";
	import { searchTerm } from "$lib/client/store";
	import type { PageData } from "./$types";
	import fuzzysort from "fuzzysort";
	import { derived } from "svelte/store";

	export let data: PageData;

	let { categories, items } = data;

	// returns the items that match best, already sorted
	const matched = derived(
		[searchTerm],
		([$searchTerm]) =>
			$searchTerm
				? fuzzysort
						.go($searchTerm, items, {
							// what to search through – add more fields if you like
							keys: ["name"],
							threshold: -10000, // anything below this score is ignored
						})
						.map((r) => r.obj) // grab the original records
				: items, // nothing typed → show everything
	);

	let collapsed: number[] = [];

	function toggleCategory(catId: number) {
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
			on:click={() => {
				goto("/items/new");
			}}
		>
			<div class="mr-2">
				<Plus />
			</div>
			{$searchTerm}
		</button>
		<ul class="text-gray-200">
			{#each $matched as item}
				<li class="m-0 flex justify-between items-center">
					<div
						class="flex items-center truncate overflow-hidden max-w-full {item.is_active
							? 'text-gray-50'
							: 'text-gray-400'}"
					>
						<ToggleActive {item} />
						{#if item.quantity !== null}<div class="mr-1">
								{item.quantity}
							</div>{/if}
						{#if item.unit !== "None"}<div class="mr-2">
								{item.unit}
							</div>{/if}
						<span class="overflow-ellipsis">{item.name}</span>
						{#if item.notes !== ""}<span
								class="ml-2 text-gray-500 truncate"
								>| {item.notes}</span
							>{/if}
					</div>
					<button
						on:click={() => goto(`/items/${item.id}`)}
						class="text-primary-500 rounded-md backdrop-blur-sm h-6 w-6"
					>
						<Edit />
					</button>
				</li>
			{/each}
		</ul>
	{:else}
		<ul class="text-gray-200">
			{#each categories as category}
				{#if items.some((item) => item.is_active && item.category_id === category.id)}
					<li class="block">
						<button
							on:click={() => toggleCategory(category.id)}
							class="w-full text-left pl-2 flex items-center rounded-md"
						>
							<h5 class="text-lg font-bold text-gray-400">
								{category.name}
							</h5>
							<span class="ml-2">
								{#if collapsed.includes(category.id)}
									▲
								{:else}
									▼
								{/if}
							</span>
						</button>

						{#each items as item}
							{#if item.is_active && item.category_id === category.id && !collapsed.includes(category.id)}
								<div class="ml-3">
									<li
										class="m-0 flex justify-between items-center"
									>
										<div
											class="flex items-center truncate overflow-hidden max-w-full {item.is_active
												? 'text-gray-50'
												: 'text-gray-400'}"
										>
											<ToggleActive {item} />
											{#if item.quantity !== null}
												<div class="mr-1">
													{item.quantity}
												</div>
											{/if}
											{#if item.unit !== "None"}
												<div class="mr-2">
													{item.unit}
												</div>
											{/if}
											<span class="overflow-ellipsis">
												{item.name}
											</span>
											{#if item.notes !== ""}
												<div class="w-2"></div>
												<span
													class="text-gray-500 truncate overflow-hidden text-ellipsis"
												>
													| {item.notes}
												</span>
											{/if}
										</div>
										<button
											on:click={() =>
												goto(`/items/${item.id}`)}
											class="text-primary-500 rounded-md backdrop-blur-sm h-6 w-6"
										>
											<Edit />
										</button>
									</li>
								</div>
							{/if}
						{/each}
					</li>
				{/if}
			{/each}
		</ul>
	{/if}
</main>
