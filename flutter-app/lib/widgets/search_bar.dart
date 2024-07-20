import 'package:flutter/material.dart';

class SearchBarWIdget extends StatelessWidget {
  const SearchBarWIdget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      decoration: BoxDecoration(
        
        color: const Color(0xFFE0E0E0), // Background color
        borderRadius: BorderRadius.circular(30.0), // Rounded corners
      ),
      child: const Padding(
        padding:  EdgeInsets.all(2.0),
        child:  Row(
          children: [
            Icon(Icons.search, color: Colors.black54),
            SizedBox(width: 8.0),
            Expanded(
              child: TextField(
                decoration: InputDecoration(
                  hintText: 'Search',
                  border: InputBorder.none
                ),
              ),
            ),
            Icon(Icons.mic, color: Colors.black54),
          ],
        ),
      ),
    );
  }
}
