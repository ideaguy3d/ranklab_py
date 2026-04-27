(() => {
    const dom = {
        chatkitHost: document.getElementById("chatkit-host"),
    };

    async function wait_for_element_def(elementName, timeoutMs) {
        await Promise.race([
            customElements.whenDefined(elementName),
            new Promise((_, reject) => {
                window.setTimeout(() => {
                    reject(new Error(`${elementName} was not defined before timeout`));
                }, timeoutMs);
            }),
        ]);
    }

    function add_event_listeners(chatkitElement) {
        chatkitElement.addEventListener("chatkit.error", (event) => {
            console.error("ChatKit error", event.detail?.error || event.detail);
        });
    }

    async function init_chatkit() {
        if (!window.customElements) {
            console.error("Browser does not support custom elements");
            return;
        }

        try {
            await wait_for_element_def("openai-chatkit", 10000);
        } catch (error) {
            console.error("ChatKit element failed.", error);
            return;
        }

        const chatkitElement = document.createElement("openai-chatkit");
        dom.chatkitHost.appendChild(chatkitElement);

        chatkitElement.setOptions({
            api: {
                url: "/chatkit",
                domainKey: "local-dev",
            },
        });

        dom.chatkitHost.style.display = "block";
        dom.chatkitHost.style.width = "360px";
        dom.chatkitHost.style.height = "600px";
        add_event_listeners(chatkitElement);
    }

    void init_chatkit();
})();

