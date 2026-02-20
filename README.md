# DeepSeek-Toolkit

本项目使用 Selenium 控制浏览器自动访问 DeepSeek Chat 网页，发送用户输入的消息并获取回答，最终将回答内容打印到控制台。

| 说明：作者个人使用的适合夸克浏览器，其他浏览器必须是谷歌内核

## 📖 功能说明

- 自动启动浏览器（基于 Chromium）
- 加载 DeepSeek Chat 页面（https://chat.deepseek.com/）
- 接收用户输入的问题并发送
- 等待并捕获 AI 的回答（支持长回答流式检测）
- 回答稳定后自动退出浏览器

## ⚙️ 环境配置

### 1. 代码构建

```bash
git clone https://github.com/sglwsjxh/deepseek-toolkit.git
cd deepseek-toolkit

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 下载 ChromeDriver

Quark 浏览器基于 Chromium，因此需要使用 ChromeDriver 来控制。请根据你的浏览器版本下载对应的 ChromeDriver：

- 查看浏览器谷歌内核版本：打开浏览器，地址栏输入 `chrome://version/`，查看第一行版本号。
- 下载对应版本的 ChromeDriver：[ChromeDriver 下载页](https://sites.google.com/chromium.org/driver/)
- 将下载的 `chromedriver.exe` 放置到合适位置，并记住路径。

> 注意：如果版本不匹配可能导致控制失败。

## 🔧 运行前必须修改的配置

打开 `main.py`，找到以下三个路径变量，修改为你的实际路径：

```python
quark_path = r"D:\Apps\Quark\quark.exe"           # 浏览器可执行文件路径
driver_path = r"C:\...\chromedriver.exe"          # ChromeDriver 路径
user_data_dir = r"C:\...\Quark\User Data"         # 浏览器用户数据目录（用于保持登录状态），通常在AppData目录下
```

## 🚀 使用方法

在终端运行脚本：

```bash
python main.py
```

## 📝 注意事项

- 首次运行可能需要手动登录 DeepSeek（因为使用了用户数据目录，后续可保持登录状态）
- 脚本以无头模式运行（`--headless`），浏览器不会显示界面。如需查看运行过程，可删除 `options.add_argument("--headless")` 这一行。
- 默认最长等待回答时间为 300 秒，可修改 `max_wait` 变量。