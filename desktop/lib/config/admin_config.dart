import 'dart:convert';
import 'package:http/http.dart' as http;

class AdminConfig {
  static String? _password;
  static bool _loaded = false;

  static Future<void> load() async {
    if (_loaded) {
      return;
    }
    _loaded = true;

    try {
      final response = await http.get(Uri.parse('${Uri.base.origin}/config.json'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        final fromFile = data['adminPassword'];
        if (fromFile is String && fromFile.isNotEmpty) {
          _password = fromFile;
          return;
        }
      }
    } catch (_) {}

    _password = 'srp-admin';
  }

  static String get password => _password ?? 'srp-admin';
}
