import 'package:flutter/material.dart';

class MarketplaceScreen extends StatefulWidget {
  const MarketplaceScreen({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _MarketplaceScreen();
}

class _MarketplaceScreen extends State<MarketplaceScreen> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Text('Marketplace Screen'),
      ),
    );
  }
}