<script lang="ts">
    import { addAlert } from "$lib/alert";
    import { api, login, password } from "$lib/auth";
    import { authenticated, categories, items } from "$lib/store";
    import { ArrowLeftToBracketOutline } from "flowbite-svelte-icons";

    async function authenticate() {
        login();
        if (!$authenticated) {
            return;
        }
        api.itemReadAll()
            .then((res) => {
                $items = res.data;
            })
            .catch((res) => {
                addAlert(res.error.detail, "error");
                return;
            });
        api.categoryreadAll()
            .then((res) => {
                $categories = res.data;
            })
            .catch((res) => {
                addAlert("Failed to fetch categories: " + res.error, "error");
            });
    }
</script>

<div class="flex flex-col justify-center items-center h-screen w-screen m-0">
    <div class="flex col-auto">
        <input
            class="mr-2"
            type="password"
            bind:value={$password}
            on:keydown={(e) => e.key === "Enter" && authenticate()}
            placeholder="Enter password ..."
        />
        <button
            on:click={authenticate}
            class="border rounded w-10 h-10 flex justify-center items-center border-primary-500"
        >
            <ArrowLeftToBracketOutline color="orange" />
        </button>
    </div>
</div>
