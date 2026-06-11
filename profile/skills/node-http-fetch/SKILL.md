---
name: node-http-fetch
description: 使用 Node.js 内置 `fetch` 调用、测试、检查和验证 HTTP/API 接口。当请求涉及 Cookie、Bearer Token、API Key、JSON 请求体、串联调用、可复用脚本或响应校验时，使用该 Skill。默认使用 Node.js 内置 `fetch`，不要先用 PowerShell `Invoke-WebRequest` 或 Windows `curl.exe`，也不要安装 `node-fetch`。
---

# 1. Node HTTP Fetch

调用 HTTP/API 接口时，默认使用 Node.js 内置 `fetch` 作为 HTTP 客户端。

这个 Skill 只沉淀工具选择和请求习惯，不绑定任何具体业务接口。

# 2. 核心规则

- 优先使用 Node.js 内置 `fetch`；不要安装或导入 `node-fetch`
- 除非用户明确要求，否则不要先尝试 PowerShell `Invoke-WebRequest` 或 Windows `curl.exe`
- PowerShell 只作为启动 Node 脚本的外壳使用
- `Cookie`、`Authorization`、Bearer Token、API Key 等敏感值优先通过环境变量传入；不要写入可复用脚本、生成产物、日志或最终回复
- 多步骤或串联接口请求使用小型 `.mjs` 脚本，不要把复杂请求逻辑塞进一条超长命令
- 输出紧凑 JSON，包含 HTTP 状态、状态文本、可解析响应、原始文本兜底和关键错误

# 3. 执行顺序

1. 判断请求是否有副作用；命中检查点时先停下确认，不执行请求
2. 选择 Node：当前运行环境提供工作区依赖发现工具时优先使用工作区 Node；否则使用本机 `node.exe`；找不到 Node 时报告阻塞
3. 将 URL、方法、请求体、Cookie 和额外请求头放入环境变量；敏感值不得写入脚本文件
4. 运行 `scripts/fetch-json.mjs` 或同类小型 `.mjs` 脚本
5. 读取脚本输出的紧凑 JSON，分开说明 HTTP 状态、业务状态和错误信息；展示前先脱敏

# 4. 副作用接口检查点

先根据接口语义判断是否有副作用，不只看 HTTP 方法。只读查询、登录态检查和结果校验通常不是副作用；创建、修改、删除、提交、审批、支付、发消息、触发任务、清缓存、重跑作业、生产环境配置变更都属于副作用。

| trigger | CHECKPOINT |
| --- | --- |
| 请求会创建、修改、删除、提交、审批、支付、发消息或触发任务 | 🛑 STOP：先向用户确认目标环境、URL、方法、请求体、影响对象和是否立即执行 |
| 请求目标疑似生产环境，且接口不是明确只读查询 | 🛑 STOP：先确认环境、账号权限、影响范围和回滚方式 |
| 用户只给了接口名、截图、口头描述或不完整参数 | 🛑 STOP：先补齐 URL、方法、认证方式、请求体和预期结果，不猜测执行 |
| 用户明确要求先生成脚本或命令但不要调用 | 只生成可审查脚本或命令，不执行请求 |

# 5. Node 选择

当前运行环境提供工作区依赖发现工具时，优先使用其返回的工作区 Node。不可用或未提供时，使用 `where.exe node` 找到的本机 `node.exe`。如果没有可用 Node，直接报告阻塞和已检查路径，不要回退到不相关的 HTTP 工具。

# 6. 请求模式

一次性 JSON 请求可以使用 [scripts/fetch-json.mjs](scripts/fetch-json.mjs) 这类脚本模板。

这个模板只处理 JSON 请求体。遇到 `multipart/form-data`、文件上传、表单提交、二进制响应或任意 raw body 时，不要强行套用 `fetch-json.mjs`；先生成专用 `.mjs` 脚本并让用户确认请求体、`Content-Type` 和副作用。

| env_var | meaning |
| --- | --- |
| `REQUEST_URL` | URL |
| `REQUEST_METHOD` | HTTP 方法，默认 `POST` |
| `REQUEST_BODY` | JSON 请求体，默认 `{}` |
| `REQUEST_COOKIE` | 可选 Cookie 请求头 |
| `REQUEST_HEADERS` | 可选 JSON 对象，会合并进请求头 |
| `REQUEST_TIMEOUT_MS` | 可选正整数；设置后请求超时会中止并输出 `REQUEST_TIMEOUT` |

默认请求头：

```json
{
  "content-type": "application/json;charset=UTF-8",
  "accept": "application/json, text/plain, */*"
}
```

如果接口依赖浏览器上下文，通过 `REQUEST_HEADERS` 添加 `Origin` 和 `Referer`。

`GET` / `HEAD` 请求不会发送 `REQUEST_BODY`；查询参数必须放在 `REQUEST_URL`，不要把查询条件塞进 body。

# 7. 失败处理

| failure | action |
| --- | --- |
| Node 不可用 | 报告阻塞和已检查路径；不要回退到 PowerShell `Invoke-WebRequest`、Windows `curl.exe` 或安装新依赖 |
| `REQUEST_URL` 缺失 | 停止请求；脚本应输出 `status=error`、`code=MISSING_REQUEST_URL`、`envVar=REQUEST_URL`，并返回非零退出码 |
| `REQUEST_HEADERS` 不是 JSON 对象，或 `REQUEST_BODY` 不是合法 JSON | 停止请求；脚本应输出 `status=error`、`code=INVALID_JSON_ENV`、`envVar` 和错误信息，给出可复制的修正版 |
| `REQUEST_TIMEOUT_MS` 不是正整数 | 停止请求；脚本应输出 `status=error`、`code=INVALID_TIMEOUT`、`envVar=REQUEST_TIMEOUT_MS`，并返回非零退出码 |
| 请求失败、DNS 失败、TLS 失败或超时 | 输出 `status=error`、`code=REQUEST_FAILED` 或 `REQUEST_TIMEOUT`、错误类型、`targetHost` 和 `requestSent`；不要重试有副作用请求 |
| 响应不是 JSON | 保留原始文本兜底，说明响应类型；不要把解析失败误报成业务失败 |
| 响应包含敏感值 | 脚本会递归脱敏常见敏感字段名；展示前继续检查摘要，不要把原始凭证写入日志、脚本或最终回复 |

# 8. 输出和校验

| scenario | requirement |
| --- | --- |
| 输出字段 | 返回或总结 `httpStatus`、`httpStatusText`、可解析 JSON 响应或原始文本，以及 `status`、`code`、`message`、`traceId` 等业务字段；错误输出保留 `status`、`code`、`error`、`envVar`、`targetHost`、`requestSent`、`cause` |
| 敏感值 | 避免回显敏感值；如果命令输出中包含凭证，展示给用户前先脱敏 |
| 单次请求 | 确认 HTTP 状态、响应体是否为有效 JSON；如有业务状态字段，将业务状态和 HTTP 状态分开说明 |
| 串联请求 | 只有在有用时，才把后续步骤需要的非敏感响应数据保存到工作区临时文件；复用同一个请求 helper 和请求头；校验最终结果的数量、标识符和差异 |

# 9. 反模式黑名单

- 不要安装或导入 `node-fetch`
- 不要把 Cookie、Bearer Token、API Key 或账号密码写入脚本、日志、生成产物或最终回复
- 不要用一条超长命令承载复杂串联请求
- 不要在 Node 不可用时回退到不相关的 HTTP 工具
- 不要在未确认环境和影响范围时调用有副作用接口
- 不要对有副作用请求自动重试

# 10. 常用 PowerShell 启动方式

在当前命令中设置环境变量，运行 Node，然后移除敏感变量。清理环境变量前先保存 `$LASTEXITCODE`，清理后按原退出码退出，避免掩盖请求失败：

```powershell
$exitCode = 1
try {
  $env:REQUEST_URL = 'https://example.com/api'
  $env:REQUEST_METHOD = 'POST'
  $env:REQUEST_COOKIE = '<cookie value>'
  $env:REQUEST_BODY = '{"id":"123"}'
  $env:REQUEST_HEADERS = '{"Origin":"https://example.com","Referer":"https://example.com/"}'
  $env:REQUEST_TIMEOUT_MS = '30000'
  & '<node.exe path>' '<skill path>\scripts\fetch-json.mjs'
  $exitCode = $LASTEXITCODE
} finally {
  Remove-Item Env:\REQUEST_URL -ErrorAction SilentlyContinue
  Remove-Item Env:\REQUEST_METHOD -ErrorAction SilentlyContinue
  Remove-Item Env:\REQUEST_COOKIE -ErrorAction SilentlyContinue
  Remove-Item Env:\REQUEST_BODY -ErrorAction SilentlyContinue
  Remove-Item Env:\REQUEST_HEADERS -ErrorAction SilentlyContinue
  Remove-Item Env:\REQUEST_TIMEOUT_MS -ErrorAction SilentlyContinue
}
exit $exitCode
```

使用 PowerShell 文件读写命令时，必须显式添加 `-Encoding UTF8`。
