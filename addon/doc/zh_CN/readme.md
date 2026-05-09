# Clipspeak


## 信息
* 作者：“Rui Fontes、Ángelo Abrantes、Abel Passos Júnior 以及 Noelia Ruiz Martínez 的合作，基于 Damien Sykes-Lindley 的作品
* 2024年11月6日更新
* 下载[稳定版本][1]
* 兼容性：NVDA 2019.3 及更高版本


## 介绍
Clipspeak 是一个插件，它允许 NVDA 自动报告剪贴板操作（例如剪切、复制和粘贴），以及其他常见的编辑操作，例如撤消和重做。
为了防止在不适当的情况下进行公告，Clipspeak 会对控件和剪贴板进行检查，以便做出是否需要进行此类公告的明智决定。
您可以在 NVDA 设置中的 Clipspeak 分类下，选择仅报告复制/剪切/粘贴，或者同时报告复制/剪切/粘贴的内容。
默认情况下，Clipspeak 的手势与 Windows 英文版常用的手势相对应：
* CTRL+Z；撤销
* CTRL+Y：重做
* CTRL+X：剪切
* CTRL+C：复制
* CTRL+SHIFT+C：复制文件路径（仅限 Windows 11）
* CTRL+V：粘贴

如果这些不是您的 Windows 版本上执行这些任务的常用快捷方式，您将需要在输入手势设置中的 Clipspeak 类别下中重新映射这些手势。


[1]: https://github.com/ruifontes/clipspeak/releases/download/2025.06.13/clipspeak-2024.06.11.nvda-addon
