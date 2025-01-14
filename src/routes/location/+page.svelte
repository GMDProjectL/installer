<script lang="ts">
    import Icon from "@iconify/svelte";
    import type { TimezonesResponse } from "$lib";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput,
        installInfo, getTimezones
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    
    let timezones: TimezonesResponse = {};
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
            {#each Object.keys(timezones).sort() as region}
                <GDLButton secondary={$installInfo.timezoneRegion == region} 
                    on:click={() => $installInfo.timezoneRegion = region}>
                    { region }
                </GDLButton>
            {/each}
        </div>
        <div class="w-96 h-96 flex flex-col gap-5 overflow-y-auto p-2 masked-overflow">
            {#each regionZones?.sort() as zone}
                <GDLButton secondary={
                    $installInfo.timezoneRegion == $installInfo.timezoneRegion 
                    && $installInfo.timezoneInfo == zone
                }
                on:click={() => {
                    $installInfo.timezoneRegion = $installInfo.timezoneRegion as string;
                    $installInfo.timezoneInfo = zone;
                }}>
                { zone }</GDLButton>
            {/each}
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => history.back()}>
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
            goto("/additional-software");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>