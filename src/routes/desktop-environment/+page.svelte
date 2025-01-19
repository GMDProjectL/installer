<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installInfo,
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";
    import { Carousel } from "flowbite-svelte";

    $: canGoFurther = true;
    const des = ["kde", "gnome"];

    $: galleryIndex = des.indexOf($installInfo.de);


</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="mynaui:desktop" width="40" height="40" />
            { getString($installInfo.language, "desktop-environment") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-start items-center flex-col px-20 w-full h-screen">
        <div class="w-full flex justify-center items-center shitinside">
            <Carousel index={galleryIndex} images={[
                {
                    src: '/de/kde.png',
                    title: 'KDE Plasma'
                },
                {
                    src: '/de/gnome.webp',
                    title: 'GNOME'
                }
            ]} />
        </div>
        <div class="w-full flex gap-5 justify-center items-center">
            <GDLButton on:click={() => $installInfo.de = "kde"} secondary={$installInfo.de == "kde"}>
                KDE Plasma ({ getString($installInfo.language, "recommended") })
            </GDLButton>
            <GDLButton on:click={() => $installInfo.de = "gnome"} secondary={$installInfo.de == "gnome"}>
                GNOME
            </GDLButton>
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => history.back()}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on:click={() => {
            goto("/additional-software");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>