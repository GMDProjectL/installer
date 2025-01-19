<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput,
        getDrives,
        installInfo,
        bytesToReadable,
        getPartitions
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { onMount, tick } from "svelte";


    const bugfixCheckbox = async() => {
        await tick();
        if ($installInfo.enableMultilibRepo == false) {
            $installInfo.installSteam = false;
            $installInfo.installWine = false;
            $installInfo.installWinetricks = false;
        }
    }


    $: canGoFurther = !(
        $installInfo.installSteam == true && !(
            $installInfo.vulkanIntel ||
            $installInfo.vulkanNvidia ||
            $installInfo.vulkanAmd
        )
    );

    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="mdi:magic" width="40" height="40" />
            { getString($installInfo.language, "additional-software") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-start items-center flex-col px-20 w-full gap-10 h-screen">
        <div class="w-auto flex flex-col gap-5 overflow-y-auto p-2 outline-none pt-16" style="height: 70vh;">
            <div class="flex items-center gap-5">
                <input id="multilib" class="invert grayscale scale-150" type="checkbox" 
                    bind:checked={$installInfo.enableMultilibRepo} />
                <label for="multilib" class="flex items-center gap-4">
                    { getString($installInfo.language, "enable-multilib-repo") }
                    <Icon icon="mdi:magic" />
                </label>
            </div>

            <div class={!$installInfo.enableMultilibRepo 
                ? "opacity-50 pointer-events-none"
                : ""}>
                <div class="flex items-center gap-5">
                    <input id="steam" class="invert grayscale scale-150" type="checkbox" 
                        bind:checked={$installInfo.installSteam}
                        />
                    <label for="steam" class="flex items-center gap-4">
                        { getString($installInfo.language, "install-steam") }
                        <Icon icon="mdi:steam" />
                    </label>
                </div>

                <div class={"ml-9 mt-5" + (!$installInfo.installSteam 
                    ? " opacity-50 pointer-events-none"
                    : "")}>
                    <div class="flex items-center gap-5 mt-5">
                        <input id="intel" class="invert grayscale scale-150" type="checkbox" 
                            bind:checked={$installInfo.vulkanIntel}
                            />
                        <label for="intel" class="flex items-center gap-4">
                            HD / UHD / Iris / Arc Graphics
                            <Icon icon="lineicons:intel" width="40" height="40" />
                        </label>
                    </div>
                    <div class="flex items-center gap-5 mt-5">
                        <input id="nvidia" class="invert grayscale scale-150" type="checkbox" 
                            bind:checked={$installInfo.vulkanNvidia}
                            />
                        <label for="nvidia" class="flex items-center gap-4">
                            NVIDIA
                            <Icon icon="lineicons:nvidia" width="30" height="30" />
                        </label>
                    </div>
                    <div class="flex items-center gap-5 mt-6">
                        <input id="amd" class="invert grayscale scale-150" type="checkbox" 
                            bind:checked={$installInfo.vulkanAmd}
                            />
                        <label for="amd" class="flex items-center gap-4">
                            AMD
                            <Icon icon="bi:amd" class="ms-1 me-3" />
                        </label>
                    </div>
                </div>

                <div class="flex items-center gap-5 mt-9">
                    <input id="wine" class="invert grayscale scale-150" type="checkbox" 
                        bind:checked={$installInfo.installWine} 
                        />
                    <label for="wine" class="flex items-center gap-4">
                        { getString($installInfo.language, "install-wine") }
                        <Icon icon="file-icons:wine" />
                    </label>
                </div>

                <div class={
                    "flex items-center gap-5 ml-9 mt-5"
                    + (!$installInfo.installWine
                        ? " opacity-50 pointer-events-none"
                        : "")
                }>
                    <input id="winetricks" class="invert grayscale scale-150" type="checkbox" 
                        bind:checked={$installInfo.installWinetricks} 
                        />
                    <label for="winetricks" class="flex items-center gap-4">
                        { getString($installInfo.language, "install-winetricks") }
                        <Icon icon="streamline:magic-wand-2-solid" />
                    </label>
                </div>
            </div>

            <div class="flex items-center gap-5 mt-5">
                <input id="gnome-disks" class="invert grayscale scale-150" type="checkbox" 
                    bind:checked={$installInfo.installGnomeDisks} 
                    />
                <label for="gnome-disks" class="flex items-center gap-4">
                    { getString($installInfo.language, "install-gnome-disks") }
                    <Icon icon="fluent:hard-drive-16-filled" />
                </label>
            </div>

            <div class="flex items-center gap-5">
                <input id="im" class="invert grayscale scale-150" type="checkbox" 
                    bind:checked={$installInfo.installIntelMedia} 
                    />
                <label for="im" class="flex items-center gap-4">
                    { getString($installInfo.language, "install-intel-media") }
                    <Icon icon="ion:hardware-chip-sharp" />
                </label>
            </div>

            <div class="flex items-center gap-5">
                <input id="bt" class="invert grayscale scale-150" type="checkbox" 
                    bind:checked={$installInfo.setupBluetooth} 
                    />
                <label for="bt" class="flex items-center gap-4">
                    { getString($installInfo.language, "setup-bluetooth") }
                    <Icon icon="material-symbols:bluetooth" />
                </label>
            </div>
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => history.back()}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on:click={() => {
            if ($installInfo.installSteam) {
                if (!canGoFurther) {
                    Swal.fire({
                        title: getString($installInfo.language, "introduce-error"),
                        text: getString($installInfo.language, "at-least-one-vulkan-backend"),
                        icon: 'error',
                        background: '#222',
                        color: 'white',
                        confirmButtonColor: '#333',
                        timer: 3000
                    });
                    return;
                }
            }
            goto("/partitioning");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>