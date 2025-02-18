# plugins/ApiCallerPlugin/main.py
import requests
from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived

# 注册插件
@register(name="ApiCallerPlugin", description="调用本地API并返回结果", version="1.0", author="YourName")
class ApiCallerPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        super().__init__(host)  # 初始化 BasePlugin 并传递 host 参数
        self.host = host  # 保存 host 对象，用于后续可能的调用

    # 异步初始化（可选）
    async def initialize(self):
        pass  # 如果需要在插件加载时执行初始化逻辑，可以在这里实现

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message.strip()  # 获取消息内容并去除首尾空格
        if msg.startswith("!api_call"):  # 如果消息以 "!api_call" 开头
            result = self.call_api()  # 调用本地API
            ctx.add_return("reply", [result])  # 将API调用结果添加到回复队列
            ctx.prevent_default()  # 阻止默认行为（如向接口获取回复）

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message.strip()  # 获取消息内容并去除首尾空格
        if msg.startswith("!api_call"):  # 如果消息以 "!api_call" 开头
            result = self.call_api()  # 调用本地API
            ctx.add_return("reply", [result])  # 将API调用结果添加到回复队列
            ctx.prevent_default()  # 阻止默认行为（如向接口获取回复）

    # 调用本地API的方法
    def call_api(self):
        try:
            response = requests.get("http://localhost:8080/api")  # 调用本地API
            response.raise_for_status()  # 检查请求是否成功
            return f"API调用成功！返回结果：{response.json()}"  # 返回API的JSON结果
        except Exception as e:
            return f"API调用失败：{e}"  # 返回错误信息

    # 插件卸载时触发
    def __del__(self):
        pass  # 如果需要在插件卸载时执行清理逻辑，可以在这里实现
