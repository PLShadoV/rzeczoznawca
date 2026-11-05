#!/usr/bin/env node
import http from "node:http";
import { createReadStream } from "node:fs";
import { realpath, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { pipeline } from "node:stream/promises";

const args = process.argv.slice(2);
let host = process.env.HOST || "127.0.0.1";
let portText = process.env.PORT || "4173";
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--host" && args[i + 1]) host = args[++i];
  else if (args[i] === "--port" && args[i + 1]) portText = args[++i];
  else {
    console.error("Użycie: npm run dev -- [--host 127.0.0.1] [--port 4173]");
    process.exit(1);
  }
}
if (!/^\d+$/.test(portText) || Number(portText) > 65535) {
  console.error("Port musi być liczbą od 0 do 65535.");
  process.exit(1);
}
const root = await realpath(
  fileURLToPath(new URL("../dist/", import.meta.url)),
);
const contained = (target) =>
  target === root || target.startsWith(root + path.sep);
const mime = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".otf": "font/otf",
  ".pdf": "application/pdf",
  ".webmanifest": "application/manifest+json; charset=utf-8",
};
const server = http.createServer(async (req, res) => {
  function reply(code, message) {
    res.writeHead(code, {
      "Content-Type": "text/plain; charset=utf-8",
      "X-Content-Type-Options": "nosniff",
    });
    res.end(req.method === "HEAD" ? undefined : message);
  }
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.setHeader("Allow", "GET, HEAD");
    reply(405, "Method Not Allowed");
    return;
  }
  try {
    let pathname;
    try {
      pathname = decodeURIComponent((req.url || "/").split("?")[0]);
    } catch {
      reply(400, "Bad Request");
      return;
    }
    if (
      !pathname.startsWith("/") ||
      /[\0\\]/.test(pathname) ||
      pathname.split("/").some((part) => part === ".." || part.startsWith("."))
    ) {
      reply(403, "Forbidden");
      return;
    }
    let filename = path.resolve(root, "." + pathname);
    if (!contained(filename)) {
      reply(403, "Forbidden");
      return;
    }
    filename = await realpath(filename);
    if (!contained(filename)) {
      reply(403, "Forbidden");
      return;
    }
    let info = await stat(filename);
    if (info.isDirectory()) {
      filename = await realpath(path.join(filename, "index.html"));
      if (!contained(filename)) {
        reply(403, "Forbidden");
        return;
      }
      info = await stat(filename);
    }
    if (!info.isFile()) {
      reply(404, "Not Found");
      return;
    }
    res.writeHead(200, {
      "Content-Type":
        mime[path.extname(filename).toLowerCase()] ||
        "application/octet-stream",
      "Content-Length": info.size,
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    });
    if (req.method === "HEAD") res.end();
    else await pipeline(createReadStream(filename), res);
  } catch (error) {
    if (res.headersSent) res.destroy();
    else if (["ENOENT", "ENOTDIR"].includes(error.code))
      reply(404, "Not Found");
    else if (error.code === "EACCES") reply(403, "Forbidden");
    else {
      console.error(error);
      reply(500, "Internal Server Error");
    }
  }
});
server.on("error", (error) => {
  console.error(error.message);
  process.exitCode = 1;
});
server.listen(Number(portText), host, () => {
  const address = server.address();
  const displayHost = address.address.includes(":")
    ? `[${address.address}]`
    : address.address;
  console.log(`Pracownia Rzeczoznawcy: http://${displayHost}:${address.port}`);
});
for (const signal of ["SIGINT", "SIGTERM"])
  process.on(signal, () => server.close());
