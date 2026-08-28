---
name: node-http-fetch
description: 使用 Node.js 内置 `fetch` 调用、测试和验证 HTTP/API 接口。当请求涉及 Cookie、Bearer Token、API Key、JSON 请求体、串联调用、响应校验或可复用请求脚本时，使用该 Skill。优先复用 `scripts/fetch-json.mjs`；副作用接口执行前确认；不要安装 `node-fetch`。
---

# Node HTTP Fetch

## 1. 执行流程

1. 按 [副作用门禁](#2-副作用门禁) 判断请求是否可以立即执行。
2. 优先使用工作区 Node；不可用时使用 `where.exe node` 查找本机 Node。找不到 Node 时报告阻塞；未经用户同意，不安装依赖或切换 HTTP 客户端。
3. JSON 请求优先运行 [scripts/fetch-json.mjs](scripts/fetch-json.mjs)；串联请求复用同一请求 helper；文件上传、表单、二进制或 raw body 使用专用 `.mjs` 脚本。
4. 通过环境变量传入请求参数；敏感值不得写入可复用脚本、生成产物、日志或最终回复。
5. 读取紧凑 JSON 输出，分开说明 HTTP 状态、业务状态和错误信息，展示前检查脱敏结果。

使用 Node.js 内置 `fetch`，不要安装或导入 `node-fetch`。除非用户明确指定，否则不要先使用 PowerShell `Invoke-WebRequest` 或 Windows `curl.exe`；PowerShell 只作为启动 Node 脚本的外壳。

## 2. 副作用门禁

根据接口语义判断副作用，不只看 HTTP 方法。只读查询、登录态检查和结果校验可以直接执行；创建、修改、删除、提交、审批、支付、发消息、触发任务、清缓存、重跑作业和生产配置变更属于副作用。

| trigger | action | continue_when |
| --- | --- | --- |
| 请求会产生副作用 | 🛑 STOP：确认目标环境、URL、方法、请求体、影响对象和是否立即执行 | 用户明确确认执行边界 |
| 目标疑似生产环境，且请求不是明确只读 | 🛑 STOP：确认账号权限、影响范围和回滚方式 | 用户确认风险和执行范围 |
| URL、方法、认证方式、请求体或预期结果不完整 | 🛑 STOP：补齐缺失参数，不猜测执行 | 执行参数完整且无冲突 |

用户要求只生成脚本或命令时，仅生成可审查内容，不调用接口。

## 3. JSON 请求契约

一次性 JSON 请求使用 [scripts/fetch-json.mjs](scripts/fetch-json.mjs)：

| env_var | meaning |
| --- | --- |
| `REQUEST_URL` | 请求 URL，必填 |
| `REQUEST_METHOD` | HTTP 方法，默认 `POST` |
| `REQUEST_BODY` | JSON 请求体，默认 `{}` |
| `REQUEST_COOKIE` | 可选 Cookie 请求头 |
| `REQUEST_HEADERS` | 可选 JSON 请求头对象 |
| `REQUEST_TIMEOUT_MS` | 可选正整数超时毫秒数 |

接口依赖浏览器来源校验时，通过 `REQUEST_HEADERS` 添加 `Origin` 和 `Referer`。

`multipart/form-data`、文件上传、表单、二进制响应或 raw body 不得套用该模板。生成专用脚本后，先确认请求体、`Content-Type` 和副作用，再决定是否执行。

## 4. 失败与输出

- 参数错误以脚本的非零退出码和错误 JSON 为准；给出可复制的修正方式。
- 网络、DNS、TLS 或超时失败时，说明错误类型、目标主机和请求是否已经发出；副作用请求不得自动重试。
- 响应不是 JSON 时保留原始文本兜底，不把解析失败解释为业务失败。
- 分开报告 `httpStatus`、`httpStatusText` 与响应中的 `status`、`code`、`message`、`traceId` 等业务字段。
- 不回显 Cookie、Token、API Key、密码或其他敏感值；脚本输出已脱敏时仍需复核摘要。
- 串联请求只在确有需要时保存非敏感中间数据，并校验最终数量、标识符和差异。
