(() => {
  const dom = {
    chatkitHost: document.getElementById("chatkit-host"),
  };

  async function waitForElementDef(elementName, timeoutMs) {
    await Promise.race([
      customElements.whenDefined(elementName),
      new Promise((_, reject) => {
        window.setTimeout(() => {
          reject(new Error(`${elementName} was not defined before timeout`));
        }, timeoutMs);
      }),
    ]);
  }

  function addEventListeners(chatkitElement) {
    chatkitElement.addEventListener("chatkit.ready", () => {
      console.log("ChatKit ready event");
    });

    chatkitElement.addEventListener("chatkit.thread.change", (event) => {
      const threadId = event.detail?.threadId ?? null;
      console.log("ChatKit thread change event", threadId);
    });

    chatkitElement.addEventListener("chatkit.response.end", () => {
      console.log("ChatKit response end event");
    });

    chatkitElement.addEventListener("chatkit.error", (event) => {
      console.error("ChatKit error", event.detail?.error || event.detail);
    });
  }

  async function initChatKit() {
    if (!window.customElements) {
      console.error("Browser does not support custom elements");
      return;
    }

    try {
      await waitForElementDef("openai-chatkit", 10000);
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
    addEventListeners(chatkitElement);
  }

  void initChatKit();
})();
