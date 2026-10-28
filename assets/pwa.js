(() => {
  if (!("serviceWorker" in navigator)) return;

  let hadController = Boolean(navigator.serviceWorker.controller);
  let updateReady = false;
  let reloading = false;
  let lastCheck = 0;
  let listeningStarted = false;

  const playing = () => [...document.querySelectorAll("audio, video")]
    .some(media => !media.paused && !media.ended);
  const applyUpdate = () => {
    if (listeningStarted || playing()) return;
    if (!updateReady || reloading || document.visibilityState === "hidden") return;
    reloading = true;
    window.location.reload();
  };

  // A pause is not the end of a listening session. Preserve its seek position
  // through pauses, buffering, and completion; the next launch loads the update.
  // Media events do not bubble, so observe them in capture phase.
  const preserveListeningSession = () => { listeningStarted = true; };
  document.addEventListener("play", preserveListeningSession, true);
  document.addEventListener("seeking", preserveListeningSession, true);

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
