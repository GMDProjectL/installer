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
        getPartitions,
        installationPage
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    let drives: DrivesResponse = {};

    onMount(async() => {
        drives = await getDrives();
    });

    $: canGoFurther = true;
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="material-symbols:checklist" width="40" height="40" />
            { getString($installInfo.language, "summary") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-start items-start flex-col px-20 w-full gap-10">
        <div class="w-full flex flex-col gap-5 overflow-y-auto p-2" style="height: 70vh;">
            <div class="mt-3">
                <p>
                    <b class="me-3">• { getString($installInfo.language, "summary-language") }</b>
                    { getString($installInfo.language, "name") }
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "summary-identity")}</b>
                    {$installInfo.username}@{$installInfo.computerName}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "summary-timezone")}</b>
                    {$installInfo.timezoneRegion}/{$installInfo.timezoneInfo}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "desktop-environment")}:</b>
                    {$installInfo.de.toUpperCase()}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "summary-drive")}</b>
                    /dev/{$installInfo.selectedDrive} - {drives[$installInfo.selectedDrive]?.model} ({bytesToReadable(drives[$installInfo.selectedDrive]?.size)})
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "summary-boot-partition")}</b>
                    /dev/{$installInfo.bootPartition}
                </p>
                <p>
                    <b class="ms-4 me-3">{getString($installInfo.language, "summary-format-boot-partition")}</b>
                    {$installInfo.formatBootPartition ? "✓" : "x"}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "summary-root-partition")}</b>
                    /dev/{$installInfo.rootPartition}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="me-3">• {getString($installInfo.language, "enable-multilib-repo")}</b>
                    {$installInfo.enableMultilibRepo ? "✓" : "x"}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="ms-4 me-3">• {getString($installInfo.language, "install-steam")}</b>
                    {$installInfo.installSteam ? "✓" : "x"}
                </p>
                <p>
                    <b class="ms-4 me-3">• Vulkan: </b>
                    {$installInfo.vulkanNvidia ? "Nvidia; " : ""}
                    {$installInfo.vulkanIntel ? "Intel; " : ""}
                    {$installInfo.vulkanAmd ? "AMD; " : ""}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="ms-4 me-3">• {getString($installInfo.language, "install-wine")}</b>
                    {$installInfo.installWine ? "✓" : "x"}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="ms-4 me-3">• {getString($installInfo.language, "install-winetricks")}</b>
                    {$installInfo.installWinetricks ? "✓" : "x"}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="ms-4 me-3">• {getString($installInfo.language, "install-gnome-disks")}</b>
                    {$installInfo.installGnomeDisks ? "✓" : "x"}
                </p>
            </div>

            <div class="mt-3">
                <p>
                    <b class="ms-4 me-3">• {getString($installInfo.language, "install-intel-media")}</b>
                    {$installInfo.installIntelMedia ? "✓" : "x"}
                </p>
            </div>
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => {
            $installationPage = $installationPage - 1;
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on:click={async() => {
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

            const result = await Swal.fire({
                title: getString($installInfo.language, "summary-install-popup-title"),
                text: getString($installInfo.language, "summary-install-popup-body"),
                icon: 'question',
                background: '#222',
                color: 'white',
                confirmButtonColor: '#333',
                showCancelButton: true,
                showConfirmButton: true,
                cancelButtonText: getString($installInfo.language, "summary-install-popup-no"),
                confirmButtonText: getString($installInfo.language, "summary-install-popup-yes"),

            });

            if (result.isConfirmed) {
                goto("/install");
            }

        }}>
            { getString($installInfo.language, "install") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>