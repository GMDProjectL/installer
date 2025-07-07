<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, installInfo, checkInternetConnection,
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installationPage,
        getSystemLanguage
    } from "$lib";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import Swal from "sweetalert2";

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
        <GDLButton on:click={async() => {
            const dialogResult = await Swal.fire({
                title: getString($installInfo.language, "quit-question-title"),
                text: getString($installInfo.language, "quit-question"),
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: getString($installInfo.language, "yes"),
                cancelButtonText: getString($installInfo.language, "cancel"),
                background: '#222',
                color: 'white',
                confirmButtonColor: '#333',
            })

            if (dialogResult.isConfirmed) {
                window.close();
            }
        }}>
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