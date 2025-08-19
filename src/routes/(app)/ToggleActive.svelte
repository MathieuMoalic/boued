<script lang="ts">
    import { enhance } from "$app/forms";
    import Close from "$icons/Close.svelte";
    import Plus from "$icons/Plus.svelte";
    import Spinner from "$icons/Spinner.svelte";

    export let item: {
        id: number;
        is_active: boolean;
    };

    let loading = false;
</script>

{#if loading}
    <Spinner />
{:else}
    <form method="POST" class="mr-3 mt-1.5" use:enhance>
        <button
            class="text-gray-500 hover:text-gray-700"
            type="submit"
            formaction="?/toggle"
        >
            {#if item.is_active}
                <Close />
            {:else}
                <Plus />
            {/if}
        </button>
    </form>
{/if}
