import 'dart:convert';
import 'package:csv/csv.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:desktop/services/base.dart';
import 'package:desktop/services/csv_download.dart';

import 'csv_data_screen.dart';

class Sidebar extends StatelessWidget {
  final bool readOnly;

  const Sidebar({
    super.key,
    this.readOnly = true,
  });

  Future<List<List<dynamic>>> getCsvFileContent() async {
    try {
      final response = await http.get(Uri.parse(apiUrl('/save/data')));
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        final rows = data['rows'];
        if (rows is List) {
          return rows
              .map((row) => List<dynamic>.from(row as List))
              .toList();
        }
      }
    } catch (e) {
      if (kDebugMode) {
        print('Error loading CSV: $e');
      }
    }
    return [];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 250,
      decoration: BoxDecoration(
        color: Theme.of(context).primaryColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          ListTile(
            leading: Icon(
              readOnly ? Icons.visibility : Icons.admin_panel_settings,
              color: Colors.white,
              size: 35,
            ),
            title: Text(
              readOnly ? 'Podgląd' : 'Admin',
              style: const TextStyle(color: Colors.white, fontSize: 24),
            ),
          ),
          const SizedBox(height: 10),
          ListTile(
            leading: const Icon(Icons.file_open, color: Colors.white),
            title: const Text('Podgląd CSV', style: TextStyle(color: Colors.white)),
            onTap: () async {
              final csvRows = await getCsvFileContent();
              if (!context.mounted) {
                return;
              }
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => CsvDataScreen(csvRows: csvRows),
                ),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.download, color: Colors.white),
            title: const Text('Pobierz CSV', style: TextStyle(color: Colors.white)),
            onTap: () {
              try {
                downloadCsvFile();
              } catch (e) {
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Błąd pobierania: $e')),
                  );
                }
              }
            },
          ),
        ],
      ),
    );
  }
}
