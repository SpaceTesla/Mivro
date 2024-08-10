import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mivro/models/message.dart';
import 'package:mivro/providers/chat_provider.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:google_generative_ai/google_generative_ai.dart';

@GenerateMocks([],
    customMocks: [MockSpec<GenerativeModel>(as: #MockGenerativeModel)])
void main() {
  var geminiApiKey = '';

  group('ChatsNotifier', () {
    final model = GenerativeModel(model: 'gemini-pro', apiKey: geminiApiKey);
    test('initial state is empty', () {
      final container = ProviderContainer();
      final chats = container.read(chatsProvider);

      expect(chats, []);
    });

    test('getResponse adds a new message to the state', () async {
      final container = ProviderContainer();
      final notifier = container.read(chatsProvider.notifier);

      final response = await notifier.getResponse('Prompt text');

      final chats = container.read(chatsProvider);
      expect(chats, [Message(text: 'Response text', isUser: false)]);
      expect(response?.text, 'Response text');
    });

    test('getResponse sets isLoading to true while fetching', () async {
      final container = ProviderContainer();
      final notifier = container.read(chatsProvider.notifier);

      final future = notifier.getResponse('Prompt text');
      expect(notifier.isLoading, true);

      await future;
      expect(notifier.isLoading, false);
    });

    test('getResponse handles empty response gracefully', () async {
      final container = ProviderContainer();
      final notifier = container.read(chatsProvider.notifier);

      final response = await notifier.getResponse('Prompt text');

      final chats = container.read(chatsProvider);
      expect(chats, [Message(text: '', isUser: false)]);
      expect(response?.text, '');
    });
  });
}
