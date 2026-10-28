/* Single-recording transport shared by the embedded readers. The audio element
 * owns playback; only the most recently played reader owns the OS session. */
(() => {
  let active = null;
  const actions = ['play', 'pause', 'stop', 'seekbackward', 'seekforward', 'seekto', 'previoustrack', 'nexttrack'];
  const session = navigator.mediaSession;
  const setHandler = (action, handler) => {
    try { session?.setActionHandler(action, handler); } catch (_) { /* Unsupported on this platform. */ }
  };

  function attach(audio, options = {}) {
    const listeners = [];
    const duration = () => {
      const value = Number.isFinite(audio.duration) ? audio.duration : options.duration?.();
      return Number.isFinite(value) && value > 0 ? value : 0;
    };
    const position = () => {
      if (active !== owner || !session?.setPositionState) return;
      const length = duration();
      try {
        if (length && audio.playbackRate > 0) session.setPositionState({
          duration: length,
          playbackRate: audio.playbackRate,
          position: Math.max(0, Math.min(length, audio.currentTime)),
        });
        else session.setPositionState();
      } catch (_) { /* Position state is optional. */ }
    };
    const seek = time => {
      const length = duration();
      if (!length || !Number.isFinite(time)) return;
      audio.currentTime = Math.max(0, Math.min(length, time));
      options.onSeek?.();
      position();
    };
    const play = () => {
      options.beforePlay?.();
      audio.play().catch(() => {});
    };
    const claim = () => {
      if (active && active !== owner) active.audio.pause();
      active = owner;
      if (!session) return;
      if (typeof MediaMetadata !== 'undefined') session.metadata = new MediaMetadata(options.metadata || {});
      session.playbackState = 'playing';
      // These readers are one recording, never a playlist.
      setHandler('previoustrack', null);
      setHandler('nexttrack', null);
      setHandler('play', play);
      setHandler('pause', () => audio.pause());
      setHandler('stop', () => { audio.pause(); seek(0); });
      const offset = details => Number.isFinite(details?.seekOffset) && details.seekOffset > 0 ? details.seekOffset : 10;
      setHandler('seekbackward', details => seek(audio.currentTime - offset(details)));
      setHandler('seekforward', details => seek(audio.currentTime + offset(details)));
      setHandler('seekto', details => seek(details.seekTime));
      position();
    };
    const on = (name, callback) => {
      audio.addEventListener(name, callback);
      listeners.push([name, callback]);
    };
    const owner = {audio, release() {
      audio.pause();
      if (active !== owner) return;
      active = null;
      if (!session) return;
      for (const action of actions) setHandler(action, null);
      session.metadata = null;
      session.playbackState = 'none';
      try { session.setPositionState?.(); } catch (_) {}
    }, dispose() {
      for (const [name, callback] of listeners) audio.removeEventListener(name, callback);
      owner.release();
    }};
    on('play', claim);
    on('pause', () => { if (session && active === owner) session.playbackState = 'paused'; });
    on('ended', () => { if (session && active === owner) session.playbackState = 'paused'; position(); });
    for (const event of ['loadedmetadata', 'durationchange', 'timeupdate', 'seeked', 'ratechange']) on(event, position);
    if (!audio.paused) claim();
    return owner;
  }
  window.VedantaMediaSession = {attach};
})();
