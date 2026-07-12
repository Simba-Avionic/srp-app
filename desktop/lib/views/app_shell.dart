import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:desktop/services/admin_session.dart';
import 'package:desktop/services/base.dart';
import 'package:desktop/views/home.dart';
import 'package:desktop/widgets/sidebar_widget.dart';

class AppShell extends StatefulWidget {
  final bool readOnly;

  const AppShell({
    super.key,
    required this.readOnly,
  });

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  bool isSaving = false;

  @override
  void initState() {
    super.initState();
    if (!widget.readOnly) {
      _syncSaveStatus();
    }
  }

  Future<void> _syncSaveStatus() async {
    try {
      final response = await http.get(Uri.parse(apiUrl('/save/status')));
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        if (mounted) {
          setState(() {
            isSaving = data['collecting'] == true || data['task_running'] == true;
          });
        }
      }
    } catch (_) {}
  }

  Future<void> toggleSaving() async {
    if (isSaving) {
      final confirmStop = await showDialog<bool>(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: const Text('Zatrzymać zapis danych?'),
            content: const Text('Czy na pewno chcesz zatrzymać zapis danych?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: const Text('Tak', style: TextStyle(color: Colors.red)),
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: const Text('Nie', style: TextStyle(color: Colors.green)),
              ),
            ],
          );
        },
      );

      if (confirmStop != true) {
        return;
      }

      try {
        final response = await http.post(
          Uri.parse(apiUrl('/save/stop')),
          headers: {'Content-Type': 'application/json'},
          body: json.encode({}),
        );
        if (response.statusCode == 200) {
          setState(() => isSaving = false);
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Błąd zatrzymywania zapisu: $e')),
          );
        }
      }
      return;
    }

    try {
      final response = await http.post(
        Uri.parse(apiUrl('/save/start')),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({}),
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        final status = data['status'] as String? ?? '';
        setState(() {
          isSaving = status == 'Started collecting data' ||
              status == 'Already collecting data';
        });
        if (mounted && status == 'Already collecting data') {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Zapis już trwa w tle')),
          );
        }
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Błąd uruchamiania zapisu (${response.statusCode}): ${response.body}',
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Błąd uruchamiania zapisu: $e')),
        );
      }
    }
  }

  void _logout() {
    AdminSession.logout();
    Navigator.of(context).pushReplacementNamed('/');
  }

  @override
  Widget build(BuildContext context) {
    final isAdmin = !widget.readOnly;

    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Padding(
            padding: const EdgeInsets.only(left: 250),
            child: Text(
              isAdmin ? 'SRP-APP (Admin)' : 'SRP-APP (Podgląd)',
              style: const TextStyle(color: Colors.white, fontSize: 24),
            ),
          ),
        ),
        actions: [
          if (isAdmin)
            IconButton(
              tooltip: 'Wyloguj',
              onPressed: _logout,
              icon: const Icon(Icons.logout),
            )
          else
            IconButton(
              tooltip: 'Logowanie admina',
              onPressed: () => Navigator.of(context).pushNamed('/admin'),
              icon: const Icon(Icons.admin_panel_settings),
            ),
        ],
      ),
      body: SizedBox(
        width: MediaQuery.of(context).size.width,
        child: Row(
          children: [
            SizedBox(
              width: 250,
              child: Sidebar(readOnly: widget.readOnly),
            ),
            Expanded(
              child: Align(
                alignment: Alignment.topCenter,
                child: SingleChildScrollView(
                  child: Home(readOnly: widget.readOnly),
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: isAdmin
          ? FloatingActionButton.extended(
              onPressed: toggleSaving,
              label: Text(
                isSaving ? 'Zatrzymaj zapis' : 'Zapisz dane',
                style: const TextStyle(color: Colors.white),
              ),
              icon: Icon(
                isSaving ? Icons.stop : Icons.save,
                color: Colors.white,
              ),
              backgroundColor: Theme.of(context).colorScheme.secondary,
            )
          : null,
    );
  }
}
