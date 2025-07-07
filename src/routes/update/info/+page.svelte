<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, installInfo, getDE,
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installationPage, getSystemLanguage, getUsername, 
        AdditionalFeaturesContent

    } from "$lib";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { updateInfo } from "$lib/stores/install-info";

    onMount(async() => {
        const lang = await getSystemLanguage();
        const username = await getUsername();
        const de = await getDE();

        $installInfo.language = lang;
        $updateInfo.username = username;
        $installInfo.de = de;
        $updateInfo.de = de;
    })

    installationPage.set(1);
</script>

<title>{ getString($installInfo.language, "update-title") }</title>

<SetupPage>
    <SetupPageTitle>
        { getString($installInfo.language, "features") }
    </SetupPageTitle>

    <AdditionalFeaturesContent>
        <div class="flex items-center gap-5">
            <input id="dontCopyKde" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$updateInfo.dontCopyKde} />
            <label for="dontCopyKde" class="flex items-center gap-4 font-bold">
                { getString($installInfo.language, "dont-copy-kde-config") }
                <Icon icon="akar-icons:cross" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="dontUpdateGrub" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$updateInfo.dontUpdateGrub} />
            <label for="dontUpdateGrub" class="flex items-center gap-4 font-bold">
                { getString($installInfo.language, "dont-update-grub") }
                <Icon icon="akar-icons:cross" />
            </label>
        </div>
    </AdditionalFeaturesContent>

    <SetupPageBottom>
        <GDLButton on:click={async() => {
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary
            on:click={() => {
                goto("/install?update=true");
            }}>
            { 
                getString($installInfo.language, "install")
            }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>