import 'package:desktop/services/admin_session_storage.dart';

class AdminSession {
  static bool _authenticated = false;
  static bool _initialized = false;

  static void _ensureLoaded() {
    if (_initialized) {
      return;
    }
    _authenticated = loadStoredSession();
    _initialized = true;
  }

  static bool get isAuthenticated {
    _ensureLoaded();
    return _authenticated;
  }

  static void authenticate() {
    _authenticated = true;
    _initialized = true;
    storeSession(true);
  }

  static void logout() {
    _authenticated = false;
    storeSession(false);
  }
}
