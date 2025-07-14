<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput,
        installInfo, installationPage
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";

    installationPage.set(2);

    $: canGoFurther = !(
        $installInfo.username == "" ||
        $installInfo.computerName == "" ||
        $installInfo.password == "" ||
        $installInfo.password2 == "");

    $: passwordMismatch = !(
        $installInfo.password == $installInfo.password2);
        
    const next = () => {
        if (!canGoFurther) {
            Swal.fire({
                title: getString($installInfo.language, "introduce-error"),
                text: getString($installInfo.language, "introduce-error-explaination"),
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
        } else if (passwordMismatch) {
            Swal.fire({
                title: getString($installInfo.language, "introduce-error"),
                text: getString($installInfo.language, "password-mismatch-explanation"),
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
        goto("/location");
    }
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="ic:baseline-account-circle" width="40" height="40" />
            { getString($installInfo.language, "introduce-yourself") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-between items-center flex-col px-20 w-full gap-10">
        <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
        <form on:keypress={(e) => {
            if (e.key == "Enter") {
                next();
            }
        }} class="w-96 flex flex-col gap-5 overflow-y-auto p-2">
            <div>
                <span class="flex gap-2 no-select">
                    <Icon icon="material-symbols-light:person-outline-rounded" width="24" height="24" />
                    { getString($installInfo.language, "username") }:
                </span>
                <GDLInput bind:value={$installInfo.username} inputType="text" placeholder="relative" />
            </div>
            <div>
                <span class="flex gap-2 no-select">
                    <Icon icon="mdi-light:monitor" width="24" height="24" />
                    { getString($installInfo.language, "computer-name") }:
                </span>
                <GDLInput bind:value={$installInfo.computerName} inputType="text" placeholder="relatives-pc" />
            </div>
            <div>
                <span class="flex gap-2 no-select">
                    <Icon icon="mdi:password" width="24" height="24" />
                    { getString($installInfo.language, "password") }:
                </span>
                <GDLInput bind:value={$installInfo.password} inputType="password" placeholder="••••••••••••••••" />
            </div>
            <div>
                <span class="flex gap-2 no-select">
                    <Icon icon="mdi:password" width="24" height="24" />
                    { getString($installInfo.language, "password-2") }:
                </span>
                <GDLInput bind:value={$installInfo.password2} inputType="password" placeholder="••••••••••••••••" />
            </div>
        </form>
    </div>

    <SetupPageBottom>
        <GDLButton on_click={() => {
            history.back();
        }}>
            { getString($installInfo.language, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther || passwordMismatch} on_click={next}>
            { getString($installInfo.language, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>