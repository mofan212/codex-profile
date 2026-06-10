function parseJsonEnv(name, text) {
  try {
    return JSON.parse(text);
  } catch (error) {
    const wrapped = new Error(`${name} must be valid JSON: ${error.message}`);
    wrapped.code = "INVALID_JSON_ENV";
    wrapped.envVar = name;
    throw wrapped;
  }
}

function requirePlainObject(name, value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    const error = new Error(`${name} must be a JSON object`);
    error.code = "INVALID_JSON_ENV";
    error.envVar = name;
    throw error;
  }
  return value;
}

function parseTimeout(text) {
  if (!text) {
    return undefined;
  }
  const timeoutMs = Number(text);
  if (!Number.isInteger(timeoutMs) || timeoutMs <= 0) {
    const error = new Error("REQUEST_TIMEOUT_MS must be a positive integer");
    error.code = "INVALID_TIMEOUT";
    error.envVar = "REQUEST_TIMEOUT_MS";
    throw error;
  }
  return timeoutMs;
}

function targetHostFrom(url) {
  try {
    return new URL(url).host || undefined;
  } catch {
    return undefined;
  }
}

function redactSensitive(value) {
  if (Array.isArray(value)) {
    return value.map(redactSensitive);
  }
  if (!value || typeof value !== "object") {
    return value;
  }

  return Object.fromEntries(Object.entries(value).map(([key, entry]) => {
    if (/cookie|token|secret|password|passwd|authorization|api[-_]?key/i.test(key)) {
      return [key, "<redacted>"];
    }
    return [key, redactSensitive(entry)];
  }));
}

let url;
let requestSent = false;
let timeoutId;
let timeoutTriggered = false;

try {
  url = process.env.REQUEST_URL;
  const method = process.env.REQUEST_METHOD || "POST";
  const cookie = process.env.REQUEST_COOKIE;
  const bodyText = process.env.REQUEST_BODY || "{}";
  const headersText = process.env.REQUEST_HEADERS || "{}";
  const timeoutMs = parseTimeout(process.env.REQUEST_TIMEOUT_MS);

  if (!url) {
    const error = new Error("REQUEST_URL is required");
    error.code = "MISSING_REQUEST_URL";
    error.envVar = "REQUEST_URL";
    throw error;
  }

  const extraHeaders = requirePlainObject("REQUEST_HEADERS", parseJsonEnv("REQUEST_HEADERS", headersText));
  const parsedBody = parseJsonEnv("REQUEST_BODY", bodyText);
  const body = method.toUpperCase() === "GET" || method.toUpperCase() === "HEAD"
    ? undefined
    : JSON.stringify(parsedBody);

  const headers = {
    "content-type": "application/json;charset=UTF-8",
    accept: "application/json, text/plain, */*",
    ...extraHeaders,
    ...(cookie ? { cookie } : {}),
  };

  const controller = timeoutMs ? new AbortController() : undefined;
  timeoutId = timeoutMs
    ? setTimeout(() => {
        timeoutTriggered = true;
        controller.abort();
      }, timeoutMs)
    : undefined;

  requestSent = true;
  const response = await fetch(url, {
    method,
    headers,
    body,
    signal: controller?.signal,
  });
  clearTimeout(timeoutId);

  const text = await response.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = text;
  }

  console.log(JSON.stringify({
    httpStatus: response.status,
    httpStatusText: response.statusText,
    response: redactSensitive(parsed),
  }));
} catch (error) {
  clearTimeout(timeoutId);
  console.error(JSON.stringify({
    status: "error",
    code: timeoutTriggered ? "REQUEST_TIMEOUT" : error.code || "REQUEST_FAILED",
    error: error.message,
    envVar: error.envVar,
    targetHost: typeof url === "string" ? targetHostFrom(url) : undefined,
    requestSent,
    cause: error.cause ? String(error.cause) : undefined,
  }));
  process.exitCode = 1;
}
