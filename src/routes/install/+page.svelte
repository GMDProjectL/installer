<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        getDrives,
        installInfo,
        startInstallation,
        getInstallationEvents
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount, tick } from "svelte";


    let logsPre: unknown;
    let scrollLocked = true;
    let installationProgress = 40;
    let logs = '-----------------------------------------------------------';

    const scrollToBottom = async (node: HTMLElement) => {
        if (!scrollLocked) return;

        node.scroll({ top: node.scrollHeight, behavior: 'smooth' });
    }; 


    onMount(() => {
        startInstallation($installInfo);

        const eventCheckerInterval = setInterval(async() => {
            const newEvents = await getInstallationEvents();
            if (newEvents.length > 0) {
                logs += '\n' + newEvents.join('\n');
            }
            await tick();
            scrollToBottom(logsPre as HTMLElement);
        }, 1000);

        return () => {
            clearInterval(eventCheckerInterval);
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
        <div class="w-full flex justify-start rounded-2xl overflow-hidden bg-zinc-700 h-4">
            <div class="bg-slate-400 h-4 transition-all" style={`width: ${installationProgress}%`}></div>
        </div>
    </SetupPageBottom>
</SetupPage>