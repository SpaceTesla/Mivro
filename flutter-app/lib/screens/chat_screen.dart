import 'dart:developer';

import 'package:mivro/models/message.dart';
import 'package:mivro/providers/chat_history_provider.dart';
import 'package:mivro/providers/chat_provider.dart';
import 'package:mivro/widgets/chat/chat_item.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ChatbotScreen extends ConsumerStatefulWidget {
  const ChatbotScreen({super.key});

  @override
  ConsumerState<ConsumerStatefulWidget> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends ConsumerState<ChatbotScreen> {
  final _userMessage = TextEditingController();
  final _scrollController = ScrollController();

  @override
  Widget build(BuildContext context) {
    final isLoading = ref.watch(chatsProvider.notifier).isLoading;
    List<Message> messages = ref.watch(chatHistoryProvider);

    void sendPromptAndGetResponse() async {
      FocusScope.of(context).unfocus();
      var userPrompt = _userMessage.text;
      _userMessage.clear();
      log('in send prompt');

      setState(() {
        ref
            .read(chatHistoryProvider.notifier)
            .addMessage(Message(text: userPrompt, isUser: true));
        WidgetsBinding.instance.addPostFrameCallback((_) {
          _scrollController.animateTo(
            _scrollController.position.maxScrollExtent,
            duration: const Duration(milliseconds: 500),
            curve: Curves.easeInOut,
          );
        });
      });
      log(userPrompt);
      var responseMessage =
          await ref.read(chatsProvider.notifier).getResponse(userPrompt);
      log(responseMessage!.text);
      setState(() {
        ref.read(chatHistoryProvider.notifier).addMessage(responseMessage);
      });

      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 500),
          curve: Curves.easeInOut,
        );
      });
    }

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            Expanded(
              child: Container(
                child: ListView.separated(
                    controller: _scrollController,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (context, idx) {
                      if (idx < messages.length) {
                        return ChatItem(message: messages[idx]);
                      } else if (isLoading) {
                        return const Center(
                            child: CircularProgressIndicator());
                      } else {
                        return const SizedBox.shrink();
                      }
                    },
                    separatorBuilder: (context, idx) =>
                        const Padding(padding: EdgeInsets.only(top: 10)),
                    itemCount: messages.length),
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16)
                  .copyWith(bottom: 8),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                color: Colors.white,
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      decoration: const InputDecoration(
                          hintText: 'Start your conversation here...',
                          labelStyle: TextStyle(color: Colors.black),
                          filled: true,
                          fillColor: Colors.white,
                          border: InputBorder.none),
                      keyboardType: TextInputType.text,
                      controller: _userMessage,
                    ),
                  ),
                  IconButton(
                    onPressed: () {},
                    icon: const Icon(Icons.mic),
                  ),
                  IconButton(
                    onPressed: sendPromptAndGetResponse,
                    icon: const Icon(Icons.send),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
