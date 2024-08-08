import 'dart:convert';
import 'dart:developer';

import 'package:mivro/models/message.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

class ChatsNotifier extends StateNotifier<List<dynamic>> {
  ChatsNotifier() : super([]);
  bool _isLoading = false;
  bool get isLoading => _isLoading;

  Future<Message?> getResponse(String prompt) async {
    try {
      log('in get response');
      _isLoading = true;
      state = [...state];
      String url = 'http://192.168.195.94:5000/api/v1/ai/savora';

      Map<String, String> body = {
        "email": "areebahmed0709@gmail.com",
        "message": prompt,
      };

      final response = await http.post(
        Uri.parse(url),
        body: json.encode(body),
        headers: {
          "Content-Type": "application/json",
        },
      );

      log('got response');

      if (response.statusCode == 200) {
        var data = json.decode(response.body);

        final result = data['response'];
        log(result);

        final chat = Message(text: result, isUser: false);

        state = [...state, chat];
        _isLoading = false;
        state = [...state];
        return chat;
      } else {
        log(response.body);
        return null;
      }
    } catch (e) {
      log(e.toString());
      return null;
    }
  }
}

final chatsProvider = StateNotifierProvider<ChatsNotifier, List<dynamic>>(
    (ref) => ChatsNotifier());
