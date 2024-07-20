import 'package:areeb/providers/chat_provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:gap/gap.dart';

class ChatItem extends ConsumerWidget {
  final int idx;
  const ChatItem({super.key, required this.idx});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    var height = MediaQuery.of(context).size.height;
    var width = MediaQuery.of(context).size.width;
    final chatList = ref.watch(chatsProvider);

    return Container(
      padding: const EdgeInsets.all(8),
      child: Column(
        children: [
          Align(
            alignment: Alignment.centerRight,
            child: Container(
              decoration:const BoxDecoration(
                  color: Colors.white,
                  borderRadius: const BorderRadius.only(
                      topLeft: Radius.circular(10),
                      bottomLeft: Radius.circular(10),
                      bottomRight: Radius.circular(10))),
              alignment: Alignment.topRight,
              constraints: BoxConstraints(
                maxWidth: width * 2 / 3,
              ),
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(
                  children: [
                    const Align(
                      alignment: Alignment.centerRight,
                      child: Text(
                        'You',
                        style: TextStyle(color: Colors.black),
                      ),
                    ),
                    Align(
                      alignment: Alignment.centerRight,
                      child: Text(
                        chatList[idx]['prompt'],
                        style: const TextStyle(fontSize: 18, color: Colors.black),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          Gap(height * 0.02),
          Align(
            alignment: Alignment.centerLeft,
            child: Container(
              decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: const BorderRadius.only(
                      topRight: Radius.circular(10),
                      bottomLeft: Radius.circular(10),
                      bottomRight: Radius.circular(10))),
              alignment: Alignment.topLeft,
              constraints: BoxConstraints(
                maxWidth: width * 2 / 3,
              ),
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(
                  children: [
                    const Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Mivro',
                        style: TextStyle(color: Colors.black),
                      ),
                    ),
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        chatList[idx]['response'],
                        style: const TextStyle(fontSize: 18, color: Colors.black),
                      ),
                    )
                  ],
                ),
              ),
            ),
          ),
          // Container(
          //   alignment: Alignment.topLeft,
          //   constraints: BoxConstraints(minWidth: width * 2 / 3),
          //   child: Text(chatList[idx]['response']),
          // )
        ],
      ),
    );
  }
}