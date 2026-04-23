# Node.js App Logic (inference.js)

The `inference.js` file contains your app's logic with setup, run, and Zod schemas.

## Structure

```javascript
import { z } from "zod";
import { File, textMeta } from "@inferencesh/app";

export const AppSetup = z.object({
  modelId: z.string().default("gpt2").describe("Model to load"),
});

export const RunInput = z.object({
  prompt: z.string().describe("What to generate"),
  style: z.string().default("modern").describe("Style"),
});

export const RunOutput = z.object({
  result: z.string().describe("Generated output"),
});

export class App {
  async setup(config) {
    // Runs once when worker starts or config changes
    this.model = await loadModel(config.modelId);
  }

  async run(inputData) {
    // Runs for each request — inputData is validated against RunInput
    return { result: "done" };
  }

  async unload() {
    // Cleanup on shutdown
  }
}
```

## Zod Field Types

| Type | Zod | Description |
|------|-----|-------------|
| String | `z.string()` | Text |
| Number | `z.number()` | Integer or float |
| Boolean | `z.boolean()` | True/false |
| Array | `z.array(z.string())` | List of items |
| Optional | `z.string().optional()` | Nullable field |
| Default | `z.string().default("hi")` | Has default value |
| Enum | `z.enum(["a", "b"])` | Restricted choices |
| Object | `z.object({...})` | Nested object |

## Setup Parameters

Use `AppSetup` to define parameters that trigger re-initialization when changed:

```javascript
export const AppSetup = z.object({
  modelId: z.string().default("gpt2").describe("Model to load"),
  precision: z.string().default("fp16").describe("Model precision"),
});

export class App {
  async setup(config) {
    // config is validated against AppSetup — defaults filled in
    this.model = await loadModel(config.modelId);
  }
}
```

## File Handling

Use `File` from `@inferencesh/app` for input and output files. The engine uploads local paths to CDN automatically.

```javascript
import { File } from "@inferencesh/app";
import { readFileSync, writeFileSync } from "node:fs";

async run(inputData) {
  // Input: download URL and get local path
  const input = await File.from(inputData.imageUrl);
  const data = readFileSync(input.path);

  // Output: write to temp path, wrap with File
  const outputPath = "/tmp/output.png";
  writeFileSync(outputPath, processedData);
  return { file: File.fromPath(outputPath) };
}
```

`File.fromPath()` is sync (no download) and serializes to `{ path, content_type, size, filename }` via `toJSON()`.

`File.from()` is async — downloads and caches URLs, or resolves local paths.

## Multi-Function Apps

Apps can expose multiple functions with different schemas. Export `{PascalName}Input` and `{PascalName}Output` for each method:

```javascript
import { z } from "zod";

export const RunInput = z.object({ name: z.string().default("World") });
export const RunOutput = z.object({ message: z.string() });

export const ReverseInput = z.object({ text: z.string() });
export const ReverseOutput = z.object({ reversedText: z.string() });

export class App {
  async run(inputData) {
    return { message: `Hello, ${inputData.name}!` };
  }

  async reverse(inputData) {
    return { reversedText: inputData.text.split("").reverse().join("") };
  }
}
```

Functions are auto-discovered if they:
- Are public (no `_` prefix)
- Have matching `{PascalName}Input` and `{PascalName}Output` Zod schema exports
- Are not lifecycle methods (`setup`, `unload`, `onCancel`, `constructor`)

Call via API with `"function": "reverse"` in the request body.

### Default Function

By default, `run` is called when no function is specified. To change this, set `default_function` in `inf.yml`:

```yaml
default_function: greet
```

## The onCancel Hook

For long-running tasks:

```javascript
async onCancel() {
  // Called when user cancels — must return quickly
  this.cancelFlag = true;
  return true;
}
```
