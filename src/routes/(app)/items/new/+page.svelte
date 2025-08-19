<script lang="ts">
    import { searchTerm } from "$lib/client/store";
    import ItemForm from "../ItemForm.svelte";
    import type { PageData } from "./$types";
    export let data: PageData;

    let item = {
        name: $searchTerm,
        quantity: 0,
        unit: "pcs",
        category_id: null,
        notes: "",
    };

    let categories = data.categories;
</script>

<ItemForm {item} {categories} mode="create" />
