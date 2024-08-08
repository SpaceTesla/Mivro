import 'package:mivro/screens/home_page.dart';
import 'package:mivro/utils/hexcolor.dart';
import 'package:flutter/material.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

void main() async {
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);
  FlutterNativeSplash.remove();

  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: theme,
      home: const HomePage(),
    );
  }
}

final theme = ThemeData.light().copyWith(
  textTheme: GoogleFonts.poppinsTextTheme(),
  scaffoldBackgroundColor: myColorFromHex("#F8EDE3"),
  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    backgroundColor: myColorFromHex("#134B70"),
    selectedItemColor: Colors.white,
    unselectedItemColor: Colors.white,
  ),
);
