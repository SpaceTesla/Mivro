import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mivro/models/message.dart';
import 'package:mivro/providers/chat_history_provider.dart';

void main() {
  group('ChatHistoryNotifier', () {
    final container = ProviderContainer();
    test('initial state contains default message', () {
      // arrange
      var chatHistory = <Message>[];

      // act
      chatHistory = container.read(chatHistoryProvider);

      // assert
      expect(chatHistory, [const Message(text: 'Hello! How can I help you?', isUser: false)]);
    });

    test('addMessage adds a new message to the state', () {
      // arrange
      final notifier = container.read(chatHistoryProvider.notifier);
      final newMessage = Message(text: 'Hi there!', isUser: true);

      // act
      notifier.addMessage(newMessage);
      final chatHistory = container.read(chatHistoryProvider);

      // assert
      expect(chatHistory, [
        const Message(text: 'Hello! How can I help you?', isUser: false),
        newMessage,
      ]);
    });

  });
}