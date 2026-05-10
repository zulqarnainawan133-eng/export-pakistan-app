import 'package:firebase_auth/firebase_auth.dart';

abstract class IAuthService {
  Future<bool> register({
    required String email,
    required String password,
    required String cnic,
    required String cropType,
  });
}

class AuthService implements IAuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  @override
  Future<bool> register({
    required String email,
    required String password,
    required String cnic,
    required String cropType,
  }) async {
    try {
      UserCredential result = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      return result.user != null;
    } catch (e) {
      return false;
    }
  }
}
