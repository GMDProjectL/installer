<script lang="ts">
    import { 
        getString, installInfo,
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installationPage,
        getSystemLanguage
    } from "$lib";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    onMount(async() => {
        const lang = await getSystemLanguage();
        $installInfo.language = lang;
    })

    installationPage.set(0);
</script>

<title>{ getString($installInfo.language, "update-title") }</title>

<SetupPage>
    <SetupPageTitle>
        { getString($installInfo.language, "update-title") }
    </SetupPageTitle>

    <div class="flex justify-between items-center flex-col px-20 w-full gap-10">
        <h2 class="text-2xl font-semibold text-center flex w-full gap-4 justify-center items-center">
            { getString($installInfo.language, "update-body") }
        </h2>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => window.close()}>
            { getString($installInfo.language, "quit") }
        </GDLButton>
        <GDLButton secondary
            on:click={() => {
                goto("/update/info");
            }}>
            { 
                getString($installInfo.language, "begin")
            }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>