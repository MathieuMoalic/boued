<script lang="ts">
	import ActiveItems from "$components/ActiveItems.svelte";
	import InactiveItems from "$components/InactiveItems.svelte";
	import Search from "$components/Search.svelte";
	import SearchResult from "$components/SearchResult.svelte";
	import ItemForm from "$components/ItemForm.svelte";
	import { items, searching, categories, authenticated } from "$lib/store";
	import { api, get_password, login } from "$lib/auth";
	import { onMount } from "svelte";
	import AddItemButton from "$components/AddItemButton.svelte";
	import Alert from "$components/Alert.svelte";
	import { addAlert } from "$lib/alert";
	import Login from "$components/Login.svelte";
	onMount(async () => {
		// The initial fetch of items and categories is done
		// in Login if the user is not authenticated.
		if (!$authenticated) {
			let password = get_password();
			if (password) {
				login();
			}
		}
		api.itemReadAll()
			.then((res) => {
				items.set(res.data);
			})
			.catch((res) => {
				addAlert("Failed to fetch items: " + res.error, "error");
			});
		api.categoryreadAll()
			.then((res) => {
				categories.set(res.data);
			})
			.catch((res) => {
				addAlert("Failed to fetch categories: " + res.error, "error");
			});
	});
</script>

{#if $authenticated}
	<Search />
	{#if $searching}
		<SearchResult />
	{:else}
		<ActiveItems />
		<hr class="m-4" />
		<InactiveItems />
	{/if}
	<ItemForm />
	<AddItemButton />
{:else}
	<Login />
{/if}
<Alert />
