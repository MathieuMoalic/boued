<script lang="ts">
    import { scale } from "svelte/transition";
    import { enhance } from "$app/forms";
    import type { SubmitFunction } from "@sveltejs/kit";
    import { goto } from "$app/navigation";

    let open = false;
    let showLogoutConfirmation = false;
    let loggingOut = false;

    const toggle = () => (open = !open);
    const close = () => (open = false);

    function clickOutside(node: HTMLElement) {
        const onClick = (e: MouseEvent) => {
            if (!node.contains(e.target as Node)) close();
        };
        document.addEventListener("click", onClick, true);
        return {
            destroy: () => document.removeEventListener("click", onClick, true),
        };
    }

    const onKey = (e: KeyboardEvent) => {
        if (e.key === "Escape") {
            if (showLogoutConfirmation) showLogoutConfirmation = false;
            else close();
        }
    };

    const logoutEnhance: SubmitFunction = () => {
        loggingOut = true;
        open = false;

        return async ({ result }: { result: any }) => {
            loggingOut = false;

            if (result.type === "redirect") {
                await goto(result.location);
                return;
            }
            if (result.type === "success") {
                await goto("/login");
                return;
            }
            if (result.type === "failure") {
                alert(result.data?.message ?? "Logout failed");
                showLogoutConfirmation = false;
            }
        };
    };
</script>

<svelte:window on:keydown={onKey} />

<nav class="absolute top-0 right-0 z-50">
    <div class="relative" use:clickOutside>
        <button
            type="button"
            class="m-2 inline-flex h-10 w-10 items-center justify-center rounded border bg-primary-900 border-gray-600 text-primary-200 shadow-sm backdrop-blur"
            aria-label="Open menu"
            aria-expanded={open}
            aria-controls="main-menu"
            on:click={toggle}
        >
            <svg viewBox="0 0 24 24" class="h-6 w-6" aria-hidden="true">
                <path
                    d="M4 6h16M4 12h16M4 18h16"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                />
            </svg>
        </button>

        {#if open}
            <ul
                id="main-menu"
                role="menu"
                transition:scale={{ duration: 120 }}
                class="absolute right-2 top-14 min-w-36 overflow-hidden border bg-primary-900 border-gray-600 rounded text-primary-200 shadow-xl"
                style="transform-origin: top right;"
            >
                <li role="none">
                    <a
                        href="/"
                        role="menuitem"
                        class="flex items-center gap-3 px-4 py-3 hover:bg-zinc-100"
                        on:click={close}
                    >
                        <span class="font-medium">Home</span>
                    </a>
                </li>
                <li role="none">
                    <a
                        href="/categories"
                        role="menuitem"
                        class="block px-4 py-3 hover:bg-zinc-100"
                        on:click={close}>Categories</a
                    >
                </li>

                <li role="none" class="my-1 border-t border-zinc-200"></li>

                {#if showLogoutConfirmation}
                    <li role="none" class="px-4 py-3">
                        <div
                            class="flex flex-wrap items-center gap-3"
                            role="alertdialog"
                            aria-live="assertive"
                            aria-label="Confirm logout"
                        >
                            <span class="font-medium">Log out?</span>
                            <form
                                method="POST"
                                action="/logout"
                                class="flex items-center gap-2"
                                use:enhance={logoutEnhance}
                            >
                                <button
                                    type="submit"
                                    class="px-3 py-1 rounded text-sm bg-zinc-900 text-white hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-400/60 disabled:opacity-60 disabled:cursor-not-allowed"
                                    disabled={loggingOut}
                                >
                                    {loggingOut ? "…" : "Yes"}
                                </button>

                                <button
                                    type="button"
                                    class="px-3 py-1 rounded text-sm border border-zinc-300 text-zinc-700 hover:bg-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-400/60"
                                    on:click={() =>
                                        (showLogoutConfirmation = false)}
                                >
                                    No
                                </button>
                            </form>
                        </div>
                    </li>
                {:else}
                    <li role="none">
                        <button
                            type="button"
                            role="menuitem"
                            class="w-full text-left block px-4 py-3 hover:bg-zinc-100"
                            on:click={() => (showLogoutConfirmation = true)}
                        >
                            Logout
                        </button>
                    </li>
                {/if}
            </ul>
        {/if}
    </div>
</nav>
