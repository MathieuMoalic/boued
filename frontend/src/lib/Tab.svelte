<script lang="ts">
	import { writable } from 'svelte/store';

	// Store for the current active tab
	export const category = writable('Groceries');

	// List of tabs (can be extended dynamically)
	let tabs = ['Groceries', 'Alcohol', 'Snacks', 'Beverages'];

	// Function to change the active tab
	let changeTab = (tab: string) => {
		category.set(tab);
	};
</script>

<div>
	{#each tabs as tab}
		<button class={$category === tab ? 'active' : 'inactive'} on:click={() => changeTab(tab)}>
			{tab}
		</button>
	{/each}
</div>

<style>
	div {
		display: flex;
	}
	button {
		border: 0px solid red;
		width: 100%;
		font-size: large;
		height: 2rem;
		margin: 0px;
		padding: 0px;
		font-weight: bold;
		text-align: center;
		color: hsl(208, 49%, 82%);
		cursor: pointer;
	}
	.active {
		background-color: rgb(108, 44, 42);
	}
	.inactive {
		background-color: rgb(131, 35, 0);
	}
</style>
