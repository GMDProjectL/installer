<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        getDrives,
        installInfo,
        startInstallation
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";


    let installationProgress = 40;


    onMount(async() => {
        startInstallation($installInfo);
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
        <div class="w-auto flex flex-col gap-5 overflow-y-auto p-2" style="height: 70vh;">
            
        </div>
    </div>

    <SetupPageBottom>
        <div class="w-full flex justify-start rounded-2xl overflow-hidden bg-zinc-700 h-4">
            <div class="bg-slate-400 h-4 transition-all" style={`width: ${installationProgress}%`}></div>
        </div>
    </SetupPageBottom>
</SetupPage>