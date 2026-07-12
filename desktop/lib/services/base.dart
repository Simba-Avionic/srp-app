String get apiBaseUrl {
  const env = String.fromEnvironment('BASE_URL', defaultValue: 'http://localhost:5000');
  if (env.isEmpty) {
    return Uri.base.origin;
  }
  return env;
}

String apiUrl(String path) {
  final normalizedPath = path.startsWith('/') ? path : '/$path';
  return '$apiBaseUrl$normalizedPath';
}