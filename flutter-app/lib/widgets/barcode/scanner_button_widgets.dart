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
      icon: const Image(image: AssetImage('assets/icons/gallery.png'), height: 40,),
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

// class StartStopMobileScannerButton extends StatelessWidget {
//   const StartStopMobileScannerButton({required this.controller, super.key});

//   final MobileScannerController controller;

//   @override
//   Widget build(BuildContext context) {
//     return ValueListenableBuilder(
//       valueListenable: controller.cameraFacingState,
//       builder: (context, state, child) {
//         if (!state.isInitialized || !state.isRunning) {
//           return IconButton(
//             color: Colors.white,
//             icon: const Icon(Icons.play_arrow),
//             iconSize: 32.0,
//             onPressed: () async {
//               await controller.start();
//             },
//           );
//         }

//         return IconButton(
//           color: Colors.white,
//           icon: const Icon(Icons.stop),
//           iconSize: 32.0,
//           onPressed: () async {
//             await controller.stop();
//           },
//         );
//       },
//     );
//   }
// }

// class SwitchCameraButton extends StatelessWidget {
//   const SwitchCameraButton({required this.controller, super.key});

//   final MobileScannerController controller;

//   @override
//   Widget build(BuildContext context) {
//     return ValueListenableBuilder(
//       valueListenable: controller.cameraFacingState,
//       builder: (context, state, child) {
//         if (!state.isInitialized || !state.isRunning) {
//           return const SizedBox.shrink();
//         }

//         final int? availableCameras = state.availableCameras;

//         if (availableCameras != null && availableCameras < 2) {
//           return const SizedBox.shrink();
//         }

//         final Widget icon;

//         switch (state.cameraDirection) {
//           case CameraFacing.front:
//             icon = const Icon(Icons.camera_front);
//           case CameraFacing.back:
//             icon = const Icon(Icons.camera_rear);
//         }

//         return IconButton(
//           iconSize: 32.0,
//           icon: icon,
//           onPressed: () async {
//             await controller.switchCamera();
//           },
//         );
//       },
//     );
//   }
// }

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
              icon: const Image(image: AssetImage('assets/icons/thunderbolt-.png'), height: 45,),
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
              icon: const Image(image: AssetImage('assets/icons/lightning.png'), height: 45,),
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
