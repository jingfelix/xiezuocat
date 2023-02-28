# xiezuocat

Reversed API for [写作猫](https://xiezuocat.com/chat).

## Usage

获取 cookies。建议从调试工具中将请求复制为 cURL 格式，再使用 [curl转换工具](https://tool.lu/curl/) 转换为 Python 代码。

以下为一个示例：

```python
cookies = {
    "Hm_lvt_099c1a390e23e6b73b081c48519f6e8e":None,
    "headimgurl":None,
    "nickname":None,
    "traceid":None,
    "sid":None,
    "uid":None,
    "Hm_lpvt_099c1a390e23e6b73b081c48519f6e8e":None,
    "JSESSIONID":None,
}
```

设置 cookies 后，可使用仓库目录下的 chat 文件进行对话。

```bash
$ ./chat

You: 你好
Bot: 你好！今天我能为您做些什么？有什么我可以帮助您的？请告诉我，我会尽力回答您的问题。

You: 你能帮我写一封推荐信么
Bot: 当然可以。请告诉我你需要写一封推荐信来提升自己，我很乐意为你提供帮助。
这是一种简单的方法，只需要列出你的优势，如学习能力、沟通能力等。但是，如果你想要更具体地描述你的优势，可以考虑使用“具体表现”一词。
例如，“你的学习能力很强，能够很快掌握新知识”，或者“你的工作能力很强，能够迅速完成任务”。同样地，“你的沟通能力很强，能够有效地与他人进行交流”。
最后，请确保信的内容清晰、准确、及时地表达您的意图。如果您需要更详细的信息，请与更多专家或组织联系以获取更多信息。
```

## Development

目前采用的方法是：

- 一次 `/ai-chat` 请求获取 `session_id`，接下来均使用这一变量

- 每次对话中，请求 `/ai-chat` 获取 `history_id` 和 `doc_id`，并将其作为下一次请求的参数

- 同一轮对话的 session_id 相同，但是每次问答的 history_id 和 doc_id 均不同
