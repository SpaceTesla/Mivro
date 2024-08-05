import 'dart:developer';

import 'package:mivro/models/message.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_generative_ai/google_generative_ai.dart';

class ChatsNotifier extends StateNotifier<List<dynamic>> {
  ChatsNotifier() : super([]);
  bool _isLoading = false;
  bool get isLoading => _isLoading;

  Future<Message> getResponse(String prompt) async {
    _isLoading = true;
    state = [...state];
    var geminiApiKey = '';
    log(geminiApiKey);
    log('here in gemini api provider');
    final model = GenerativeModel(model: 'gemini-pro', apiKey: geminiApiKey);
    final content = [
      Content.text(
          prompt)
    ];

    final response = await model.generateContent(content);

    final chat = Message(text: response.text!, isUser: false);

    state = [...state, chat];
    _isLoading = false;
    state = [...state];

    return chat;
  }
}

final chatsProvider = StateNotifierProvider<ChatsNotifier, List<dynamic>>(
    (ref) => ChatsNotifier());
