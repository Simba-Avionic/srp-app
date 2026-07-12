import 'package:flutter/material.dart';
import 'package:desktop/services/admin_session.dart';
import 'package:desktop/views/admin_login_page.dart';
import 'package:desktop/views/app_shell.dart';

void main() {
  runApp(const MyApp());
}

String _initialRoute() {
  final fragment = Uri.base.fragment;
  if (fragment == '/admin' ||
      fragment == 'admin' ||
      fragment.startsWith('/admin')) {
    return '/admin';
  }

  final path = Uri.base.path;
  if (path.endsWith('/admin')) {
    return '/admin';
  }

  return '/';
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
        secondaryHeaderColor: const Color(0xFF004D40),
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
      initialRoute: _initialRoute(),
      onGenerateRoute: (settings) {
        switch (settings.name) {
          case '/admin':
            if (AdminSession.isAuthenticated) {
              return MaterialPageRoute(
                builder: (_) => const AppShell(readOnly: false),
              );
            }
            return MaterialPageRoute(
              builder: (_) => const AdminLoginPage(),
            );
          case '/':
          default:
            if (AdminSession.isAuthenticated) {
              return MaterialPageRoute(
                builder: (_) => const AppShell(readOnly: false),
              );
            }
            return MaterialPageRoute(
              builder: (_) => const AppShell(readOnly: true),
            );
        }
      },
    );
  }
}
