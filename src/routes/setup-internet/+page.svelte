<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, installInfo,
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
    } from "$lib";
    import { goto } from "$app/navigation";
    import { onMount, onDestroy } from "svelte";
    import { get } from "svelte/store";
    import Swal from "sweetalert2";
    import { 
        getInternetDevices, activateConnection,
        getActiveConnectionState, updateStatus,
        disconnectDevice, deleteConnection
    } from "$lib/api"
    import { 
        currentInternetDevice, 
        doSkippedInternetSetup, 
        internetDevices 
    } from "$lib"

    let expandedSSIDorUUID: string | null = null;
    let accessPoints: Array<Record<string, any>> = [];
    let deactivatedButtons: Array<string> = [];
    let savedSSID: Array<Record<string, any>> = [];
    let savedSSIDNames: Array<string> = [];
    let updateID: NodeJS.Timeout | undefined = undefined;
    let hasInternet: boolean = false;
    let connectedTo: Record<string, any> | undefined = undefined;
    let enteredPasswords: Record<string, string> = {};

    onMount(async () => {
        doOpenRoutine();
    });

    onDestroy(async () => {
        toggleUpdate();
    });

    $: {
        if (!$doSkippedInternetSetup && hasInternet) {
            setTimeout(() => {
                goto("/introduce-yourself");
            }, 200)
            $doSkippedInternetSetup = true;
        }
    }

    const doOpenRoutine = async () => {
        const data = await getInternetDevices()
        internetDevices.set(data);

        if ($currentInternetDevice === undefined)
            currentInternetDevice.set(data[0]);

        toggleUpdate();
    };

    const onDeviceChange = (e: Event) => {
        const devices = get(internetDevices);
        currentInternetDevice.set(devices.find(v => v?.location === (e.target as HTMLOptionElement).value));

        toggleUpdate();
        toggleUpdate();
    };

    const toggleUpdate = (disableScanning: boolean = false) => {
        if (updateID !== undefined) {
            clearInterval(updateID);
            updateID = undefined;
        } else {
            updateID = setInterval(async () => {
                let wireless = get(currentInternetDevice)?.wireless === true;
                const result = await updateStatus(true, wireless, wireless && disableScanning === false, wireless, get(currentInternetDevice)?.location);

                hasInternet = result?.connectivity === 4;

                if (wireless === true) {
                    connectedTo = {
                        uuid: result?.applied_connection?.uuid,
                        active_loc: result?.applied_connection?.active_loc
                    };

                    savedSSID = []
                    savedSSIDNames = []

                    for (const connection of result?.saved_connections) {
                        if (connection?.connection?.type === "802-11-wireless") {
                            savedSSID.push(connection?.connection)
                            savedSSIDNames.push(connection?.connection?.id)
                        }
                    }

                    if (disableScanning === false) {
                        accessPoints = result?.access_points;
                    }
                }
            }, 500);
        }
    };

    const connectionButtonValidator = (flags: number, SSID: string): boolean => {
        if (flags != 0 && enteredPasswords[SSID]?.length >= 8 && !deactivatedButtons.includes(SSID)) {
            return true;
        } else if (flags == 0 && !deactivatedButtons.includes(SSID)) {
            return true;
        }

        return false;
    };

    const toggleExpand = (UUIDorSSID: string) => {
        if (expandedSSIDorUUID === UUIDorSSID) {
            delete enteredPasswords[UUIDorSSID];
            toggleUpdate();
            toggleUpdate();
        } else {
            toggleUpdate();
            toggleUpdate(true);
        }
        expandedSSIDorUUID = expandedSSIDorUUID === UUIDorSSID ? null : UUIDorSSID;
    };
</script>

<SetupPage>
    <SetupPageTitle>
        { getString($installInfo.language, "internet-text") }
    </SetupPageTitle>

    <div class="flex h-full justify-between items-start flex-col px-20 py-10 w-full gap-10 overflow-y-hidden">
        <div class="w-full h-full flex flex-col flex-grow items-start gap-5 p-2">
            {#if ($internetDevices.length > 1)}
                <select class="bg-zinc-800 outline-0 p-4 rounded-md mt-2 w-full no-select"
                    on:click={async () => {
                        $internetDevices = await getInternetDevices();
                    }}
                    on:change={async (e: Event) => {
                        await onDeviceChange(e);
                    }}>
                    {#each $internetDevices as device}
                        <option selected={$currentInternetDevice !== undefined && $currentInternetDevice.location == device.location} value={device.location}>
                            {device.hardware_name + ` (${device.interface})`}
                        </option>
                    {/each}
                </select>
            {/if}
            {#if ($currentInternetDevice && "wireless" in $currentInternetDevice && $currentInternetDevice.wireless)}
                {#if accessPoints.length === 0}
                <div class="w-full h-full flex flex-row justify-center items-center gap-2 p-2">
                    {#each Array(3) as _}
                        <i class="text-4xl loading no-select">•</i>
                    {/each}
                </div>
                {:else}
                <div class="w-full flex flex-col flex-grow items-start gap-3 overflow-y-auto p-2">
                    {#each savedSSID as savedConnection}
                        <button class={"smooth-transition flex flex-col gap-2 w-full no-select p-3 rounded-md items-start" + (expandedSSIDorUUID === savedConnection?.uuid ? " bg-zinc-800" : " hover:bg-zinc-800")}
                        on:click={() => { toggleExpand(savedConnection?.uuid); }}>
                            <div class="w-full flex flex-rows gap-1 items-center no-select">
                                {savedConnection?.id}
                                {#if (connectedTo?.uuid === savedConnection?.uuid)}
                                    <Icon icon="material-symbols:check" width="20" height="20"/>
                                {/if}
                            </div>
                            {#if expandedSSIDorUUID === savedConnection?.uuid}
                            <div class="w-full flex flex-rows flex-row-reverse justify-start items-center gap-3">
                                {#if (connectedTo?.uuid === savedConnection?.uuid)}
                                    <span role="button" tabindex="0" class={"smooth-transition no-select p-2 px-4 rounded-md bg-zinc-700" + (deactivatedButtons.includes(savedConnection?.uuid) ? " opacity-50" : " hover:bg-zinc-600 active:bg-zinc-800")}
                                    on:click|stopPropagation={async () => {
                                        if (deactivatedButtons.includes(savedConnection?.uuid))
                                            return;
                                        
                                        deactivatedButtons.push(savedConnection?.uuid)

                                        disconnectDevice($currentInternetDevice?.location);

                                        const interval = setInterval(() => {
                                            console.log(connectedTo?.uuid)
                                            if (connectedTo?.uuid === savedConnection?.uuid)
                                                return;

                                            deactivatedButtons = deactivatedButtons.filter(v => v !== savedConnection?.uuid)
                                            clearInterval(interval)
                                        }, 50);
                                    }}
                                    on:keydown={() => {}}>
                                        {getString($installInfo.language, "disconnect")}
                                    </span>
                                {:else}
                                    <span role="button" tabindex="0" class={"smooth-transition no-select p-2 px-4 rounded-md bg-zinc-700" + (deactivatedButtons.includes(savedConnection?.uuid) ? " opacity-50" : " hover:bg-zinc-600 active:bg-zinc-800")}
                                    on:click|stopPropagation={async () => {
                                        if (deactivatedButtons.includes(savedConnection?.uuid))
                                            return;
                                        
                                        deactivatedButtons.push(savedConnection?.uuid)

                                        console.log(savedConnection)

                                        const active_connection = await activateConnection(
                                            savedConnection?.location, 
                                            '/', 
                                            $currentInternetDevice?.location
                                        );

                                        const interval = setInterval(async () => {
                                            if (await getActiveConnectionState(active_connection) == 2) {
                                                deactivatedButtons = deactivatedButtons.filter(v => v !== savedConnection?.uuid);
                                                clearInterval(interval);
                                            }
                                        }, 50);
                                    }}
                                    on:keydown={() => {}}>
                                        {getString($installInfo.language, "connect")}
                                    </span>
                                {/if}
                                <span role="button" tabindex="0" class="smooth-transition no-select p-2 px-4 rounded-md bg-zinc-700 hover:bg-zinc-600 active:bg-zinc-800"
                                on:click|stopPropagation={async () => {
                                    await deleteConnection(savedConnection?.location);
                                }}
                                on:keydown={() => {}}>
                                    {getString($installInfo.language, "delete")}
                                </span>
                            </div>
                            {/if}
                        </button>
                    {/each}
                    {#each accessPoints as ap}
                        {#if (!savedSSIDNames.includes(ap?.decodedSSID))}
                        <button class={"smooth-transition flex flex-col gap-3 w-full no-select p-3 rounded-md items-start" + (expandedSSIDorUUID === ap?.Ssid ? " bg-zinc-800" : " hover:bg-zinc-800")}
                        on:click={() => {
                            toggleExpand(ap.Ssid)
                        }}>
                            <div class="w-full flex flex-rows gap-1 items-center no-select">
                                {ap?.decodedSSID}
                                {#if ap?.Flags != 0}
                                    <Icon icon="material-symbols:lock" width="15" height="15" />
                                {/if}
                            </div>
                            {#if (expandedSSIDorUUID === ap?.Ssid)}
                            <div class="w-full flex flex-rows flex-row justify-end items-center gap-3">
                                {#if ap?.Flags !== 0}
                                <input type="password" on:click|stopPropagation bind:value={enteredPasswords[ap.Ssid]} placeholder={getString($installInfo.language, "password-tip")} class="w-full bg-zinc-700 p-2 rounded-md focus:outline-none" />
                                {/if}
                                <span role="button" tabindex="0" class={"smooth-transition no-select p-2 px-4 rounded-md bg-zinc-700" + (!connectionButtonValidator(ap?.Flags, ap?.Ssid) ? " opacity-50" : " hover:bg-zinc-600 active:bg-zinc-800")}
                                on:click|stopPropagation={async () => {
                                    if (!connectionButtonValidator(ap?.Flags, ap?.Ssid))
                                        return;

                                    
                                }}
                                on:keydown={() => {}}>
                                    {getString($installInfo.language, "connect")}
                                </span>
                            </div>
                            {/if}
                        </button>
                        {/if}
                    {/each}
                </div>
                {/if}
            {:else if ($currentInternetDevice && "wireless" in $currentInternetDevice && !$currentInternetDevice.wireless)}
                <div class="w-full h-full justify-center flex flex-col items-center">
                    <div class="w-full h-full justify-center flex flex-row items-center gap-4">
                        <Icon icon="material-symbols:lan" width="30" height="30"/>
                        <h2 class="no-select text-2xl">{getString($installInfo.language, "ethernet-tip")}</h2>
                    </div>
                </div>
            {/if}
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on_click={() => {
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!hasInternet}
        on_click={() => {
            if (!hasInternet) {
                Swal.fire({
                    title: getString($installInfo.language, "introduce-error"),
                    text: getString($installInfo.language, "no-internet-explanation"),
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

            goto("/introduce-yourself"); 
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>

<style>
    .smooth-transition {
        transition-duration: 300ms;
    }

    .loading {
        animation: loading-anim 1s ease-in-out infinite alternate both;
        will-change: transform;
    }

    .loading:nth-child(1) {
        animation-delay: 0s;
    }

    .loading:nth-child(2) {
        animation-delay: 0.3s;
    }

    .loading:nth-child(3) {
        animation-delay: 0.5s;
    }

    @keyframes loading-anim {
        from {
            transform: translateY(10px);
        }

        to {
            transform: translateY(-10px);
        }
    }
</style>