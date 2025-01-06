import { get, writable } from "svelte/store";
import { Api } from "./Api";
import type { BasicAuthSecurity } from "./types";
import { addAlert } from "./alert";
import { authenticated } from "./store";


// Create your API instance
export const apiInner = new Api<BasicAuthSecurity>({
    baseUrl: ".",
    // This function receives the "securityData" (our BasicAuthSecurity) 
    // and returns request params that include the Authorization header.
    securityWorker: (securityData) => {
        if (!securityData) {
            // If securityData is not set, don’t add any headers
            return {};
        }

        const authString = btoa(`any:${securityData.password}`);

        return {
            headers: {
                Authorization: `Basic ${authString}`,
            },
        };
    },
});

export const api = apiInner.api;

export const password = writable<string>("");

export function get_password(): string {
    if (get(password) === "") {
        let localpw = localStorage.getItem("password")
        if (localpw) {
            password.set(localpw)
        }
    }
    if (get(password) === "") {
        addAlert("No password set", "error");
    }
    return get(password)
}

export function login() {
    let password = get_password()

    apiInner.setSecurityData({ password: password })

    // Test the credentials
    apiInner.ping.pongPingGet().then((res) => {
        localStorage.setItem("password", password)
        authenticated.set(true);
    }).catch((res) => {
        addAlert(res.error, "error",);
    })
    authenticated.set(false);
}