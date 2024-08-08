import 'package:mivro/utils/hexcolor.dart';
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

  Icon favorite = const Icon(Icons.favorite_border);
  ValueNotifier<bool> showMorePositives = ValueNotifier(false);
  ValueNotifier<bool> showMoreIngredients = ValueNotifier(false);
  ValueNotifier<bool> showMoreNegatives = ValueNotifier(false);

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
                    padding: const EdgeInsets.only(
                        top: 5, left: 16, right: 16, bottom: 16),
                    color: Colors.white,
                    child: SingleChildScrollView(
                      controller: scrollController,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Text('Detected Barcode: ${barcodes![0].rawValue}'),
                          Row(
                            children: [
                              // const Image(
                              //   image: AssetImage(
                              //     'assets/images/logo-transparent.png',
                              //   ),
                              //   height: 70,
                              // ),
                              const Spacer(),
                              IconButton(
                                icon: const Icon(Icons.ios_share_rounded),
                                iconSize: 20,
                                onPressed: () {},
                              ),
                              StatefulBuilder(
                                builder: (BuildContext context,
                                    StateSetter setState) {
                                  return IconButton(
                                    icon: favorite,
                                    iconSize: 20,
                                    onPressed: () {
                                      setState(() {
                                        favorite = Icon(
                                          favorite.icon == Icons.favorite
                                              ? Icons.favorite_border
                                              : Icons.favorite,
                                        );
                                      });
                                    },
                                  );
                                },
                              ),
                              IconButton(
                                icon: const Icon(Icons.flag_outlined),
                                iconSize: 20,
                                onPressed: () {},
                              ),
                              IconButton(
                                icon: const Icon(Icons.close),
                                iconSize: 20,
                                onPressed: () {
                                  Navigator.pop(context);
                                  controller!.start();
                                },
                              ),
                            ],
                          ),
                          Row(
                            children: [
                              Image.network(
                                'https://5.imimg.com/data5/SELLER/Default/2022/7/MU/PJ/SD/5742893/maggi-noodles.jpg',
                                width: 60,
                                height: 60,
                              ),
                              const SizedBox(width: 16),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'MAGGI 2-Minute Instant Noodles',
                                    style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold),
                                  ),
                                  const Text(
                                    'Nestle',
                                    style: TextStyle(
                                        fontSize: 14, color: Colors.grey),
                                  ),
                                  Row(
                                    children: [
                                      Icon(Icons.circle,
                                          color: myColorFromHex('#F8A72C'),
                                          size: 12),
                                      const SizedBox(width: 8),
                                      Text('14/100',
                                          style: TextStyle(
                                              color:
                                                  myColorFromHex('#F8A72C'))),
                                      const SizedBox(width: 8),
                                      Text('D',
                                          textAlign: TextAlign.right,
                                          style: TextStyle(
                                              fontSize: 18,
                                              color:
                                                  myColorFromHex('#F8A72C'))),
                                    ],
                                  ),
                                  Text('Very Poor',
                                      style: TextStyle(
                                          color: myColorFromHex('#F8A72C'))),
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
                          _buildNutritionRow(
                              'Carbohydrates',
                              '59.60 g',
                              'Carb-tastic!',
                              Colors.red,
                              'assets/icons/carbohydrate.png'),
                          _buildNutritionRow('Fat', '13.50 g', 'Fat-tastic!',
                              Colors.orange, 'assets/icons/fat.png'),
                          _buildNutritionRow(
                              'Energy',
                              '389.00 kcal',
                              'Energy bomb!',
                              Colors.red,
                              'assets/icons/energy.png'),
                          ValueListenableBuilder(
                            valueListenable: showMoreNegatives,
                            builder: (context, value, child) {
                              if (value) {
                                return Column(
                                  children: [
                                    _buildNutritionRow(
                                        'Saturated Fat',
                                        '8.20 g',
                                        'Saturated fat alert!',
                                        Colors.red,
                                        'assets/icons/fatty-acid.png'),
                                    _buildNutritionRow(
                                        'Salt',
                                        '1.03 g',
                                        'Salt overload!',
                                        Colors.red,
                                        'assets/icons/salt.png'),
                                    // const SizedBox(height: 20),
                                  ],
                                );
                              }
                              return const SizedBox.shrink();
                            },
                          ),
                          StatefulBuilder(builder:
                              (BuildContext context, StateSetter setState) {
                            return TextButton(
                              onPressed: () {
                                setState(() {
                                  showMoreNegatives.value =
                                      !showMoreNegatives.value;
                                });
                              },
                              child: Text(
                                showMoreNegatives.value
                                    ? 'Show Less'
                                    : 'Show More',
                                style: const TextStyle(color: Colors.blue),
                              ),
                            );
                          }),

                          const SizedBox(height: 20),

                          const Text(
                            'Positives',
                            style: TextStyle(
                                fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          _buildNutritionRow('Fiber', '2.00 g', 'Fiber-tastic!',
                              Colors.green, 'assets/icons/fiber.png'),
                          _buildNutritionRow(
                              'Protein',
                              '8.20 g',
                              'Protein power!',
                              Colors.green,
                              'assets/icons/protein.png'),
                          ValueListenableBuilder<bool>(
                            valueListenable: showMorePositives,
                            builder: (context, value, child) {
                              if (value) {
                                return Column(
                                  children: [
                                    _buildNutritionRow(
                                        'Saturated Fat',
                                        '8.20 g',
                                        'Saturated fat alert!',
                                        Colors.red,
                                        'assets/icons/fatty-acid.png'),
                                    _buildNutritionRow(
                                        'Salt',
                                        '1.03 g',
                                        'Salt overload!',
                                        Colors.red,
                                        'assets/icons/salt.png'),
                                    _buildNutritionRow(
                                        'Fiber',
                                        '2.00 g',
                                        'Fiber-tastic!',
                                        Colors.green,
                                        'assets/icons/fiber.png'),
                                    _buildNutritionRow(
                                        'Protein',
                                        '8.20 g',
                                        'Protein power!',
                                        Colors.green,
                                        'assets/icons/protein.png'),
                                    // const SizedBox(height: 20),
                                  ],
                                );
                              }
                              return const SizedBox.shrink();
                            },
                          ),
                          StatefulBuilder(builder:
                              (BuildContext context, StateSetter setState) {
                            return TextButton(
                              onPressed: () {
                                setState(() {
                                  showMorePositives.value =
                                      !showMorePositives.value;
                                });
                              },
                              child: Text(
                                showMorePositives.value
                                    ? 'Show Less'
                                    : 'Show More',
                                style: const TextStyle(color: Colors.blue),
                              ),
                            );
                          }),
                          const SizedBox(height: 20),
                          const Text(
                            'Ingredients',
                            style: TextStyle(
                                fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 10),
                          _buildIngredientRow('Wheat Flour', '46.70%',
                              'assets/icons/wheat-flour.png'),
                          _buildIngredientRow('Chocolate Chips', '23.00%',
                              'assets/icons/chocolate-chip.png'),
                          _buildIngredientRow(
                              'Sugar', '11.80%', 'assets/icons/sugar.png'),
                          ValueListenableBuilder(
                              valueListenable: showMoreIngredients,
                              builder: (context, value, child) {
                                if (value) {
                                  return Column(
                                    children: [
                                      _buildIngredientRow('Cocoa Mass', '9.55%',
                                          'assets/icons/cocoa.png'),
                                      _buildIngredientRow('Cocoa Butter',
                                          '4.78%', 'assets/icons/butter.png'),
                                      _buildIngredientRow('Dextrose', '2.39%',
                                          'assets/icons/starch.png'),
                                      _buildIngredientRow('Emulsifier', '1.19%',
                                          'assets/icons/emulsifier.png'),
                                      _buildIngredientRow(
                                          'Artificial Flavouring Sugar',
                                          '0.60%',
                                          'assets/icons/syrup.png'),
                                      _buildIngredientRow(
                                          'Vegetable Oil Palm Oil',
                                          '0.30%',
                                          'assets/icons/palm-oil.png'),
                                      _buildIngredientRow(
                                          'Glucose-Fructose Syrup',
                                          '0.15%',
                                          'assets/icons/glucose.png'),
                                      _buildIngredientRow('Raising Agents',
                                          '0.07%', 'assets/icons/additive.png'),
                                    ],
                                  );
                                }
                                return const SizedBox.shrink();
                              }),
                          StatefulBuilder(builder:
                              (BuildContext context, StateSetter setState) {
                            return TextButton(
                              onPressed: () {
                                setState(() {
                                  showMoreIngredients.value =
                                      !showMoreIngredients.value;
                                });
                              },
                              child: Text(
                                showMoreIngredients.value
                                    ? 'Show Less'
                                    : 'Show More',
                                style: const TextStyle(color: Colors.blue),
                              ),
                            );
                          }),
                          // _buildIngredientRow(
                          //     'Cocoa Mass', '9.55%', 'assets/icons/cocoa.png'),
                          // _buildIngredientRow('Cocoa Butter', '4.78%',
                          //     'assets/icons/butter.png'),
                          // _buildIngredientRow(
                          //     'Dextrose', '2.39%', 'assets/icons/starch.png'),
                          // _buildIngredientRow('Emulsifier', '1.19%',
                          //     'assets/icons/emulsifier.png'),
                          // _buildIngredientRow('Artificial Flavouring Sugar',
                          //     '0.60%', 'assets/icons/syrup.png'),
                          // _buildIngredientRow('Vegetable Oil Palm Oil', '0.30%',
                          //     'assets/icons/palm-oil.png'),
                          // _buildIngredientRow('Glucose-Fructose Syrup', '0.15%',
                          //     'assets/icons/glucose.png'),
                          // _buildIngredientRow('Raising Agents', '0.07%',
                          //     'assets/icons/additive.png'),

                          const SizedBox(height: 20),
                          // Allergies Section
                          const Text("Nova Group",
                              style: TextStyle(
                                  fontSize: 16, fontWeight: FontWeight.bold)),
                          Padding(
                              padding: const EdgeInsets.symmetric(vertical: 4.0),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.start,
                                children: [
                                  Image.asset(
                                    'assets/new/4.png',
                                    height: 30,
                                    width: 30,
                                  ),
                                  const SizedBox(width: 8),
                                  const Text(
                                      "Ultra-processed food and drink products"),
                                ],
                              )),
                          const SizedBox(height: 16),

                          // Health Risks Section
                          const Text("Health Risks",
                              style: TextStyle(
                                  fontSize: 16, fontWeight: FontWeight.bold)),

                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                            child: Row(
                              children: [
                                Image.asset(
                                  'assets/new/health-risk.png',
                                  height: 30,
                                  width: 30,
                                ),
                                const SizedBox(width: 8),
                                const Expanded(
                                  child:  Text(
                                    "This product contains E472e (esters of acetic acid and mono- and diglycerides of fatty acids), "
                                    "which may be derived from palm oil and may be a concern for some individuals.",
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 16),

                          // Recommendation Section
                          const Text("Recommendation",
                              style: TextStyle(
                                  fontSize: 16, fontWeight: FontWeight.bold)),

                          Row(
                            children: [
                              Image.network(
                                'https://www.bigbasket.com/media/uploads/p/l/40113739_14-maggi-noodles-nutri-licious-masala-oats.jpg',
                                width: 60,
                                height: 60,
                              ),
                              const SizedBox(width: 16),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'MAGGI Noodles - Masala Oats',
                                    style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold),
                                  ),
                                  const Text(
                                    'Nestle',
                                    style: TextStyle(
                                        fontSize: 14, color: Colors.grey),
                                  ),
                                  Row(
                                    children: [
                                      Icon(Icons.circle,
                                          color: myColorFromHex('#FFD65A'),
                                          size: 12),
                                      const SizedBox(width: 8),
                                      Text('27/100',
                                          style: TextStyle(
                                              color:
                                                  myColorFromHex('#FFD65A'))),
                                      const SizedBox(width: 8),
                                      Text('C',
                                          textAlign: TextAlign.right,
                                          style: TextStyle(
                                              fontSize: 18,
                                              color:
                                                  myColorFromHex('#FFD65A'))),
                                    ],
                                  ),
                                  Text('Poor',
                                      style: TextStyle(
                                          color: myColorFromHex('#FFD65A'))),
                                ],
                              )
                            ],
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

  Widget _buildIngredientRow(
      String name, String percentage, String imageString) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Image.asset(imageString, width: 30, height: 30),
          const SizedBox(width: 8),
          Text(name, style: const TextStyle(fontSize: 14)),
          const Spacer(),
          Text(
            percentage,
            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }

  Widget _buildNutritionRow(String title, String amount, String description,
      Color color, String imageString) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Image.asset(imageString, width: 30, height: 30),
          const SizedBox(width: 8),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(fontSize: 16)),
              Text(description,
                  style: const TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          const Spacer(),
          Row(
            children: [
              Text(amount,
                  style: TextStyle(
                      fontSize: 16, color: color, fontWeight: FontWeight.bold)),
              const SizedBox(width: 8),
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
              border: Border.all(
                  color: const Color.fromARGB(255, 172, 49, 40), width: 2),
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
