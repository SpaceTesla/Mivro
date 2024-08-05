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
      setState(() {}); 
    }
  }

  Widget _buildBarcodesListView() {
    return StreamBuilder<BarcodeCapture>(
      stream: controller!.barcodes,
      builder: (context, snapshot) {
        final barcodes = snapshot.data?.barcodes;

        if (barcodes == null || barcodes.isEmpty) {
          return const SizedBox.shrink();
        }

        controller!.stop();

        WidgetsBinding.instance.addPostFrameCallback((_) {
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            builder: (context) {
              return DraggableScrollableSheet(
                expand: false,
                builder: (context, scrollController) {
                  return Container(
                    padding: const EdgeInsets.all(16.0),
                    color: Colors.white,
                    child: SingleChildScrollView(
                      controller: scrollController,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Text('Detected Barcode: ${barcodes![0].rawValue}'),
                          Row(
                            children: [
                              Image.network(
                                'https://i.imgur.com/Z3Qj4hl.png',
                                width: 60,
                                height: 60,
                              ),
                              const SizedBox(width: 16),
                              const Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    '2-minutes masala noodles',
                                    style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold),
                                  ),
                                  Text(
                                    'Nestle nutrition',
                                    style: TextStyle(
                                        fontSize: 14, color: Colors.grey),
                                  ),
                                  Row(
                                    children: [
                                      Icon(Icons.circle,
                                          color: Colors.orange, size: 12),
                                      SizedBox(width: 8),
                                      Text('14/100',
                                          style:
                                              TextStyle(color: Colors.orange)),
                                      SizedBox(width: 8),
                                      Text('D',
                                          style: TextStyle(
                                              fontSize: 18,
                                              color: Colors.orange)),
                                    ],
                                  ),
                                  Text('Very Poor',
                                      style: TextStyle(color: Colors.orange)),
                                ],
                              )
                            ],
                          ),
                          const SizedBox(height: 20),
                          const Text(
                            'Negatives',
                            style: TextStyle(
                                fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          _buildNutritionRow('Carbohydrates', '59.60 g',
                              'Carb-tastic!', Colors.red),
                          _buildNutritionRow(
                              'Fat', '13.50 g', 'Fat-tastic!', Colors.orange),
                          _buildNutritionRow('Energy', '389.00 kcal',
                              'Energy bomb!', Colors.red),
                          _buildNutritionRow('Saturated Fat', '8.20 g',
                              'Saturated fat alert!', Colors.red),
                          _buildNutritionRow(
                              'Salt', '1.03 g', 'Salt overload!', Colors.red),
                          const SizedBox(height: 20),
                          const Text(
                            'Positives',
                            style: TextStyle(
                                fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          _buildNutritionRow(
                              'Fiber', '2.00 g', 'Fiber-tastic!', Colors.green),
                          _buildNutritionRow('Protein', '8.20 g',
                              'Protein power!', Colors.green),
                          // Allergies Section
                          const Text("Allergies",
                              style: TextStyle(
                                  fontSize: 20, fontWeight: FontWeight.bold)),
                          const Padding(
                            padding:  EdgeInsets.symmetric(vertical: 4.0),
                            child:  Text("Soybeans"),
                          ),
                          const SizedBox(height: 16),

                          // Health Risks Section
                          const Text("Health Risks",
                              style: TextStyle(
                                  fontSize: 20, fontWeight: FontWeight.bold)),
                          
                          const Padding(
                            padding:  EdgeInsets.symmetric(vertical: 4.0),
                            child:  Text(
                              "This product contains E472e (esters of acetic acid and mono- and diglycerides of fatty acids), "
                              "which may be derived from palm oil and may be a concern for some individuals.",
                            ),
                          ),
                          const SizedBox(height: 16),

                          // Recommendation Section
                          const Text("Recommendation",
                              style: TextStyle(
                                  fontSize: 20, fontWeight: FontWeight.bold)),
                          const Padding(
                            padding:  EdgeInsets.symmetric(vertical: 4.0),
                            child:  Text("No data available."),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              );
            },
          );
        });

        controller!.start();

        return const SizedBox.shrink();
      },
    );
  }

  Widget _buildNutritionRow(
      String title, String amount, String description, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(fontSize: 16)),
              Text(description,
                  style:const TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          Row(
            children: [
              Text(amount, style: TextStyle(fontSize: 16, color: color)),
              Icon(Icons.circle, color: color, size: 12),
            ],
          ),
        ],
      ),
    );
  }

  @override
  void initState() {
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
        Center(
          child: Container(
            height: 150,
            width: 400,
            decoration: BoxDecoration(
              border: Border.all(color: const Color.fromARGB(255, 172, 49, 40), width: 2),
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),
        Positioned(
          top: 200,
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
