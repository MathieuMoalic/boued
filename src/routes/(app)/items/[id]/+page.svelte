<script lang="ts">
	import ItemForm from "../ItemForm.svelte";
	import type { PageData } from "./$types";
	export let data: PageData;
	let item = data.item
		? {
				name: data.item.name,
				quantity: data.item.quantity ?? 0,
				unit: data.item.unit,
				category_id: data.item.category_id,
				notes: data.item.notes,
			}
		: {
				name: "Item not found",
				quantity: 0,
				unit: "pcs",
				category_id: null,
				notes: "",
			};
	let categories = data.categories;
</script>

<ItemForm {item} {categories} mode="edit" />
