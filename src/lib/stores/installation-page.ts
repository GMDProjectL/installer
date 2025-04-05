import { writable } from "svelte/store";

let installationPage = writable<number>(0);

export default installationPage;