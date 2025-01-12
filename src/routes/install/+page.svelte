<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        getDrives,
        installInfo,
        startInstallation,
        getInstallationEvents,

        reboot

    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount, tick } from "svelte";


    let logsPre: unknown;
    let scrollLocked = true;
    let progressLeftPos = 0;
    let installationProgress = 0;
    let pbVisible = false;
    let done = false;
    let progressAnimationInterval = 0;
    let logs = '-----------------------------------------------------------';

    const scrollToBottom = async (node: HTMLElement) => {
        if (!scrollLocked) return;

        node.scroll({ top: node.scrollHeight, behavior: 'smooth' });
    }; 


    const sleepAwait = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));


    onMount(() => {
        startInstallation($installInfo);

        const eventCheckerInterval = setInterval(async() => {
            const newEvents = await getInstallationEvents();
            if (newEvents.length > 0) {
                logs += '\n' + newEvents.join('\n');
            }
            await tick();
            scrollToBottom(logsPre as HTMLElement);

            newEvents.forEach((content) => {
                if (content.includes('Project GDL Installed!')) {
                    clearInterval(eventCheckerInterval);
                    clearInterval(progressAnimationInterval);
                    done = true;
                }
            })
        }, 1000);

        progressAnimationInterval = setInterval(async() => {
            pbVisible = true;
            installationProgress = 30;

            for (let int = 0; int < 70; int++) {
                progressLeftPos = int;
                await sleepAwait(16);
            }
            
            for (let int = 70; int > 0; int--) {
                progressLeftPos = int;
                await sleepAwait(27);
            }
            
        }, 3000);

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

    <div class="flex justify-start items-start flex-col px-20 w-full gap-10">
        <pre bind:this={logsPre} class="w-full flex flex-col gap-5 overflow-y-auto p-2 text-wrap" 
            style="height: 70vh;">{ logs }</pre>
    </div>

    <SetupPageBottom>
        {#if !done}
        <div class="w-full flex justify-start rounded-2xl overflow-hidden bg-zinc-700 h-4 relative">
            <div class={"bg-slate-400 h-4 transition-all absolute" + (!pbVisible ? " opacity-0" : " opacity-100")}
                    style={`left: ${progressLeftPos}%; width: ${installationProgress}%`}></div>
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