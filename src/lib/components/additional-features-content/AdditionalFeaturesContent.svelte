<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        installInfo,
        installationPage
    } from "$lib";

    let { children } = $props();
    
</script>

<div class="flex justify-start items-center flex-col px-20 w-full gap-10 h-screen">
    <div class="w-auto flex flex-col gap-5 overflow-y-auto p-2 outline-none pt-16" style="height: 70vh;">
        {@render children()}
        <div class="flex items-center gap-5">
            <input id="doOsProber" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.doOsProber} />
            <label for="doOsProber" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "detect-other-os") }
                <Icon icon="icomoon-free:windows" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="multilib" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.enableMultilibRepo} />
            <label for="multilib" class="flex items-center gap-4 no-select">
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
                <label for="steam" class="flex items-center gap-4 no-select">
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
                    <label for="intel" class="flex items-center gap-4 no-select">
                        HD / UHD / Iris / Arc Graphics
                        <Icon icon="lineicons:intel" width="40" height="40" />
                    </label>
                </div>
                <div class="flex items-center gap-5 mt-5">
                    <input id="nvidia" class="invert grayscale scale-150" type="checkbox" 
                        bind:checked={$installInfo.vulkanNvidia}
                        />
                    <label for="nvidia" class="flex items-center gap-4 no-select">
                        NVIDIA
                        <Icon icon="lineicons:nvidia" width="30" height="30" />
                    </label>
                </div>
                <div class="flex items-center gap-5 mt-6">
                    <input id="amd" class="invert grayscale scale-150" type="checkbox" 
                        bind:checked={$installInfo.vulkanAmd}
                        />
                    <label for="amd" class="flex items-center gap-4 no-select">
                        AMD
                        <Icon icon="bi:amd" class="ms-1 me-3" />
                    </label>
                </div>
            </div>
            <div class="flex items-center gap-5 mt-9">
                <input id="wine" class="invert grayscale scale-150" type="checkbox" 
                    bind:checked={$installInfo.installWine} 
                    />
                <label for="wine" class="flex items-center gap-4 no-select">
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
                <label for="winetricks" class="flex items-center gap-4 no-select">
                    { getString($installInfo.language, "install-winetricks") }
                    <Icon icon="streamline:magic-wand-2-solid" />
                </label>
            </div>
        </div>
        <div class="flex items-center gap-5 mt-5">
            <input id="gnome-disks" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.installGnomeDisks} 
                />
            <label for="gnome-disks" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "install-gnome-disks") }
                <Icon icon="fluent:hard-drive-16-filled" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="im" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.installIntelMedia} 
                />
            <label for="im" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "install-intel-media") }
                <Icon icon="ion:hardware-chip-sharp" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="cosk" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.setupCachyosKernel} 
                />
            <label for="cosk" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "setup-cachyos-kernel") }
                <Icon icon="uil:linux" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="ruref" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.runRussianReflector} 
                />
            <label for="ruref" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "range-russian-mirrors") }
                <Icon icon="material-symbols:cloud" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="lact" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.installLact} 
                />
            <label for="lact" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "install-lact") }
                <Icon icon="mdi:gpu" />
            </label>
        </div>
        <div class="flex items-center gap-5">
            <input id="bt" class="invert grayscale scale-150" type="checkbox" 
                bind:checked={$installInfo.setupBluetooth} 
                />
            <label for="bt" class="flex items-center gap-4 no-select">
                { getString($installInfo.language, "setup-bluetooth") }
                <Icon icon="material-symbols:bluetooth" />
            </label>
        </div>
    </div>
</div>