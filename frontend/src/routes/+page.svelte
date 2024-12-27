<script lang="ts">
	import List from "$components/List.svelte";
	import Search from "$components/Search.svelte";
</script>

<Search />
<List />

<style>
	:global(body) {
		font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
		background-image: url("/background.avif");
		background-attachment: fixed;
	}
</style>
