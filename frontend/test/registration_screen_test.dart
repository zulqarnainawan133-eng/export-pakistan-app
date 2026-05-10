import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/registration_screen.dart';
import 'package:frontend/auth_service.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

class MockAuthService implements IAuthService {
  @override
  Future<bool> register({required String email, required String password, required String cnic, required String cropType}) async => true;
}

void main() {
  Widget makeTestable(Locale locale) => MaterialApp(
    localizationsDelegates: const [
      AppLocalizations.delegate,
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ],
    supportedLocales: const [Locale('en'), Locale('ur')],
    locale: locale,
    home: RegistrationScreen(authService: MockAuthService()),
  );

  testWidgets('Renders in Urdu', (tester) async {
    await tester.pumpWidget(makeTestable(const Locale('ur')));
    await tester.pumpAndSettle();
    expect(find.text('رجسٹریشن'), findsOneWidget);
  });

  testWidgets('CNIC validation', (tester) async {
    await tester.pumpWidget(makeTestable(const Locale('en')));
    await tester.pumpAndSettle();
    await tester.enterText(find.widgetWithText(TextFormField, 'CNIC Number'), '123');
    await tester.tap(find.text('Register'));
    await tester.pump();
    expect(find.text('Please enter a valid CNIC (13 digits)'), findsOneWidget);
  });
}
