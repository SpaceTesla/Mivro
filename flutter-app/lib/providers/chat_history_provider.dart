import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mivro/models/message.dart';

class ChatHistoryNotifier extends StateNotifier<List<Message>> {
  ChatHistoryNotifier()
      : super([const Message(text: 'Hello! How can I help you?', isUser: false)]);

  void addMessage(Message message) {
    state = [...state, message];
  }
}

final chatHistoryProvider = StateNotifierProvider<ChatHistoryNotifier, List<Message>>(
    (ref) => ChatHistoryNotifier());
