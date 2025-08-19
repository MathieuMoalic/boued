<script lang="ts">
    import type { PageData } from "./$types";
    import { language } from "$lib/client/i18n";
    import Alert from "./Alert.svelte";
    import ConfirmPopup from "./ConfirmPopup.svelte";
    export let data: PageData;
    language.set(data.language);
</script>

<main>
    <Alert />
    <ConfirmPopup />
    <slot />
</main>
