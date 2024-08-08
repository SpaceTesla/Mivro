import 'package:mivro/utils/hexcolor.dart';
import 'package:flutter/material.dart';

class SearchBarWIdget extends StatelessWidget {
  const SearchBarWIdget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      decoration: BoxDecoration(
        color: myColorFromHex('#EEF1FF'), // Background color
        borderRadius: BorderRadius.circular(30.0), // Rounded corners
      ),
      child: const Padding(
        padding: EdgeInsets.all(2.0),
        child: Row(
          children: [
            Image(image: AssetImage('assets/navigation/search.png'), height: 20),
            SizedBox(width: 8.0),
            Expanded(
              child: TextField(
                decoration: InputDecoration(
                    hintText: 'Search', border: InputBorder.none),
              ),
            ),
            Icon(Icons.mic, color: Colors.black54),
          ],
        ),
      ),
    );
  }
}
