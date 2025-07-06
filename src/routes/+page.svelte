<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, installInfo, checkInternetConnection,
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installationPage,
        reboot
    } from "$lib";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import Swal from "sweetalert2";

    let internetConnectionAvailable: boolean | null = null;

    onMount(() => {
        checkInternetConnection().then(status => internetConnectionAvailable = status);
        
        const internetConnectionInterval = setInterval(async() => {
            internetConnectionAvailable = await checkInternetConnection();
        }, 5000);

        return () => {
            clearInterval(internetConnectionInterval);
        }
    })
</script>


<SetupPage>
    <SetupPageTitle>
        { getString($installInfo.language, "welcome") }
        <span class="text-base mt-4 text-zinc-400 font-normal">
            { getString($installInfo.language, "welcome-description") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-between items-center flex-col px-20 w-full gap-10">
        <h2 class="text-2xl font-semibold text-center flex w-full gap-4 justify-center items-center">
            <Icon icon="material-symbols:language" width="30" height="30" />
            { getString($installInfo.language, "language-tip") }
        </h2>

        <div class="w-96 flex flex-col gap-5 h-40 overflow-y-auto p-2">
            {#each ["en", "ru"] as lang}
                <GDLButton on:click={() => {
                    $installInfo.language = lang;
                }}>
                    <span class={$installInfo.language == lang ? "font-bold" : "font-normal"}>
                        { getString(lang, "name") }
                    </span>
                </GDLButton>
            {/each}
        </div>

        {#if internetConnectionAvailable === false}
        <div class="text-red-500 text-center text-lg">
            { getString($installInfo.language, "no-internet") }
        </div>
        {/if}
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
                reboot();
            }
        }}>
            { getString($installInfo.language, "quit") }
        </GDLButton>
        <GDLButton secondary disabled={!internetConnectionAvailable} 
        on:click={() => {
            if (!internetConnectionAvailable) {
                return;
            }

            $installationPage = $installationPage + 1;

            goto("/introduce-yourself");
        }}>
            { 
                internetConnectionAvailable === null
                ? getString($installInfo.language, "checking-for-connection")
                : getString($installInfo.language, "begin")
            }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>