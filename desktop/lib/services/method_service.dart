import 'package:http/http.dart' as http;
import 'dart:convert';
import 'base.dart';


class MethodService {
  static Future<Map<String, dynamic>> sendRequest({
    required String namespace,
    required String methodName,
    required String inType,
    String? input,
  }) async {
    final Uri url = Uri.parse(
      '$base_url/${namespace.toLowerCase()}/${methodName.toLowerCase()}',
    );

    final Map<String, dynamic> body = inType != 'void' ? {methodName.toLowerCase(): input} : {};

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode(body),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception('Error: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Request failed: $e');
    }
  }
}
