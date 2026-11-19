// Make.fun news-image entry (Node 22, standard library only).
// Emits the checked-in entry.png as /output/entry.png after checking it is a
// PNG within the gate's limits: at most 1 MiB and at most 1024 x 1024 pixels.
// The judge sees exactly the bytes copied, so the check fails loudly instead of
// emitting something the gate would refuse.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, openSync, readSync, closeSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outPath = join(outDir, 'entry.png');

const size = statSync(source).size;
if (size <= 0 || size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes; the limit is ${MAX_BYTES}`);
}

// The first 24 bytes hold the PNG signature and the IHDR width and height.
const head = Buffer.alloc(24);
const fd = openSync(source, 'r');
try {
  if (readSync(fd, head, 0, 24, 0) !== 24) throw new Error('entry.png is truncated');
} finally {
  closeSync(fd);
}

for (let i = 0; i < PNG_SIGNATURE.length; i++) {
  if (head[i] !== PNG_SIGNATURE[i]) throw new Error('entry.png is not a PNG');
}
if (head.toString('ascii', 12, 16) !== 'IHDR') throw new Error('entry.png has no IHDR chunk');

const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width < 1 || height < 1 || width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width} x ${height}; the limit is ${MAX_SIDE} per side`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, outPath);
console.log(`wrote ${outPath} (${size} bytes, ${width} x ${height})`);
