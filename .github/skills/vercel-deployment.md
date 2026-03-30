---
name: vercel-deployment
description: Patterns and best practices for deploying applications to Vercel
---

# Vercel Deployment Patterns

## When to Use
Apply these patterns when configuring, optimizing, or troubleshooting deployments to the Vercel platform, particularly for Next.js, Vue/Nuxt, or static frontend applications.

## Core Principles
1. **Zero Configuration**: Rely on Vercel's default framework presets whenever possible.
2. **Environment Parity**: Ensure local development environments closely match Vercel's edge environment.
3. **Edge Optimization**: Utilize Edge Functions and Edge Caching for global performance.

## Step-by-Step

### 1. Basic Configuration (`vercel.json`)
While often unnecessary, a `vercel.json` file is useful for custom routing or headers:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://external-api.com/v1/$1"
    }
  ]
}
```

### 2. Environment Variables
- **Local**: Use `.env.local` for development (never commit this).
- **Vercel**: Configure variables in the Vercel Dashboard under Settings > Environment Variables.
- Ensure all required variables are present across Preview and Production environments.

### 3. Serverless vs. Edge Functions
- **Serverless (Node.js)**: Best for heavy computation or database connections that don't support Edge.
- **Edge**: Best for fast, globally distributed execution (e.g., middleware, simple API routes).

```javascript
// Next.js Edge API Route Example
export const config = {
  runtime: 'edge',
};

export default async function handler(req) {
  return new Response(JSON.stringify({ message: 'Hello from the Edge!' }), {
    status: 200,
    headers: {
      'content-type': 'application/json',
    },
  });
}
```

### 4. Caching Strategies
Utilize Vercel's Edge Network caching using standard Cache-Control headers:

```javascript
// Cache for 1 hour at the edge, allow stale while revalidating
res.setHeader(
  'Cache-Control',
  'public, s-maxage=3600, stale-while-revalidate=86400'
);
```

## References
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Edge Functions](https://vercel.com/docs/concepts/functions/edge-functions)
- [Vercel Project Configuration](https://vercel.com/docs/projects/project-configuration)