import 'package:flutter/material.dart';
import 'package:desktop/config/admin_config.dart';
import 'package:desktop/services/admin_session.dart';
import 'package:desktop/views/app_shell.dart';

class AdminLoginPage extends StatefulWidget {
  const AdminLoginPage({super.key});

  @override
  State<AdminLoginPage> createState() => _AdminLoginPageState();
}

class _AdminLoginPageState extends State<AdminLoginPage> {
  final _passwordController = TextEditingController();
  String? _errorMessage;
  bool _obscurePassword = true;
  bool _loading = true;

  static const _cardColor = Color(0xFFF8FAFC);
  static const _titleColor = Color(0xFF111827);
  static const _subtitleColor = Color(0xFF4B5563);
  static const _accentColor = Color(0xFF2563EB);

  @override
  void initState() {
    super.initState();
    _loadConfig();
  }

  Future<void> _loadConfig() async {
    await AdminConfig.load();
    if (mounted) {
      setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    await AdminConfig.load();
    if (_passwordController.text == AdminConfig.password) {
      AdminSession.authenticate();
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => const AppShell(readOnly: false),
        ),
      );
      return;
    }

    setState(() {
      _errorMessage = 'Nieprawidłowe hasło';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('SRP-APP — logowanie admina'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pushReplacementNamed('/'),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 420),
          child: Card(
            color: _cardColor,
            elevation: 4,
            shadowColor: Colors.black26,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
              side: const BorderSide(color: Color(0xFFE5E7EB)),
            ),
            margin: const EdgeInsets.all(24),
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(
                    Icons.admin_panel_settings,
                    size: 48,
                    color: _accentColor,
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Tryb administratora',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: _titleColor,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Dostęp do sterowania i zapisu danych wymaga hasła.',
                    style: TextStyle(
                      color: _subtitleColor,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 24),
                  if (_loading)
                    const Center(child: CircularProgressIndicator())
                  else ...[
                  TextField(
                    controller: _passwordController,
                    obscureText: _obscurePassword,
                    autofocus: true,
                    style: const TextStyle(color: _titleColor),
                    decoration: InputDecoration(
                      labelText: 'Hasło',
                      labelStyle: const TextStyle(color: _subtitleColor),
                      errorText: _errorMessage,
                      filled: true,
                      fillColor: Colors.white,
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility
                              : Icons.visibility_off,
                          color: _subtitleColor,
                        ),
                        onPressed: () {
                          setState(() {
                            _obscurePassword = !_obscurePassword;
                          });
                        },
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(color: Color(0xFFD1D5DB)),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(color: Color(0xFFD1D5DB)),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: _accentColor,
                          width: 2,
                        ),
                      ),
                    ),
                    onSubmitted: (_) => _submit(),
                  ),
                  const SizedBox(height: 24),
                  FilledButton(
                    onPressed: _submit,
                    style: FilledButton.styleFrom(
                      backgroundColor: _accentColor,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                    child: const Text(
                      'Zaloguj',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () =>
                        Navigator.of(context).pushReplacementNamed('/'),
                    style: TextButton.styleFrom(
                      foregroundColor: _subtitleColor,
                    ),
                    child: const Text('Wróć do podglądu'),
                  ),
                  ],
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
