import 'dart:io';
import 'package:flutter/material.dart';
import 'package:csv/csv.dart';

class CsvDataScreen extends StatelessWidget {
  final List<List<dynamic>> csvRows;

  const CsvDataScreen({super.key, required this.csvRows});

  @override
  Widget build(BuildContext context) {
    List<String> headers = [];
    List<List<dynamic>> data = [];

    if (csvRows.isNotEmpty) {
      headers = List<String>.from(csvRows[0]);
      data = csvRows.skip(1).toList();
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('CSV Data'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Container(
          color: Colors.white,
          child: Column(
            children: [
              const SizedBox(height: 10),
              if (csvRows.isEmpty)
                const Center(child: Text("No data available in the CSV file."))
              else
                Expanded(
                  child: CustomScrollView(
                    slivers: [
                      SliverPersistentHeader(
                        pinned: true,
                        delegate: _StickyHeaderDelegate(
                          headers: headers,
                        ),
                      ),
                      SliverList(
                        delegate: SliverChildBuilderDelegate(
                              (context, index) {
                            return _buildDataRow(data[index]);
                          },
                          childCount: data.length,
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDataRow(List<dynamic> row) {
    return Container(
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Colors.black.withOpacity(0.1)),
        ),
      ),
      child: Row(
        children: row.map((cell) {
          return Expanded(
            child: Container(
              padding: const EdgeInsets.all(8.0),
              decoration: BoxDecoration(
                border: Border(
                  right: BorderSide(color: Colors.black.withOpacity(0.1)),
                ),
              ),
              child: Text(
                cell.toString(),
                style: const TextStyle(fontSize: 14),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}

class _StickyHeaderDelegate extends SliverPersistentHeaderDelegate {
  final List<String> headers;

  _StickyHeaderDelegate({required this.headers});

  @override
  double get maxExtent => 60.0;

  @override
  double get minExtent => 60.0;

  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    return Container(
      color: Theme.of(context).primaryColor,
      child: Row(
        children: headers.map((header) {
          return Expanded(
            child: Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.all(8.0),
              decoration: BoxDecoration(
                border: Border(
                  right: BorderSide(color: Colors.black.withOpacity(0.1)),
                ),
              ),
              child: Text(
                header,
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  @override
  bool shouldRebuild(covariant SliverPersistentHeaderDelegate oldDelegate) {
    return false;
  }
}
