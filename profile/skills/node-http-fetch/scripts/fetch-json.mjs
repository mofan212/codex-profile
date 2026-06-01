const url = process.env.REQUEST_URL;
const method = process.env.REQUEST_METHOD || "POST";
const cookie = process.env.REQUEST_COOKIE;
const bodyText = process.env.REQUEST_BODY || "{}";
const headersText = process.env.REQUEST_HEADERS || "{}";

if (!url) {
  throw new Error("REQUEST_URL is required");
}

function parseJsonEnv(name, text) {
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`${name} must be valid JSON: ${error.message}`);
  }
}

const extraHeaders = parseJsonEnv("REQUEST_HEADERS", headersText);
const body = method.toUpperCase() === "GET" || method.toUpperCase() === "HEAD"
  ? undefined
  : JSON.stringify(parseJsonEnv("REQUEST_BODY", bodyText));

const headers = {
  "content-type": "application/json;charset=UTF-8",
  accept: "application/json, text/plain, */*",
  ...extraHeaders,
  ...(cookie ? { cookie } : {}),
};

try {
  const response = await fetch(url, {
    method,
    headers,
    body,
  });
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
    response: parsed,
  }));
} catch (error) {
  console.error(JSON.stringify({
    error: error.message,
    cause: error.cause ? String(error.cause) : undefined,
  }));
  process.exitCode = 1;
}
