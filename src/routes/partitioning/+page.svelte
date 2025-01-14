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

    let drives: DrivesResponse = {};

    onMount(async() => {
        drives = await getDrives();
    });

    let partitions: PartitionsResponse = {};

    $: console.log(partitions);


    $: canGoFurther = $installInfo.selectedDrive != '';
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="fluent:hard-drive-16-filled" width="40" height="40" />
            { getString($installInfo.language, "partitioning-title") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-start items-center flex-col px-20 w-full gap-10">
        <div class="w-auto flex flex-col gap-5 overflow-y-auto p-2">
            <div>
                <p>
                    { getString($installInfo.language, "select-drive") }
                    <a class="ms-3 text-blue-200" href="#" on:click={async() => {
                        drives = await getDrives();
                    }}>
                        ({ getString($installInfo.language, "drive-update") })
                    </a>
                </p>
                <select id="select-drive" 
                    class="bg-zinc-800 outline-0 p-4 rounded-md mt-2 w-full"
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
                    class="bg-zinc-800 outline-0 p-4 rounded-md mt-2 w-full"
                    on:change={(e) => {
                        $installInfo.method = `${(e.target as any).value}`
                    }}
                    >
                    {#each ['manual-partitioning'] as method}
                        <option selected={$installInfo.method == method} 
                        value={method}>
                            { getString($installInfo.language, method) }
                        </option>
                    {/each}
                </select>
                <p class={"text-red-500 mt-2" + (
                    $installInfo.method == 'nuke-drive'
                    ? ""
                    : " text-transparent"
                )}> {getString($installInfo.language, "nuke-warning")} </p>

                <div class={$installInfo.method != 'manual-partitioning' ? "opacity-0 pointer-events-none" : ""}>
                    <p class="mb-5 opacity-50 w-96 text-wrap whitespace-pre">{ getString($installInfo.language, "partitioning-disclaimer") }</p>

                    <GDLButton on:click={() => fetch("/open-gnome-disks")}>
                        { getString($installInfo.language, "open-gnome-disks") }
                    </GDLButton>
                </div>
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

            if ($installInfo.method == 'nuke-drive') {
                $installInfo.bootPartition = $installInfo.selectedDrive + '1';
                $installInfo.rootPartition = $installInfo.selectedDrive + '2';
            }

            goto(
                $installInfo.method != 'manual-partitioning'
                ? "/summary"
                : "/manual-mount"
            );
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>