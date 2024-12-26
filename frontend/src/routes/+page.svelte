<script lang="ts">
	import List from "$lib/List.svelte";
	import Tab from "$lib/Tab.svelte";
	import Search from "$lib/Search.svelte";
</script>

<Search />
<Tab />
<List />

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
</style>
