<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
        installInfo,
        installationPage, AdditionalFeaturesContent
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";

    installationPage.set(4);

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

    <AdditionalFeaturesContent>
        <div></div>
    </AdditionalFeaturesContent>

    <SetupPageBottom>
        <GDLButton on:click={() => {
            history.back();
        }}>
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