import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

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
            onTap: () {},
          ),
          const SizedBox(height: 10),
          ListTile(
            leading: const Icon(Icons.file_open, color: Colors.white),
            title: const Text('data1.csv', style: TextStyle(color: Colors.white)),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.file_open, color: Colors.white),
            title: const Text('data2.csv', style: TextStyle(color: Colors.white)),
            onTap: () {},
          ),
        ],
      ),
    );
  }
}