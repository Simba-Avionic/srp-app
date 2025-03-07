import 'dart:io';
import 'package:flutter/material.dart';
import 'package:csv/csv.dart';

import '../views/home.dart';
import 'csv_data_screen.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

  Future<List<List<dynamic>>> getCsvFileContent() async {
    final currentDir = Directory.current.path;
    final filePath = '$currentDir/data/csv/data.csv';

    final file = File(filePath);
    if (await file.exists()) {
      final fileContent = await file.readAsString();
      List<List<dynamic>> rows = CsvToListConverter().convert(fileContent);
      return rows;
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
            leading: const Icon(Icons.home, color: Colors.white, size: 35),
            title: const Text('Home', style: TextStyle(color: Colors.white, fontSize: 24)),
            onTap: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (context) => const Home()),
              );
            },
          ),
          const SizedBox(height: 10),
          ListTile(
            leading: const Icon(Icons.file_open, color: Colors.white),
            title: const Text('data.csv', style: TextStyle(color: Colors.white)),
            onTap: () async {
              final csvRows = await getCsvFileContent();
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
