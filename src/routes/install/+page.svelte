<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installInfo, updateInfo,
        startInstallation,
        getInstallationEvents,
        installProgress,
        reboot,
        autoscroll, startUpdate
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount, tick } from "svelte";
    import type { PageProps } from './$types';


    let logsPre: unknown;
    let scrollLocked = true;
    let progressLeftPos = 0;
    let installationProgress = 0;
    let pbVisible = false;
    let done = false;
    let progressAnimationInterval = 0;
    let logs = '-----------------------------------------------------------';

    export let data: { isUpdate: boolean };

    const scrollToBottom = async (node: HTMLElement) => {
        if (!scrollLocked) return;

        node.scroll({ top: node.scrollHeight, behavior: 'smooth' });
    }; 

    const startInstallationOnClient = () => {
        if (!pbVisible) {
            if (data.isUpdate) {
                startUpdate({...$installInfo, ...$updateInfo});
            }
            else {
                startInstallation($installInfo);
            }
        }
    };

    onMount(() => {
        startInstallationOnClient();

        const eventCheckerInterval = setInterval(async() => {
            const newEvents = await getInstallationEvents();
            if (newEvents.length > 0) {
                logs += '\n' + newEvents.join('\n');
            }
            await tick();
            // scrollToBottom(logsPre as HTMLElement);

            newEvents.forEach((content) => {
                if (content.includes('Project GDL Installed!')) {
                    clearInterval(eventCheckerInterval);
                    clearInterval(progressAnimationInterval);
                    done = true;
                    $installProgress.progress = $installProgress.total
                }

                if (content.includes('Fatal error. Installation failed.')) {
                    Swal.fire({
                        title: getString($installInfo.language, "error-installing"),
                        text: getString($installInfo.language, "fatal-error"),
                        icon: 'error',
                        background: '#222',
                        color: 'white',
                        confirmButtonColor: '#333'
                    });

                    clearInterval(eventCheckerInterval);
                    clearInterval(progressAnimationInterval);

                    done = true;
                }
            })
        }, 1000);

        progressAnimationInterval = setInterval(async() => {
            pbVisible = true;
        }, 1000);

        return () => {
            clearInterval(eventCheckerInterval);
            clearInterval(progressAnimationInterval);
        }
    });

    $: canGoFurther = true;
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="mdi:clock" width="40" height="40" />
            { getString($installInfo.language, "installing") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-start items-start flex-col px-20 w-full gap-10" use:autoscroll={{pauseOnUserScroll: true, behavior: "smooth"}}>
        <pre bind:this={logsPre} class="w-full flex flex-col gap-5 overflow-y-auto p-2 text-wrap" 
            style="height: 70vh;">{ logs }</pre>
    </div>

    <SetupPageBottom>
        {#if !done}
        <div class="w-full flex justify-start rounded-2xl overflow-hidden bg-zinc-700 h-4 relative">
            <div class={"pb-inner bg-slate-400 h-4 absolute" 
                + (!pbVisible ? " opacity-0" : " opacity-100")
                } style={`left: 0%; width: ${Math.round($installProgress.progress / $installProgress.total * 100)}%`}></div>
            </div>
        {:else}
            <GDLButton secondary on:click={() => {
                reboot();
            }}>
                { getString($installInfo.language, "restart") }
            </GDLButton>
        {/if}
    </SetupPageBottom>
</SetupPage>

<style>
    .pb-inner {
        transition: all 2s ease-in-out;
    }
</style>