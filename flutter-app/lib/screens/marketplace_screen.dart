import 'package:flutter/material.dart';

class MarketplaceScreen extends StatefulWidget {
  const MarketplaceScreen({super.key});

  @override
  State<StatefulWidget> createState() {
    return _MarketplaceScreenState();
  }
}

class _MarketplaceScreenState extends State<MarketplaceScreen> {
  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        'MarketPlace',
        style: TextStyle(fontSize: 24),
      ),
    );
  }
}
