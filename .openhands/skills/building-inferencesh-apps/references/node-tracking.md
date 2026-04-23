# Node.js: Tracking Usage (Output Metadata)

Enable usage-based pricing by reporting what your app processes.

## Basic Structure

Use the factory functions from `@inferencesh/app` and return an `output_meta` field:

```javascript
import { textMeta } from "@inferencesh/app";

async run(inputData) {
  const result = await this.generate(inputData);

  return {
    result: result.text,
    output_meta: {
      inputs: [textMeta({ tokens: result.promptTokens })],
      outputs: [textMeta({ tokens: result.completionTokens })],
    },
  };
}
```

## MetaItem Types

| Factory | Fields |
|---------|--------|
| `textMeta` | `tokens` |
| `imageMeta` | `width`, `height`, `resolution_mp`, `steps`, `count` |
| `videoMeta` | `width`, `height`, `resolution`, `seconds` |
| `audioMeta` | `seconds` |
| `rawMeta` | `cost` (dollar cents) |

## Examples

### LLM/Text Generation

```javascript
import { textMeta } from "@inferencesh/app";

return {
  response: generatedText,
  output_meta: {
    inputs: [textMeta({ tokens: promptTokens })],
    outputs: [textMeta({ tokens: completionTokens })],
  },
};
```

### Image Generation

```javascript
import { File, imageMeta } from "@inferencesh/app";

return {
  image: File.fromPath(outputPath),
  output_meta: {
    outputs: [imageMeta({
      width: 1024,
      height: 1024,
      resolution_mp: 1.05,
      steps: 20,
      count: 1,
    })],
  },
};
```

### Video Generation

```javascript
import { File, videoMeta } from "@inferencesh/app";

return {
  video: File.fromPath(outputPath),
  output_meta: {
    outputs: [videoMeta({
      width: 1280,
      height: 720,
      resolution: "720p",
      seconds: 5.0,
    })],
  },
};
```

### Audio Generation

```javascript
import { File, audioMeta } from "@inferencesh/app";

return {
  audio: File.fromPath(outputPath),
  output_meta: {
    outputs: [audioMeta({ seconds: 30.0 })],
  },
};
```

## Custom Data

Use `extra` for app-specific pricing factors:

```javascript
output_meta: {
  outputs: [imageMeta({
    width: 1024,
    height: 1024,
    extra: {
      model: "sdxl-turbo",
      lora_count: 2,
    },
  })],
}
```

## Best Practices

1. **Always populate `output_meta`** if usage varies per request
2. **Use accurate token counts** from the actual tokenizer
3. **Report actual dimensions** — don't hardcode
4. **Include relevant `extra` data** for pricing flexibility
