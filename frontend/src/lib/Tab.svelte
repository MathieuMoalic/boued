<script lang="ts">
	import { tab } from "$lib/store";
	let tabs = ["Active", "Inactive"];
	let changeTab = (new_tab: string) => {
		tab.set(new_tab);
	};
</script>

<div>
	{#each tabs as new_tab}
		<button
			class={$tab === new_tab ? "active" : "inactive"}
			on:click={() => changeTab(new_tab)}
		>
			{new_tab}
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
