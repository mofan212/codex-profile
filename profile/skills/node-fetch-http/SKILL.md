---
name: node-fetch-http
description: Use Node.js built-in fetch in Codex to call, test, verify, POST to, or inspect HTTP/API endpoints, especially for Cookie, Bearer Token, JSON body, chained requests, reusable request scripts, or response validation. Do not try PowerShell Invoke-WebRequest or Windows curl.exe first, and do not install node-fetch.
---

# 1. Node Fetch HTTP

在 Codex 中调用 HTTP/API 接口时，默认使用 Node.js 内置 `fetch` 作为 HTTP 客户端。

这个 Skill 只沉淀工具选择和请求习惯，不绑定任何具体业务接口。

# 2. 核心规则

- 优先使用 Node.js 内置 `fetch` 调用 HTTP/API 接口。
- 不要安装或导入 npm 包 `node-fetch`。
- 除非用户明确要求，否则不要先尝试 PowerShell `Invoke-WebRequest` 或 Windows `curl.exe`。
- PowerShell 只作为启动 Node 脚本的外壳使用。
- `Cookie`、`Authorization`、Bearer Token、API Key 等敏感值优先通过环境变量传入。
- 不要把敏感值写入可复用脚本、生成产物、日志或最终回复。
- 多步骤或串联接口请求，创建小型 `.mjs` 脚本，不要把复杂请求逻辑塞进一条超长命令。
- 输出紧凑 JSON，包含 HTTP 状态、状态文本、可解析响应、原始文本兜底和关键错误。

# 3. Node 选择

按以下顺序选择 Node：

1. 如果可以通过 `load_workspace_dependencies` 获取 Codex 工作区依赖，优先使用其中的 Node 可执行文件。
2. 否则使用 `where.exe node` 找到的本机 `node.exe`。
3. 如果没有可用 Node，直接报告阻塞，不要回退到不相关的 HTTP 工具。

# 4. 请求模式

一次性 JSON 请求可以使用 `scripts/fetch-json.mjs` 这类脚本模板。

输入环境变量：

- `REQUEST_URL`: URL.
- `REQUEST_METHOD`: HTTP 方法，默认 `POST`。
- `REQUEST_BODY`: JSON 请求体，默认 `{}`。
- `REQUEST_COOKIE`: 可选 Cookie 请求头。
- `REQUEST_HEADERS`: 可选 JSON 对象，会合并进请求头。

默认请求头：

```json
{
  "content-type": "application/json;charset=UTF-8",
  "accept": "application/json, text/plain, */*"
}
```

如果接口依赖浏览器上下文，通过 `REQUEST_HEADERS` 添加 `Origin` 和 `Referer`。

# 5. 输出模式

返回或总结以下信息：

- `httpStatus`
- `httpStatusText`
- 可解析的 JSON 响应；如果响应不是 JSON，则返回原始文本
- 业务字段，例如 `status`、`code`、`message`、`traceId`

避免回显敏感值。如果命令输出中包含凭证，展示给用户前先脱敏。

# 6. 校验

单次请求：

- 确认 HTTP 状态。
- 确认响应体是否为有效 JSON。
- 如果响应体中有业务状态字段，将业务状态和 HTTP 状态分开说明。

串联请求：

- 只有在有用时，才把后续步骤需要的非敏感响应数据保存到工作区临时文件。
- 复用同一个请求 helper 和请求头。
- 校验最终结果的数量、标识符和差异。

# 7. 常用 PowerShell 启动方式

在当前命令中设置环境变量，运行 Node，然后移除敏感变量：

```powershell
$env:REQUEST_URL = 'https://example.com/api'
$env:REQUEST_METHOD = 'POST'
$env:REQUEST_COOKIE = '<cookie value>'
$env:REQUEST_BODY = '{"id":"123"}'
$env:REQUEST_HEADERS = '{"Origin":"https://example.com","Referer":"https://example.com/"}'
& '<node.exe path>' '<skill path>\scripts\fetch-json.mjs'
Remove-Item Env:\REQUEST_URL
Remove-Item Env:\REQUEST_METHOD
Remove-Item Env:\REQUEST_COOKIE
Remove-Item Env:\REQUEST_BODY
Remove-Item Env:\REQUEST_HEADERS
```

使用 PowerShell 文件读写命令时，必须显式添加 `-Encoding UTF8`。
