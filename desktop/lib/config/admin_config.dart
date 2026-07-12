class AdminConfig {
  static const String password = String.fromEnvironment(
    'ADMIN_PASSWORD',
    defaultValue: 'srp-admin',
  );
}
