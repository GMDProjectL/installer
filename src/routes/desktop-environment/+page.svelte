<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installInfo, installationPage
    } from "$lib";
    import { goto } from "$app/navigation";
    import { Carousel } from "flowbite-svelte";

    installationPage.set(4);

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
                    title: 'KDE Plasma',
                    alt: 'KDE Plasma is a desktop environment from the KDE community. It\'s very customizable and has a lot of features. Highly recommended for gaming.',
                },
                {
                    src: '/de/gnome.webp',
                    title: 'GNOME',
                    alt: 'GNOME is a desktop environment from the GNOME community. It\'s strict and determined. Highly recommended for productivity.'
                }
            ]} />
        </div>
        <div class="w-full flex gap-5 justify-center items-center">
            <GDLButton on_click={() => $installInfo.de = "kde"} secondary={$installInfo.de == "kde"}>
                KDE Plasma ({ getString($installInfo.language, "recommended") })
            </GDLButton>
            <GDLButton on_click={() => $installInfo.de = "gnome"} secondary={$installInfo.de == "gnome"}>
                GNOME
            </GDLButton>
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on_click={() => {
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on_click={() => {
            goto("/additional-software");
        }}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>