(() => {
  if (!("serviceWorker" in navigator)) return;

  let hadController = Boolean(navigator.serviceWorker.controller);
  let updateReady = false;
  let reloading = false;
  let lastCheck = 0;

  const applyUpdate = () => {
    if (!updateReady || reloading || document.visibilityState === "hidden") return;
    reloading = true;
    window.location.reload();
  };

  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (!hadController) {
      hadController = true;
      return;
    }
    updateReady = true;
    applyUpdate();
  });

  window.addEventListener("load", async () => {
    try {
      const registration = await navigator.serviceWorker.register("/sw.js", {
        scope: "/",
        updateViaCache: "none",
      });
      const checkForUpdate = () => {
        const now = Date.now();
        if (now - lastCheck < 5 * 60 * 1000) return;
        lastCheck = now;
        registration.update().catch(() => {});
      };

      checkForUpdate();
      document.addEventListener("visibilitychange", () => {
        if (document.visibilityState !== "visible") return;
        applyUpdate();
        checkForUpdate();
      });
      window.addEventListener("pageshow", (event) => {
        if (event.persisted) checkForUpdate();
      });
    } catch (_) {
      // The site remains usable when service workers are unavailable.
    }
  });
})();
