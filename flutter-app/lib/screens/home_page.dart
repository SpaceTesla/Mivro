import 'package:mivro/screens/barcode_scanner_screen.dart';
import 'package:mivro/screens/chat_screen.dart';
import 'package:mivro/screens/marketplace_screen.dart';
import 'package:mivro/screens/overview_screen.dart';
import 'package:mivro/screens/profile_screen.dart';
import 'package:mivro/utils/hexcolor.dart';
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
        body: screens[myIndex],
        bottomNavigationBar: ClipRRect(
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(20),
            topRight: Radius.circular(20),
          ),
          child: BottomNavigationBar(
            showUnselectedLabels: false,
            type: BottomNavigationBarType.shifting,
            selectedLabelStyle: const TextStyle(color: Colors.black),
            selectedItemColor: Colors.black,
            backgroundColor:
                Theme.of(context).bottomNavigationBarTheme.backgroundColor,
            onTap: (index) {
              setState(() {
                myIndex = index;
              });
            },
            currentIndex: myIndex,
            items: [
              BottomNavigationBarItem(
                icon: const Image(
                  image: AssetImage('assets/navigation/chat.png'),
                  height: 35,
                ),
                label: 'Chat',
                backgroundColor: myColorFromHex("#EEF1FF"),
              ),
              BottomNavigationBarItem(
                icon: const Image(
                  image: AssetImage('assets/navigation/marketplace.png'),
                  height: 35,
                ),
                label: 'Marketplace',
                backgroundColor: myColorFromHex("#EEF1FF"),
              ),
              BottomNavigationBarItem(
                icon: const Image(
                  image: AssetImage('assets/navigation/scanner.png'),
                  height: 35,
                ),
                label: 'Scanner',
                backgroundColor: myColorFromHex("#EEF1FF"),
              ),
              BottomNavigationBarItem(
                icon: const Image(
                  image: AssetImage('assets/navigation/tracker.png'),
                  height: 35,
                ),
                label: 'Tracker',
                backgroundColor: myColorFromHex("#EEF1FF"),
              ),
              BottomNavigationBarItem(
                icon: const Image(
                  image: AssetImage('assets/navigation/profile.png'),
                  height: 35,
                ),
                label: 'Profile',
                backgroundColor: myColorFromHex("#EEF1FF"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
