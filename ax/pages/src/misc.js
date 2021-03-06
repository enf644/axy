let axHost = null;
let axProtocol = null;

export function getAxHost() {
  if (axHost == null) {
    const scripts = document.getElementsByTagName('script');
    const index = scripts.length - 1;
    const myScript = scripts[index];
    const url = new URL(myScript.src);
    axHost = url.host;
    axProtocol = url.protocol;
  }
  return axHost;
}

export function getAxProtocol() {
  if (axProtocol == null) {
    getAxHost();
  }
  if (axProtocol.includes('https')) return 'https';
  return 'http';
}

export function getAxWsProtocol() {
  if (axProtocol == null) {
    getAxHost();
  }
  if (axProtocol.includes('https')) return 'wss';
  return 'ws';
}

export function getAxHostProtocol() {
  const protocol = getAxProtocol();
  const host = getAxHost();
  return `${protocol}://${host}`;
}


export function uuidWithDashes(uuidString) {
  if (!uuidString) return null;
  if (uuidString.includes('-')) return uuidString;
  return `${uuidString.substr(0, 8)}-${uuidString.substr(8, 4)}-${uuidString.substr(12, 4)}-${uuidString.substr(16, 4)}-${uuidString.substr(20)}`;
}

export function debounce(callback, limit) {
  let wait = false;
  return () => {
    if (!wait) {
      callback.call();
      wait = true;
      setTimeout(() => {
        wait = false;
      }, limit);
    }
  };
}

export function isGuid(strGuid) {
  const regexGuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return regexGuid.test(strGuid);
}
