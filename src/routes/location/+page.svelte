<script lang="ts">
    import Icon from "@iconify/svelte";
    import type { TimezonesResponse } from "$lib";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installInfo, getTimezones, getRegionString,
        installationPage,
        getCityString

    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import GdlInput from "$lib/components/input/GDLInput.svelte";

    installationPage.set(3);
    
    let timezones: TimezonesResponse = {};
    let filter1: string = "";
    let filter2: string = "";

    $: regionZones = $installInfo.timezoneRegion == '' ? [] : timezones[$installInfo.timezoneRegion];

    onMount(async() => {
        timezones = await getTimezones();
    });

    console.log(timezones);

    $: canGoFurther = !($installInfo.timezoneRegion == '' || $installInfo.timezoneInfo == '');

    const filterPredicate = (val: string, filter: string) => val.toLowerCase().includes(filter.toLowerCase());

    $: regionResults = Object.keys(timezones).sort()
                .filter((val) => filterPredicate(val, filter1));
    
    $: zoneResults = regionZones?.sort()
                .filter((val) => filterPredicate(val, filter2));
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="material-symbols:language" width="40" height="40" />
            { getString($installInfo.language, "location-title") }
        </span>
        <span class="text-base mt-4 text-zinc-400 font-normal">
            { getString($installInfo.language, "location-title-description") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-center items-center px-20 w-full gap-40">
        <div class="w-96 h-96 flex flex-col gap-5 overflow-y-auto p-2 masked-overflow">
            <GdlInput inputType="text" placeholder={getString($installInfo.language, 'search-placeholder')} bind:value={filter1} />
            {#each regionResults as region}
                <GDLButton secondary={$installInfo.timezoneRegion == region} 
                    on_click={() => $installInfo.timezoneRegion = region}>
                    { getRegionString($installInfo.language, region) != region ? 
                        getRegionString($installInfo.language, region) + ` (${region})` : region }
                </GDLButton>
            {/each}
        </div>
        <div class="w-96 h-96 flex flex-col gap-5 overflow-y-auto p-2 masked-overflow">
            {#if regionZones?.length == 0}
                <div class="text-center text-zinc-400 flex flex-col items-center justify-center h-full no-select">
                    { getString($installInfo.language, "select-region") }
                </div>
            {:else}
                <GdlInput inputType="text" placeholder={getString($installInfo.language, 'search-placeholder')} bind:value={filter2} />
                {#each zoneResults as zone}
                    <GDLButton secondary={
                        $installInfo.timezoneRegion == $installInfo.timezoneRegion 
                        && $installInfo.timezoneInfo == zone
                    }
                    on_click={() => {
                        $installInfo.timezoneRegion = $installInfo.timezoneRegion as string;
                        $installInfo.timezoneInfo = zone;
                    }}>
                    { getCityString($installInfo.language, zone) != zone ?
                        getCityString($installInfo.language, zone) + ` (${zone})` : zone }</GDLButton>
                {/each}
            {/if}
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on_click={() => {
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on_click={() => {
            if (!canGoFurther) {
                Swal.fire({
                    title: getString($installInfo.language, "introduce-error"),
                    text: getString($installInfo.language, "introduce-error-explaination"),
                    icon: 'error',
                    background: '#222',
                    color: 'white',
                    confirmButtonColor: '#333',
                    timer: 3000,
                    customClass: {
                        popup: "no-select"
                    }
                });
                return;
            }
            goto("/desktop-environment");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>