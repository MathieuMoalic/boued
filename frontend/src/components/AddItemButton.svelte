<script>
    import { modal } from "$lib/store";
    import { Button } from "flowbite-svelte";
</script>

<Button
    size="lg"
    class="fixed bottom-4 right-4"
    on:click={() => {
        $modal.mode = "add";
        $modal.item = {
            name: "",
            quantity: 0,
            unit: "None",
            category: "Other",
            notes: "",
        };
        $modal.isOpen = true;
    }}
>
    +
</Button>
