<script lang="ts">
    import Icon from "@iconify/svelte";
    import type { TimezonesResponse } from "$lib";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput,
        installInfo, getTimezones, getRegionString,
        installationPage,
        getCityString

    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import GdlInput from "$lib/components/input/GDLInput.svelte";
    
    let timezones: TimezonesResponse = {};
    let filter1: string = "";
    let filter2: string = "";

    $: regionZones = $installInfo.timezoneRegion == '' ? [] : timezones[$installInfo.timezoneRegion];

    onMount(async() => {
        timezones = await getTimezones();
    });

    console.log(timezones);

    $: canGoFurther = !($installInfo.timezoneRegion == '' || $installInfo.timezoneInfo == '');
    
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

    <div class="flex justify-around items-center px-20 w-full gap-10">
        <div class="w-96 h-96 flex flex-col gap-5 overflow-y-auto p-2 masked-overflow">
            <GdlInput inputType="text" placeholder={getString($installInfo.language, 'search-placeholder')} bind:value={filter1} />
            {#each 
                Object.keys(timezones).sort()
                .filter((val, index, arr) => getRegionString($installInfo.language, val)
                    .toLowerCase().includes(filter1.toLowerCase())
                ) as region}
                <GDLButton secondary={$installInfo.timezoneRegion == region} 
                    on:click={() => $installInfo.timezoneRegion = region}>
                    { getRegionString($installInfo.language, region) }
                </GDLButton>
            {/each}
        </div>
        <div class="w-96 h-96 flex flex-col gap-5 overflow-y-auto p-2 masked-overflow">
            <GdlInput inputType="text" placeholder={getString($installInfo.language, 'search-placeholder')} bind:value={filter2} />
            {#each regionZones?.sort()
                .filter((val, index, arr) => getCityString($installInfo.language, val)
                    .toLowerCase().includes(filter2.toLowerCase())
                ) as zone}
                <GDLButton secondary={
                    $installInfo.timezoneRegion == $installInfo.timezoneRegion 
                    && $installInfo.timezoneInfo == zone
                }
                on:click={() => {
                    $installInfo.timezoneRegion = $installInfo.timezoneRegion as string;
                    $installInfo.timezoneInfo = zone;
                }}>
                { getCityString($installInfo.language, zone) }</GDLButton>
            {/each}
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => {
            $installationPage = $installationPage - 1;
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on:click={() => {
            if (!canGoFurther) {
                Swal.fire({
                    title: getString($installInfo.language, "introduce-error"),
                    text: getString($installInfo.language, "introduce-error-explaination"),
                    icon: 'error',
                    background: '#222',
                    color: 'white',
                    confirmButtonColor: '#333',
                    timer: 3000
                });
                return;
            }
            $installationPage = $installationPage + 1;
            goto("/desktop-environment");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>