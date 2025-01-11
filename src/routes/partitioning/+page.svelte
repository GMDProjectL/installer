<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput,
        getDrives,
        installInfo,
        bytesToReadable,
        type DrivesResponse,
        type PartitionsResponse,

        getPartitions


    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";


    $: canGoFurther = false;

    let drives: DrivesResponse = {};

    onMount(async() => {
        drives = await getDrives();
    });

    let partitions: PartitionsResponse = {};

    $: console.log(partitions);
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="fluent:hard-drive-16-filled" width="40" height="40" />
            { getString($installInfo.language, "partitioning-title") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-between items-center flex-col px-20 w-full gap-10">
        <div class="w-auto flex flex-col gap-5 overflow-y-auto p-2">
            <div>
                <p>{ getString($installInfo.language, "select-drive") }</p>
                <select id="select-drive" 
                    class="bg-zinc-800 outline-0 p-4 rounded-xl mt-2 w-96"
                    on:change={(e) => {
                        $installInfo.selectedDrive = `${(e.target as any).value}`
                        getPartitions($installInfo.selectedDrive)
                        .then(response => partitions = response)
                    }}
                    >
                    <option disabled selected value>{ getString($installInfo.language, "no-drive-selected") }</option>
                    {#each Object.keys(drives)?.sort() as drive}
                        <option selected={$installInfo.selectedDrive == drive} 
                        value={drive}>
                            {drives[drive].model} - {bytesToReadable(drives[drive].size)} - {drive}
                        </option>
                    {/each}
                </select>
            </div>
            <div>
                <p>{ getString($installInfo.language, "drive-method") }</p>
                <select id="drive-method" 
                    class="bg-zinc-800 outline-0 p-4 rounded-xl mt-2 w-96"
                    on:change={(e) => {
                        $installInfo.selectedDrive = `${(e.target as any).value}`
                    }}
                    >
                    {#each ['nuke-drive', 'manual-partitioning'] as method}
                        <option selected={$installInfo.method == method} 
                        value={method}>
                            { getString($installInfo.language, method) }
                        </option>
                    {/each}
                </select>
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
            goto("/location");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>