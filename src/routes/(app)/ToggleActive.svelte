<script lang="ts">
    import { enhance } from "$app/forms";
    import { invalidate } from "$app/navigation";
    import Close from "$icons/Close.svelte";
    import Plus from "$icons/Plus.svelte";
    import Spinner from "$icons/Spinner.svelte";
    import { addAlert } from "$lib/client/alert";
    import { searchTerm } from "$lib/client/store";
    import type { SubmitFunction } from "@sveltejs/kit";

    export let item: { id: number; is_active: boolean };

    let loading = false;

    const handleEnhance: SubmitFunction = () => {
        loading = true;
        return async ({ result }) => {
            loading = false;
            switch (result.type) {
                case "success": {
                    await invalidate("app:items");
                    $searchTerm = "";
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
