<script lang="ts">
    import { Li } from "flowbite-svelte";

    import type { Item } from "$lib/types";
    import QuantityField from "$components/QuantityField.svelte";
    import UnitField from "$components/UnitField.svelte";
    import NameField from "$components/NameField.svelte";
    import Notes from "$components/Notes.svelte";
    import ToggleActive from "$components/ToggleActive.svelte";
    import EditItem from "./EditItem.svelte";

    export let item: Item;
</script>

<Li icon class="m-2 {item.is_active ? 'text-gray-50' : 'text-gray-500'}" id="1">
    <ToggleActive {item} />
    <QuantityField {item} />
    <UnitField {item} />
    <NameField {item} />
    <Notes {item} />
    <EditItem {item} />
</Li>
