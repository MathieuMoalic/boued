<script lang="ts">
    import type { PageData } from "./$types";
    import { language } from "$lib/client/i18n";
    import Alert from "./Alert.svelte";
    import ConfirmPopup from "./ConfirmPopup.svelte";
    import Navbar from "./Navbar.svelte";
    export let data: PageData;
    language.set(data.language);
</script>

<Navbar />
<main>
    <Alert />
    <ConfirmPopup />
    <slot />
</main>
