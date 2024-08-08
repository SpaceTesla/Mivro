import 'package:flutter_test/flutter_test.dart';
import 'package:mivro/models/message.dart';

void main() {
  group('Message Model', () {
    test('should return a Message instance', () {
      // arrange
      var message;

      // act
      message = const Message(text: 'Hello', isUser: true);

      // assert
      expect(message, isA<Message>());
      expect(message.isUser, true);
      expect(message.text, 'Hello');
    });
  });
}