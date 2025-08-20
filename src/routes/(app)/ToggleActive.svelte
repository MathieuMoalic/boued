<script lang="ts">
    import { enhance } from "$app/forms";
    import Close from "$icons/Close.svelte";
    import Plus from "$icons/Plus.svelte";
    import Spinner from "$icons/Spinner.svelte";
    import { addAlert } from "$lib/client/alert";
    import type { SubmitFunction } from "@sveltejs/kit";

    export let item: {
        id: number;
        is_active: boolean;
    };

    let loading = false;
    const handleEnhance: SubmitFunction = () => {
        return async ({ result }) => {
            switch (result.type) {
                case "success": {
                    if (result.data && result.data.item) {
                        item = result.data.item;
                    }
                    break;
                }
                case "failure": {
                    addAlert(result.data?.error ?? "Unknown error", "error");
                    break;
                }
            }
        };
    };
</script>

{#if loading}
    <Spinner />
{:else}
    <form method="POST" class="mr-3 mt-1.5" use:enhance={handleEnhance}>
        <input type="hidden" name="id" value={item.id} />
        <button
            class="text-gray-500 hover:text-gray-700"
            type="submit"
            formaction="?/toggle"
        >
            {#if item.is_active}
                <Close className="w-5 h-5 text-primary-200" />
            {:else}
                <Plus className="w-5 h-5 text-primary-200" />
            {/if}
        </button>
    </form>
{/if}
