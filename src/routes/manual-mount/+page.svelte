<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installInfo,
        bytesToReadable,
        type PartitionsResponse,
        getPartitions,
        installationPage
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import GdlButton from "$lib/components/button/GDLButton.svelte";

    installationPage.set(5);

    let partitions: PartitionsResponse = {};

    onMount(async() => {
        partitions = await getPartitions($installInfo.selectedDrive);
    });


    $: console.log(partitions);
    $: canGoFurther = $installInfo.bootPartition != '' && $installInfo.rootPartition != '';
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="fluent:hard-drive-16-filled" width="40" height="40" />
            { getString($installInfo.language, "manual-mount-title") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-start items-center flex-col px-20 w-full gap-10">
        <div class="w-auto flex flex-col gap-5 overflow-y-auto p-2">
            <h2 class="text-xl font-bold" style="width: 400px;">
                { getString($installInfo.language, "selected-drive") }
                /dev/{$installInfo.selectedDrive}
            </h2>

            <div>
                <p>{ getString($installInfo.language, "boot-partition") }</p>
                <select id="select-boot-part" 
                    class="bg-zinc-800 outline-0 p-4 rounded-md mt-2 w-full"
                    on:change={(e) => {
                        $installInfo.bootPartition = `${(e.target as any).value}`
                    }}
                    >
                    <option disabled selected value>{ getString($installInfo.language, "no-partition-selected") }</option>
                    {#each Object.keys(partitions)?.sort() as partition}
                        <option selected={$installInfo.bootPartition == partition} 
                        value={partition}>
                            {partition} - {bytesToReadable(partitions[partition].size)}
                        </option>
                    {/each}
                </select>
                <div class="mt-3 flex gap-4 items-center">
                    <input 
                        class="scale-125 -translate-y-px outline-0"
                        bind:checked={$installInfo.formatBootPartition} 
                        type="checkbox" 
                        id="boot-partition-checkbox" />

                    <label for="boot-partition-checkbox">
                        { getString($installInfo.language, "format") }
                    </label>
                </div>
            </div>

            <div class="mt-3">
                <p>{ getString($installInfo.language, "root-partition") }</p>
                <select id="select-root-part" 
                    class="bg-zinc-800 outline-0 p-4 rounded-md mt-2 w-full"
                    on:change={(e) => {
                        $installInfo.rootPartition = `${(e.target as any).value}`
                    }}
                    >
                    <option disabled selected value>{ getString($installInfo.language, "no-partition-selected") }</option>
                    {#each Object.keys(partitions)?.sort() as partition}
                        <option selected={$installInfo.rootPartition == partition} 
                        value={partition}>
                            {partition} - {bytesToReadable(partitions[partition].size)}
                        </option>
                    {/each}
                </select>
            </div>
            
            <div class="mt-3">
                <GdlButton on:click={async() => {
                    partitions = await getPartitions($installInfo.selectedDrive);
                }}>
                    { getString($installInfo.language, "drive-update") }
            </GdlButton>
            </div>
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
            goto("/summary");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>