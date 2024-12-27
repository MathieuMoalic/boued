<script lang="ts">
    import { ws } from "$lib/store";
    import type { Item } from "$lib/types";

    let searchQuery = ""; // User's search query
    let searchResults: Item[] = []; // Results from the backend
    let loading = false; // Loading state
    let errorMessage = ""; // Error message display
    let activeIndex = -1; // Index of the currently selected item

    async function performSearch() {
        if (!searchQuery.trim()) {
            errorMessage = "";
            searchResults = [];
            return;
        }

        errorMessage = "";
        loading = true;

        try {
            searchResults = await $ws.searchItems(searchQuery, 10, {
                is_active: true,
            });
        } catch (error) {
            console.error("Search failed:", error);
            errorMessage = "An error occurred during the search.";
        } finally {
            loading = false;
        }
    }

    function handleKeyDown(event: KeyboardEvent) {
        if (searchResults.length === 0) return;

        if (event.key === "ArrowDown") {
            event.preventDefault();
            activeIndex = (activeIndex + 1) % searchResults.length;
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            activeIndex =
                (activeIndex - 1 + searchResults.length) % searchResults.length;
        } else if (event.key === "Enter" && activeIndex !== -1) {
            event.preventDefault();
            selectItem(searchResults[activeIndex]);
        }
    }

    function selectItem(item: Item) {
        console.log("Selected item:", item);
    }
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div class="search-container" on:keydown={handleKeyDown} role="search">
    <div class="search-input">
        <input
            type="text"
            placeholder="Search items..."
            bind:value={searchQuery}
            on:input={performSearch}
        />
    </div>

    <!-- Popup for search results -->
    {#if searchResults.length > 0 || loading || errorMessage}
        <div class="popup">
            {#if loading}
                <p>Loading...</p>
            {:else if errorMessage}
                <p class="error">{errorMessage}</p>
            {:else if searchResults.length > 0}
                <ul class="results-list">
                    {#each searchResults as item, i}
                        <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
                        <!-- svelte-ignore a11y_click_events_have_key_events -->
                        <li
                            class="result-item {activeIndex === i
                                ? 'active'
                                : ''}"
                            tabindex="0"
                            on:click={() => selectItem(item)}
                        >
                            <strong>{item.name}</strong>
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>
    {/if}
</div>

<style>
    .search-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 1rem;
        border-radius: 8px;
        background: rgb(131, 35, 0); /* Red theme background */
        color: white;
        position: relative;
    }

    .search-input {
        margin-bottom: 1rem;
    }

    .search-input input {
        width: 100%;
        padding: 0.5rem;
        border: none;
        border-radius: 4px;
        background-color: rgb(108, 44, 42); /* Slightly darker red */
        color: white;
    }

    .search-input input::placeholder {
        color: hsl(208, 49%, 82%);
    }

    .popup {
        position: absolute; /* Ensure it positions below the input */
        top: 3.5rem; /* Space below the input */
        left: 0;
        width: 100%;
        max-height: 300px; /* Limit height of the popup */
        background-color: rgba(82, 19, 19, 0.95); /* Dark red overlay */
        color: white;
        z-index: 10;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        overflow-y: auto; /* Allow scrolling for long content */
    }

    .results-list {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }

    .result-item {
        padding: 0.5rem;
        border-bottom: 1px solid hsl(208, 49%, 82%);
        cursor: pointer;
    }

    .result-item:hover,
    .result-item.active {
        background-color: rgb(108, 44, 42); /* Highlight active item */
    }

    .error {
        color: hsl(0, 100%, 80%);
    }

    p {
        color: white;
        margin: 0.5rem 0;
    }
</style>
