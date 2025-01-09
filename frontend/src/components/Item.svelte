<script lang="ts">
    import { Li } from "flowbite-svelte";

    import type { ItemRead } from "$lib/Api";
    import QuantityField from "$components/QuantityField.svelte";
    import UnitField from "$components/UnitField.svelte";
    import NameField from "$components/NameField.svelte";
    import Notes from "$components/Notes.svelte";
    import ToggleActive from "$components/ToggleActive.svelte";
    import EditItem from "./EditItem.svelte";

    export let item: ItemRead;
</script>

<Li
    icon
    class="m-2 flex justify-between  items-center {item.is_active
        ? 'text-gray-50'
        : 'text-gray-500'}"
    id=" {item.id}"
>
    <div class="flex items-center space-x-0">
        <ToggleActive {item} />
        <QuantityField {item} />
        <UnitField {item} />
        <NameField {item} />
    </div>
    <Notes {item} />

    <div class="ml-auto">
        <EditItem {item} />
    </div>
</Li>
