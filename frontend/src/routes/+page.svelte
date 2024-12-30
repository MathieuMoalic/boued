<script lang="ts">
	import ActiveItems from "$components/ActiveItems.svelte";
	import InactiveItems from "$components/InactiveItems.svelte";
	import Search from "$components/Search.svelte";
	import SearchResult from "$components/SearchResult.svelte";
	import ItemForm from "$components/ItemForm.svelte";
	import { items, searching, api, categories } from "$lib/store";
	import { onMount } from "svelte";
	import AddItemButton from "$components/AddItemButton.svelte";
	import Alert from "$components/Alert.svelte";
	import { addAlert } from "$lib/alert";
	let isReady = false;
	onMount(async () => {
		let res = await api.items.readAll();
		if (!res.ok) {
			addAlert("Failed to fetch items: " + res.error, "error");
			return;
		} else {
			items.set(res.data);
		}
		let res2 = await api.categories.readAllCategory();
		if (!res2.ok) {
			addAlert("Failed to fetch categories: " + res2.error, "error");
			return;
		} else {
			categories.set(res2.data);
		}
		isReady = true;
	});
</script>

<Search />
{#if !isReady}
	<p>Loading...</p>
{:else if $searching}
	<SearchResult />
{:else}
	<ActiveItems />
	<hr class="m-4" />
	<InactiveItems />
{/if}
<ItemForm />
<AddItemButton />
<Alert />
