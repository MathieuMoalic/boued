<script lang="ts">
	import ActiveItems from "$components/ActiveItems.svelte";
	import InactiveItems from "$components/InactiveItems.svelte";
	import Search from "$components/Search.svelte";
	import SearchResult from "$components/SearchResult.svelte";
	import { items, searching, ws } from "$lib/store";
	import { onMount } from "svelte";
	let isReady = false;
	onMount(async () => {
		$items = await $ws.readAllItems();
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
