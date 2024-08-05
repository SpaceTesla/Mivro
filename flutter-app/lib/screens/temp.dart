import 'package:flutter/material.dart';

class TempPage extends StatelessWidget {
  void _showModalBottomSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) {
        return DraggableScrollableSheet(
          expand: false,
          builder: (context, scrollController) {
            return Container(
              padding: EdgeInsets.all(16.0),
              color: Colors.white,
              child: SingleChildScrollView(
                controller: scrollController,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Image.network(
                          'https://i.imgur.com/Z3Qj4hl.png',
                          width: 60,
                          height: 60,
                        ),
                        SizedBox(width: 16),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '2-minutes masala noodles',
                              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                            ),
                            Text(
                              'Nestle nutrition',
                              style: TextStyle(fontSize: 14, color: Colors.grey),
                            ),
                            Row(
                              children: [
                                Icon(Icons.circle, color: Colors.orange, size: 12),
                                SizedBox(width: 8),
                                Text('14/100', style: TextStyle(color: Colors.orange)),
                                SizedBox(width: 8),
                                Text('D', style: TextStyle(fontSize: 18, color: Colors.orange)),
                              ],
                            ),
                            Text('Very Poor', style: TextStyle(color: Colors.orange)),
                          ],
                        )
                      ],
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Negatives',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    _buildNutritionRow('Carbohydrates', '59.60 g', 'Carb-tastic!', Colors.red),
                    _buildNutritionRow('Fat', '13.50 g', 'Fat-tastic!', Colors.orange),
                    _buildNutritionRow('Energy', '389.00 kcal', 'Energy bomb!', Colors.red),
                    _buildNutritionRow('Saturated Fat', '8.20 g', 'Saturated fat alert!', Colors.red),
                    _buildNutritionRow('Salt', '1.03 g', 'Salt overload!', Colors.red),
                    SizedBox(height: 20),
                    Text(
                      'Positives',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    _buildNutritionRow('Fiber', '2.00 g', 'Fiber-tastic!', Colors.green),
                    _buildNutritionRow('Protein', '8.20 g', 'Protein power!', Colors.green),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildNutritionRow(String title, String amount, String description, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: TextStyle(fontSize: 16)),
              Text(description, style: TextStyle(fontSize: 12, color: Colors.grey)),
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
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Modal Bottom Sheet Example')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _showModalBottomSheet(context),
          child: Text('Show Modal Bottom Sheet'),
        ),
      ),
    );
  }
}