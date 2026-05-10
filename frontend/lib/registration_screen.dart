import 'package:flutter/material.dart';
import 'auth_service.dart';

class AppLocalizations {
  final Locale locale;
  AppLocalizations(this.locale);

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const _localizedValues = {
    'en': {
      'registration': 'Registration',
      'cnic': 'CNIC Number',
      'cropType': 'Crop Type',
      'register': 'Register',
      'invalidCnic': 'Please enter a valid CNIC (13 digits)',
      'invalidCrop': 'Please enter crop type',
      'email': 'Email',
      'password': 'Password',
      'registrationSuccess': 'Registration Successful',
      'registrationFailed': 'Registration Failed',
    },
    'ur': {
      'registration': 'رجسٹریشن',
      'cnic': 'شناختی کارڈ نمبر (CNIC)',
      'cropType': 'فصل کی قسم',
      'register': 'رجسٹر کریں',
      'invalidCnic': 'براہ کرم درست شناختی کارڈ نمبر درج کریں (13 ہندسے)',
      'invalidCrop': 'براہ کرم فصل کی قسم درج کریں',
      'email': 'ای میل',
      'password': 'پاس ورڈ',
      'registrationSuccess': 'رجسٹریشن کامیاب رہی',
      'registrationFailed': 'رجسٹریشن ناکام رہی',
    },
  };

  String get registration => _localizedValues[locale.languageCode]!['registration']!;
  String get cnic => _localizedValues[locale.languageCode]!['cnic']!;
  String get cropType => _localizedValues[locale.languageCode]!['cropType']!;
  String get register => _localizedValues[locale.languageCode]!['register']!;
  String get invalidCnic => _localizedValues[locale.languageCode]!['invalidCnic']!;
  String get invalidCrop => _localizedValues[locale.languageCode]!['invalidCrop']!;
  String get email => _localizedValues[locale.languageCode]!['email']!;
  String get password => _localizedValues[locale.languageCode]!['password']!;
  String get registrationSuccess => _localizedValues[locale.languageCode]!['registrationSuccess']!;
  String get registrationFailed => _localizedValues[locale.languageCode]!['registrationFailed']!;

  static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();
  @override
  bool isSupported(Locale locale) => ['en', 'ur'].contains(locale.languageCode);
  @override
  Future<AppLocalizations> load(Locale locale) async => AppLocalizations(locale);
  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

class RegistrationScreen extends StatefulWidget {
  final IAuthService? authService;
  const RegistrationScreen({super.key, this.authService});

  @override
  State<RegistrationScreen> createState() => _RegistrationScreenState();
}

class _RegistrationScreenState extends State<RegistrationScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _cnicController = TextEditingController();
  final _cropController = TextEditingController();
  late final IAuthService _authService;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _authService = widget.authService ?? AuthService();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _cnicController.dispose();
    _cropController.dispose();
    super.dispose();
  }

  Future<void> _handleRegister() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      final l10n = AppLocalizations.of(context)!;
      try {
        final success = await _authService.register(
          email: _emailController.text,
          password: _passwordController.text,
          cnic: _cnicController.text,
          cropType: _cropController.text,
        );
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(success ? l10n.registrationSuccess : l10n.registrationFailed)),
          );
        }
      } finally {
        if (mounted) setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final isUrdu = Localizations.localeOf(context).languageCode == 'ur';
    return Scaffold(
      appBar: AppBar(title: Text(l10n.registration)),
      body: Directionality(
        textDirection: isUrdu ? TextDirection.rtl : TextDirection.ltr,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: SingleChildScrollView(
              child: Column(
                children: [
                  TextFormField(
                    controller: _emailController,
                    decoration: InputDecoration(labelText: l10n.email),
                    validator: (v) => v!.isEmpty ? 'Empty' : null,
                  ),
                  TextFormField(
                    controller: _passwordController,
                    decoration: InputDecoration(labelText: l10n.password),
                    obscureText: true,
                    validator: (v) => v!.length < 6 ? 'Short' : null,
                  ),
                  TextFormField(
                    controller: _cnicController,
                    decoration: InputDecoration(labelText: l10n.cnic),
                    keyboardType: TextInputType.number,
                    validator: (v) => v!.length != 13 ? l10n.invalidCnic : null,
                  ),
                  TextFormField(
                    controller: _cropController,
                    decoration: InputDecoration(labelText: l10n.cropType),
                    validator: (v) => v!.isEmpty ? l10n.invalidCrop : null,
                  ),
                  const SizedBox(height: 20),
                  _isLoading ? const CircularProgressIndicator() : ElevatedButton(onPressed: _handleRegister, child: Text(l10n.register)),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
