import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:mivro/utils/hexcolor.dart';

void main() {
  group('myColorFromHex', () {
    test('converts 6-digit hex to Color', () {
      final color = myColorFromHex('FFFFFF');
      expect(color, Color(0xFFFFFFFF));
    });

    test('converts 6-digit hex with # to Color', () {
      final color = myColorFromHex('#FFFFFF');
      expect(color, Color(0xFFFFFFFF));
    });

    test('converts 8-digit hex to Color', () {
      final color = myColorFromHex('FF0000FF');
      expect(color, Color(0xFF0000FF));
    });

    test('converts 8-digit hex with # to Color', () {
      final color = myColorFromHex('#FF0000FF');
      expect(color, Color(0xFF0000FF));
    });

    test('handles lowercase hex', () {
      final color = myColorFromHex('ff0000');
      expect(color, Color(0xFFFF0000));
    });

    test('handles invalid hex gracefully', () {
      expect(() => myColorFromHex('ZZZZZZ'), throwsFormatException);
    });

    test('handles empty string gracefully', () {
      expect(() => myColorFromHex(''), throwsFormatException);
    });
  });
}