import 'package:areeb/screens/barcode_scanner_screen.dart';
import 'package:areeb/screens/chat_screen.dart';
import 'package:areeb/screens/marketplace_screen.dart';
import 'package:areeb/screens/overview_screen.dart';
import 'package:areeb/screens/profile_screen.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<StatefulWidget> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  var myIndex = 2;

  List<Widget> screens = [
    const ChatbotScreen(),
    const MarketplaceScreen(),
    const BarcodeScannerScreen(),
    const OverviewScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body:  Padding(
          padding: const EdgeInsets.only(top: 24, left: 8, right: 8),
          child: screens[myIndex]
        ),
        bottomNavigationBar: BottomNavigationBar(
          showUnselectedLabels: false,
          type: BottomNavigationBarType.shifting,
          onTap: (index) {
            setState(() {
              myIndex = index;
            });
          },
          currentIndex: myIndex,
          items: const [
            BottomNavigationBarItem(
                icon: Icon(
                  Icons.chat,
                ),
                label: 'Chat',
                backgroundColor: Colors.black),
            BottomNavigationBarItem(
                icon: Icon(
                  Icons.shopify_rounded,
                ),
                label: 'Marketplace',
                backgroundColor: Colors.black),
            BottomNavigationBarItem(
                icon: Icon(
                  Icons.barcode_reader,
                ),
                label: 'Scanner',
                backgroundColor: Colors.black),
            BottomNavigationBarItem(
                icon: Icon(
                  Icons.menu,
                ),
                label: 'Overview',
                backgroundColor: Colors.black),
            BottomNavigationBarItem(
                icon: Icon(
                  Icons.person,
                ),
                label: 'Profile',
                backgroundColor: Colors.black),
          ],
        ),
      ),
    );
  }
}
