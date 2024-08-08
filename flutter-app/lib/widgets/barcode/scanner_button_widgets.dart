import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class AnalyzeImageFromGalleryButton extends StatelessWidget {
  const AnalyzeImageFromGalleryButton({required this.controller, super.key});

  final MobileScannerController controller;

  @override
  Widget build(BuildContext context) {
    return IconButton(
      color: Colors.white,
      icon: const Image(
        image: AssetImage('assets/navigation/gallery.png'),
        height: 40,
      ),
      iconSize: 32.0,
      onPressed: () async {
        final ImagePicker picker = ImagePicker();

        final XFile? image = await picker.pickImage(
          source: ImageSource.gallery,
        );

        if (image == null) {
          return;
        }

        final bool barcodes = await controller.analyzeImage(
          image.path,
        );

        if (!context.mounted) {
          return;
        }

        final SnackBar snackbar = barcodes != null
            ? const SnackBar(
                content: Text('Barcode found!'),
                backgroundColor: Colors.green,
              )
            : const SnackBar(
                content: Text('No barcode found!'),
                backgroundColor: Colors.red,
              );

        ScaffoldMessenger.of(context).showSnackBar(snackbar);
      },
    );
  }
}

class ToggleFlashlightButton extends StatelessWidget {
  const ToggleFlashlightButton({required this.controller, super.key});

  final MobileScannerController controller;

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: controller.torchState,
      builder: (context, state, child) {
        if (controller.torchState.value == null) {
          return const SizedBox.shrink();
        }

        switch (controller.torchState.value) {
          case TorchState.off:
            return IconButton(
              color: Colors.grey,
              iconSize: 32.0,
              icon: const Image(
                image: AssetImage('assets/navigation/flash-off.png'),
                height: 45,
              ),
              onPressed: () async {
                await controller.toggleTorch();
                controller.torchState.value =
                    TorchState.on; // Manually set state
              },
            );
          case TorchState.on:
            return IconButton(
              color: Colors.white,
              iconSize: 32.0,
              icon: const Image(
                image: AssetImage('assets/navigation/flash-on.png'),
                height: 45,
              ),
              onPressed: () async {
                await controller.toggleTorch();
                controller.torchState.value =
                    TorchState.off; // Manually set state
              },
            );

          default:
            return const SizedBox.shrink();
        }
      },
    );
  }
}
