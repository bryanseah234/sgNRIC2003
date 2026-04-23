# Node.js: Debugging, Optimization & Cancellation

## Debugging Issues

### Import Errors — "ERR_MODULE_NOT_FOUND"

1. Ensure `"type": "module"` is in your `package.json`
2. Use file extensions in imports:
```javascript
import { helper } from "./helper.js"; // .js required for ESM
```
3. Check that dependencies are listed in `package.json`:
```json
{
  "dependencies": {
    "@inferencesh/app": "^0.1.2",
    "zod": "^3.23.0"
  }
}
```

### "Cannot use import statement outside a module"

Your `package.json` must have `"type": "module"`:
```json
{
  "type": "module"
}
```

### Heap Out of Memory

1. Increase RAM in `inf.yml`:
```yaml
resources:
  ram: 8
```
2. Stream large data instead of loading into memory
3. Clean up references and let GC collect

### Memory Leaks

Clean up after each request:

```javascript
async run(inputData) {
  const result = await this.process(inputData);
  // Clear any large temporary data
  return result;
}
```

### Temporary Files

Use `File.fromPath()` from `@inferencesh/app` for output files:

```javascript
import { File } from "@inferencesh/app";
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const outputPath = join(tmpdir(), "result.txt");
writeFileSync(outputPath, "output data");
return { file: File.fromPath(outputPath) };
```

### Path Resolution

Use `path.join` instead of string concatenation:

```javascript
import { join } from "node:path";
const configPath = join("models", "config", "settings.json");
```

### Version Conflicts

Pin compatible versions in `package.json`:
```json
{
  "dependencies": {
    "sharp": "0.33.2"
  }
}
```

### Native Modules

Some packages (e.g., `sharp`, `canvas`) need system libraries. Add them to `packages.txt`:
```
libvips-dev
```

### Debug Logging

```javascript
async setup(config) {
  console.log("Config:", JSON.stringify(config));
  console.log("Starting initialization...");
}

async run(inputData) {
  console.log("Input keys:", Object.keys(inputData));
  // stderr goes to kernel logs
  console.error("Debug:", inputData);
}
```

## Optimizing Performance

### Streaming Responses

Use async generators for long-running work — users see progress immediately:

```javascript
export class App {
  async *run(inputData) {
    for (const chunk of inputData.items) {
      const result = await this.processChunk(chunk);
      yield { partial: result, progress: chunk.index / inputData.items.length };
    }
  }
}
```

### Efficient File Processing

Stream large files instead of loading entirely into memory:

```javascript
import { File } from "@inferencesh/app";
import { createReadStream, createWriteStream } from "node:fs";
import { pipeline } from "node:stream/promises";

async run(inputData) {
  const input = createReadStream(inputData.file.path);
  const output = createWriteStream("/tmp/result.bin");
  await pipeline(input, transformStream, output);
  return { file: File.fromPath("/tmp/result.bin") };
}
```

### Memory Management

```javascript
async run(inputData) {
  const result = await this.process(inputData);

  // Clear large buffers when done
  this.tempBuffer = null;

  // Force GC if available (Node.js --expose-gc flag)
  if (global.gc) global.gc();

  return result;
}
```

### Error Handling

```javascript
async run(inputData) {
  try {
    const result = await this.process(inputData);
    return { result };
  } catch (e) {
    console.error(`Processing failed: ${e.message}`);
    throw new Error(`Failed to process: ${e.message}`);
  }
}
```

### Concurrency with Promise.all

Process independent items in parallel:

```javascript
async run(inputData) {
  const results = await Promise.all(
    inputData.items.map((item) => this.processItem(item))
  );
  return { results };
}
```

### Pre-deploy Checklist

- [ ] All imports resolve
- [ ] `setup()` initializes resources
- [ ] `run()` processes test input
- [ ] No hardcoded file paths
- [ ] Large data is streamed, not buffered

## Handling Cancellation

### The onCancel Hook

```javascript
export class App {
  constructor() {
    this.cancelFlag = false;
  }

  async onCancel() {
    console.log("Cancellation requested...");
    this.cancelFlag = true;
    return true;
  }

  async *run(inputData) {
    this.cancelFlag = false;

    for (let i = 0; i < 100; i++) {
      if (this.cancelFlag) {
        console.log("Stopping work...");
        break;
      }

      yield await this.heavyComputation(i);
    }
  }
}
```

You can also check `this.context.cancelRequested` which is set automatically by the kernel:

```javascript
async *run(inputData) {
  for (let i = 0; i < 100; i++) {
    if (this.context.cancelRequested) {
      yield { result: `Cancelled at step ${i}`, is_final: true };
      return;
    }
    yield await this.processStep(i);
  }
}
```

### Best Practices

1. **Check frequently**: In loops, check your cancellation flag at the start of every iteration.
2. **Clean up**: Close connections, delete temporary files, or free resources before exiting.
3. **Return quickly**: The `onCancel` handler should be fast — just set a flag or signal an event.
4. **Force kill**: If an app does not respond to `onCancel` within the timeout period (default 30s), it will be forcefully terminated.
