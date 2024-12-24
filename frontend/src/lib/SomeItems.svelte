<script lang="ts">
    import type { Item } from "$lib/types";
    import { ws } from "$lib/store";

    /**
     * Sends several new items to the server via WebSocket.
     * This example assumes the server will accept 'createItem' actions
     * and respond with success or error.
     */
    async function populateItems() {
        const newItems: Item[] = [
            {
                name: "Hammer",
                category: "Tools",
                is_active: true,
                quantity: 10,
                unit: "pcs",
                notes: "Heavy duty",
            },
            {
                name: "Nails",
                category: "Hardware",
                is_active: true,
                quantity: 100,
                unit: "pcs",
                notes: "Steel nails",
            },
            {
                name: "Drill",
                category: "Tools",
                is_active: false,
                quantity: 2,
                unit: "pcs",
                notes: "Cordless model",
            },
            {
                name: "Wood Plank",
                category: "Lumber",
                is_active: true,
                quantity: 15,
                unit: "pieces",
                notes: "Oak wood",
            },
        ];

        for (const item of newItems) {
            try {
                const response = await $ws.createItem(item);
                console.log("Created item:", response);
            } catch (err) {
                console.error("Error creating item:", err);
            }
        }
    }
</script>

<main>
    <button on:click={populateItems}> Populate Items on Server </button>
</main>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
    }
    main {
        padding: 1rem;
    }
    button {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
    }
</style>
