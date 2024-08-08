import 'package:mivro/models/message.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mivro/utils/hexcolor.dart';

class ChatItem extends ConsumerWidget {
  final Message message;
  const ChatItem({super.key, required this.message});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    var width = MediaQuery.of(context).size.width;

    return Container(
      padding: const EdgeInsets.all(8),
      child: message.isUser
          ? Align(
              alignment: Alignment.centerRight,
              child: Container(
                decoration: BoxDecoration(
                  color: myColorFromHex('#95D2B3'),
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(20),
                    bottomLeft: Radius.circular(20),
                    bottomRight: Radius.circular(20),
                  ),
                  border:
                      Border.all(color: myColorFromHex('#0D7377'), width: 2),
                ),
                alignment: Alignment.topRight,
                constraints: BoxConstraints(
                  maxWidth: width * 2 / 3,
                ),
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Column(
                    children: [
                      // Align(
                      //   alignment: Alignment.centerRight,
                      //   child: Text(
                      //     'You',
                      //     style: TextStyle(
                      //         color: myColorFromHex('#0D7377'), fontSize: 16),
                      //   ),
                      // ),
                      Align(
                        alignment: Alignment.centerRight,
                        child: Text(
                          message.text,
                          style: const TextStyle(
                              fontSize: 16, color: Colors.black),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            )
          : message.text == 'Hello @areeb! How can I help you?'
              ? Align(
                  alignment: Alignment.centerLeft,
                  child: Container(
                    decoration: BoxDecoration(
                      color: myColorFromHex('#F8EDE3'),
                      borderRadius: const BorderRadius.only(
                        topRight: Radius.circular(20),
                        bottomLeft: Radius.circular(20),
                        bottomRight: Radius.circular(20),
                      ),
                      // border:
                      //     Border.all(color: myColorFromHex('#0D7377'), width: 2),
                    ),
                    alignment: Alignment.topLeft,
                    constraints: BoxConstraints(
                      maxWidth: width * 2 / 3,
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Column(
                        children: [
                          // const Align(
                          //   alignment: Alignment.centerLeft,
                          //   child: Text.rich(
                          //     TextSpan(
                          //       children: [
                          //         TextSpan(
                          //           text: 'm',
                          //           style: TextStyle(
                          //               color: Color(0xFFE83A4F)), // Red color
                          //         ),
                          //         TextSpan(
                          //           text: 'i',
                          //           style: TextStyle(
                          //               color: Color(0xFFF79C26)), // Orange color
                          //         ),
                          //         TextSpan(
                          //           text: 'v',
                          //           style: TextStyle(
                          //               color: Color(0xFF81C341)), // Green color
                          //         ),
                          //         TextSpan(
                          //           text: 'r',
                          //           style: TextStyle(
                          //               color: Color(0xFF4FAFDC)), // Blue color
                          //         ),
                          //         TextSpan(
                          //           text: 'o',
                          //           style: TextStyle(
                          //               color: Color(0xFF4FAFDC)), // Blue color
                          //         ),
                          //       ],
                          //     ),
                          //     style: TextStyle(
                          //       fontSize: 16,
                          //       fontWeight: FontWeight.bold,
                          //     ),
                          //   ),
                          // ),
                          Align(
                            alignment: Alignment.center,
                            child: Text(
                              message.text,
                              style: const TextStyle(
                                  fontSize: 32, color: Colors.black),
                            ),
                          )
                        ],
                      ),
                    ),
                  ),
                )
              : Align(
                  alignment: Alignment.centerLeft,
                  child: Container(
                    decoration: BoxDecoration(
                      color: myColorFromHex('#EEF1FF'),
                      borderRadius: const BorderRadius.only(
                        topRight: Radius.circular(20),
                        bottomLeft: Radius.circular(20),
                        bottomRight: Radius.circular(20),
                      ),
                      border:
                          Border.all(color: myColorFromHex('#0D7377'), width: 2),
                    ),
                    alignment: Alignment.topLeft,
                    constraints: BoxConstraints(
                      maxWidth: width * 4/ 5,
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Column(
                        children: [
                          // const Align(
                          //   alignment: Alignment.centerLeft,
                          //   child: Text.rich(
                          //     TextSpan(
                          //       children: [
                          //         TextSpan(
                          //           text: 'm',
                          //           style: TextStyle(
                          //               color: Color(0xFFE83A4F)), // Red color
                          //         ),
                          //         TextSpan(
                          //           text: 'i',
                          //           style: TextStyle(
                          //               color: Color(0xFFF79C26)), // Orange color
                          //         ),
                          //         TextSpan(
                          //           text: 'v',
                          //           style: TextStyle(
                          //               color: Color(0xFF81C341)), // Green color
                          //         ),
                          //         TextSpan(
                          //           text: 'r',
                          //           style: TextStyle(
                          //               color: Color(0xFF4FAFDC)), // Blue color
                          //         ),
                          //         TextSpan(
                          //           text: 'o',
                          //           style: TextStyle(
                          //               color: Color(0xFF4FAFDC)), // Blue color
                          //         ),
                          //       ],
                          //     ),
                          //     style: TextStyle(
                          //       fontSize: 16,
                          //       fontWeight: FontWeight.bold,
                          //     ),
                          //   ),
                          // ),
                          Align(
                            alignment: Alignment.centerLeft,
                            child: Text(
                              message.text,
                              style: const TextStyle(
                                  fontSize: 16, color: Colors.black),
                            ),
                          )
                        ],
                      ),
                    ),
                  ),
                ),
    );
  }
}
