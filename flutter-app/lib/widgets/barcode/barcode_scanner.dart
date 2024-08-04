import 'dart:async';

import 'package:mivro/widgets/barcode/scanner_button_widgets.dart';
import 'package:mivro/widgets/barcode/scanner_error_widget.dart';
import 'package:mivro/widgets/search_bar.dart';
import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class BarcodeScannerListView extends StatefulWidget {
  const BarcodeScannerListView({super.key});

  @override
  State<BarcodeScannerListView> createState() => _BarcodeScannerListViewState();
}

class _BarcodeScannerListViewState extends State<BarcodeScannerListView> {
  MobileScannerController? controller;

  void _initializeController() {
    if (controller == null) {
      controller = MobileScannerController(torchEnabled: false);
      setState(() {}); // Trigger build to use the new controller
    }
  }

  Widget _buildBarcodesListView() {
    return StreamBuilder<BarcodeCapture>(
      stream: controller!.barcodes,
      builder: (context, snapshot) {
        final barcodes = snapshot.data?.barcodes;

        if (barcodes == null || barcodes.isEmpty) {
          return const Center(
            child: Text(
              'Scan Something!',
              style: TextStyle(color: Colors.white, fontSize: 20),
            ),
          );
        }

        return ListView.builder(
          itemCount: barcodes.length,
          itemBuilder: (context, index) {
            return Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                barcodes[index].rawValue ?? 'No raw value',
                overflow: TextOverflow.fade,
                style: const TextStyle(color: Colors.white),
              ),
            );
          },
        );
      },
    );
  }

  @override
  void initState() {
    // TODO: implement initState
    _initializeController();
    controller!.stop();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        MobileScanner(
          onDetect: (barcodeCapture) {},
          controller: controller,
          errorBuilder: (context, error, child) {
            // controller!.stop();
            // controller!.start();
            return ScannerErrorWidget(error: error);
          },
          fit: BoxFit.cover,
        ),
        const Positioned(
          top: 10,
          left: 10,
          right: 10,
          child: SearchBarWIdget(),
        ),
        Positioned(
          top: 300,
          right: 10,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              ToggleFlashlightButton(controller: controller!),
              AnalyzeImageFromGalleryButton(controller: controller!),
            ],
          ),
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: Container(
            alignment: Alignment.bottomCenter,
            height: 100,
            color: Colors.black.withOpacity(0.4),
            child: Column(
              children: [
                Expanded(
                  child: _buildBarcodesListView(),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    super.dispose();
    controller!.dispose();
  }
}
