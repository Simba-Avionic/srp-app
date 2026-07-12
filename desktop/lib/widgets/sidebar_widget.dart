import 'dart:io';
import 'package:flutter/material.dart';
import 'package:csv/csv.dart';
import 'package:path/path.dart' as p;

import 'csv_data_screen.dart';

class Sidebar extends StatelessWidget {
  final bool readOnly;

  const Sidebar({
    super.key,
    this.readOnly = true,
  });

  Future<List<List<dynamic>>> getCsvFileContent() async {
    final currentDir = Directory.current.path;
    final filePath = p.join(currentDir, 'desktop', 'data', 'csv', 'data.csv');

    final file = File(filePath);
    if (await file.exists()) {
      final fileContent = await file.readAsString();
      return CsvToListConverter().convert(fileContent);
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
            title: const Text('data.csv', style: TextStyle(color: Colors.white)),
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
        ],
      ),
    );
  }
}
