import 'package:mivro/widgets/bar_code_scanner.dart';
import 'package:mivro/widgets/search_bar.dart';
import 'package:flutter/material.dart';

class BarcodeScannerScreen extends StatefulWidget {
  const BarcodeScannerScreen({super.key});

  @override
  State<StatefulWidget> createState() => _BarcodeScannerScreen();
}

class _BarcodeScannerScreen extends State<BarcodeScannerScreen> {
  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        SearchBarWIdget(),
        BarCodeScanner(),
      ],
    );
  }
}
