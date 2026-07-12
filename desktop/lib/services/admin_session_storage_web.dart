// ignore: avoid_web_libraries_in_flutter
import 'dart:html';

const _sessionKey = 'srp_admin_session';

bool loadStoredSession() {
  return window.sessionStorage[_sessionKey] == 'true';
}

void storeSession(bool authenticated) {
  if (authenticated) {
    window.sessionStorage[_sessionKey] = 'true';
  } else {
    window.sessionStorage.remove(_sessionKey);
  }
}
