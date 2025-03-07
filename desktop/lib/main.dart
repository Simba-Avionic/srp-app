import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:desktop/views/home.dart';
import 'package:desktop/widgets/sidebar_widget.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SRP-APP',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: const Color(0xFF1F2937),
        secondaryHeaderColor: Color(0xFF004D40),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF1F2937),
          secondary: Colors.blue,
          surface: Color(0xFF1F2937),
          background: Colors.white,
          onPrimary: Colors.white,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF1F2937),
          elevation: 0,
          iconTheme: IconThemeData(color: Colors.white),
          titleTextStyle: TextStyle(color: Colors.white),
        ),
        drawerTheme: const DrawerThemeData(
          backgroundColor: Color(0xFF1F2937),
        ),
        scaffoldBackgroundColor: Colors.white,
        textTheme: const TextTheme(
          bodyLarge: TextStyle(color: Colors.black87),
          bodyMedium: TextStyle(color: Colors.black87),
        ),
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool isSaving = false;

  void toggleSaving() async {
    if (isSaving) {
      bool? confirmStop = await showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Stop Saving Data?'),
            content: const Text('Are you sure you want to stop saving data?'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop(true);
                },
                child: const Text('Yes', style: TextStyle(color: Colors.red),),
              ),
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop(false);
                },
                child: const Text('No',
                  style: TextStyle(color: Colors.green),),
              ),
            ],
          );
        },
      );

      if (confirmStop == true) {
        final body = {};
        final response = await http.post(
          Uri.parse('http://localhost:5000/save/stop'),
          headers: {
            'Content-Type': 'application/json',
          },
          body: json.encode(body),
        );
        if (response.statusCode == 200) {
          print("Stopped saving data...");
          setState(() {
            isSaving = false;
          });
        } else {
          print("Failed to stop saving data.");
        }
      }
    }
    else{ //if not saving
      final body = {};
      final response = await http.post(
        Uri.parse('http://localhost:5000/save/start'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode(body),
      );
      if (response.statusCode == 200) {
        print("Started saving data...");
        setState(() {
          isSaving = true;
        });
      } else {
        print("Failed to start saving data.");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Center(
          child: Padding(
            padding: EdgeInsets.only(left: 250),
            child: Text(
              'SRP-APP',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
              ),
            ),
          ),
        ),
      ),
      body: SizedBox(
        width: MediaQuery.of(context).size.width,
        child: Row(
          children: const [
            SizedBox(
              width: 250,
              child: Sidebar(),
            ),
            Expanded(
              child: Center(
                child: SingleChildScrollView(
                  child: Home(),
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: toggleSaving,
        label: Text(
          isSaving ? 'Stop Saving' : 'Save Data',
          style: const TextStyle(color: Colors.white),
        ),
        icon: Icon(
          isSaving ? Icons.stop : Icons.save,
          color: Colors.white,
        ),
        backgroundColor: Theme.of(context).colorScheme.secondary,
      ),
    );
  }
}
