class AdminSession {
  static bool _authenticated = false;

  static bool get isAuthenticated => _authenticated;

  static void authenticate() {
    _authenticated = true;
  }

  static void logout() {
    _authenticated = false;
  }
}
