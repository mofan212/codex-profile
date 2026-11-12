import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";

const source = await readFile(new URL("../../../profile/skills/node-http-fetch/scripts/fetch-json.mjs", import.meta.url), "utf8");
const credential = "DUMMY_CREDENTIAL_47";

async function runRequest({ env = {}, fetch, timers = {} }) {
  const output = [];
  const errors = [];
  const process = {
    env: { REQUEST_URL: "https://example.invalid/api", REQUEST_METHOD: "GET", ...env },
    exitCode: 0,
  };
  await vm.runInNewContext(`(async () => {${source}\n})()`, {
    process,
    console: { log: line => output.push(line), error: line => errors.push(line) },
    URL,
    AbortController,
    setTimeout,
    clearTimeout,
    fetch,
    ...timers,
  });
  return { exitCode: process.exitCode, output, errors };
}

test("响应头返回后，响应体读取仍受请求超时约束", async () => {
  let deadline;
  const result = await runRequest({
    env: { REQUEST_TIMEOUT_MS: "10" },
    timers: {
      setTimeout: callback => { deadline = callback; return 1; },
      clearTimeout: () => { deadline = undefined; },
    },
    fetch: async (_url, { signal }) => ({
      status: 200,
      statusText: "OK",
      text: () => new Promise((resolve, reject) => {
        signal.addEventListener("abort", () => reject(signal.reason), { once: true });
        deadline?.();
        resolve('{"ok":true}');
      }),
    }),
  });
  assert.equal(result.exitCode, 1);
  assert.equal(JSON.parse(result.errors[0]).code, "REQUEST_TIMEOUT");
  assert.equal(result.output.length, 0);
});

test("非 JSON 响应只输出摘要，不记录原始凭据", async () => {
  const text = `Authorization: Bearer ${credential}`;
  const result = await runRequest({
    fetch: async () => ({ status: 200, statusText: "OK", text: async () => text }),
  });
  assert.equal(result.exitCode, 0);
  assert.ok(!result.output.join("").includes(credential));
  const output = JSON.parse(result.output[0]);
  assert.equal(output.httpStatus, 200);
  assert.deepEqual(output.response, { type: "non-json", length: text.length });
});

test("无效 JSON 参数的错误输出不包含原始输入", async () => {
  const result = await runRequest({
    env: { REQUEST_HEADERS: credential },
    fetch: async () => { assert.fail("参数无效时不得发送请求"); },
  });
  assert.equal(result.exitCode, 1);
  assert.equal(JSON.parse(result.errors[0]).code, "INVALID_JSON_ENV");
  assert.ok(!result.errors.join("").includes(credential));
});

test("请求异常不回显可能包含凭据的 message 或 cause", async () => {
  const result = await runRequest({
    fetch: async () => {
      const cause = new Error(`TLS diagnostic ${credential}`);
      cause.code = "CERT_HAS_EXPIRED";
      throw new TypeError(`Cannot fetch ${credential}`, { cause });
    },
  });
  assert.equal(result.exitCode, 1);
  assert.ok(!result.errors.join("").includes(credential));
  assert.equal(JSON.parse(result.errors[0]).cause, "CERT_HAS_EXPIRED");
});

test("JSON 响应保留业务字段，并递归遮蔽对象和数组中的敏感字段", async () => {
  const result = await runRequest({
    fetch: async () => ({
      status: 403,
      statusText: "Forbidden",
      text: async () => JSON.stringify({
        code: "DENIED",
        token: credential,
        items: [{ api_key: credential, count: 2 }],
      }),
    }),
  });
  assert.equal(result.exitCode, 0);
  assert.deepEqual(JSON.parse(result.output[0]), {
    httpStatus: 403,
    httpStatusText: "Forbidden",
    response: { code: "DENIED", token: "<redacted>", items: [{ api_key: "<redacted>", count: 2 }] },
  });
});
