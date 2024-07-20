import 'dart:developer';

import 'package:mivro/providers/chat_provider.dart';
import 'package:mivro/widgets/chat_item.dart';
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
    final chatlist = ref.watch(chatsProvider);
    void sendPromptAndGetResponse() async {
      log('in send prompt');
      await ref.read(chatsProvider.notifier).getResponse(_userMessage.text);
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    }

    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Column(
        children: [
          Expanded(
            child: Container(
              child: ListView.separated(
                  controller: _scrollController,
                  scrollDirection: Axis.vertical,
                  itemBuilder: (context, idx) => ChatItem(idx: idx),
                  separatorBuilder: (context, idx) =>
                      const Padding(padding: EdgeInsets.only(top: 10)),
                  itemCount: chatlist.length),
            ),
          ),
          Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 16).copyWith(bottom: 8),
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
                  onPressed: sendPromptAndGetResponse,
                  icon: const Icon(Icons.send),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
