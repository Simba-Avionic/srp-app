import 'package:desktop/views/home.dart';
import 'package:desktop/widgets/sidebar_widget.dart';
import 'package:flutter/material.dart';

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
              width: 250, // Fixed width for Sidebar
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
        onPressed:(){},
        label: const Text('Save Data', style: TextStyle(color: Colors.white)),
        icon: const Icon(Icons.save, color: Colors.white,),
        backgroundColor: Theme.of(context).colorScheme.secondary,
      ),
    );
  }
}
