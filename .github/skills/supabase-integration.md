---
name: supabase-integration
description: Supabase integration patterns for authentication, database, and storage
technologies: [JavaScript, Supabase, PostgreSQL]
repositories: [dejavista, source-repo-code]
---

# Supabase Integration Patterns

## When to Use

Use this skill when integrating Supabase for authentication, database operations, or file storage in JavaScript/TypeScript applications.

## Prerequisites

- Basic understanding of PostgreSQL
- Familiarity with JavaScript async/await
- Understanding of authentication concepts

## Step-by-Step Instructions

### 1. Supabase Client Setup

```javascript
// src/lib/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Service role client for server-side operations (Vercel functions)
export const supabaseAdmin = createClient(
  supabaseUrl,
  import.meta.env.VITE_SUPABASE_SERVICE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
)
```

### 2. Authentication Patterns

```javascript
// src/lib/auth.js
import { supabase } from './supabase'

// Sign up with email/password
export async function signUp(email, password) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: 'User Name'
      }
    }
  })
  
  if (error) throw error
  return data
}

// Sign in
export async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })
  
  if (error) throw error
  return data
}

// Sign in with Google OAuth
export async function signInWithGoogle() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`
    }
  })
  
  if (error) throw error
  return data
}

// Get current user
export async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser()
  if (error) throw error
  return user
}

// Sign out
export async function signOut() {
  const { error } = await supabase.auth.signOut()
  if (error) throw error
}

// Auth state listener
export function onAuthStateChange(callback) {
  return supabase.auth.onAuthStateChange(callback)
}
```

### 3. Database Query Patterns

```javascript
// src/lib/database.js
import { supabase } from './supabase'

// Fetch items with filters
export async function fetchTrackedItems(userId, options = {}) {
  let query = supabase
    .from('tracked_items')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
  
  // Apply optional filters
  if (options.category) {
    query = query.eq('category', options.category)
  }
  
  if (options.limit) {
    query = query.limit(options.limit)
  }
  
  const { data, error } = await query
  
  if (error) throw error
  return data
}

// Create new item
export async function createTrackedItem(itemData) {
  const { data, error } = await supabase
    .from('tracked_items')
    .insert([itemData])
    .select()
    .single()
  
  if (error) throw error
  return data
}

// Update item
export async function updateTrackedItem(itemId, updates) {
  const { data, error } = await supabase
    .from('tracked_items')
    .update(updates)
    .eq('id', itemId)
    .select()
    .single()
  
  if (error) throw error
  return data
}

// Delete item
export async function deleteTrackedItem(itemId) {
  const { error } = await supabase
    .from('tracked_items')
    .delete()
    .eq('id', itemId)
  
  if (error) throw error
}

// Complex query with joins
export async function fetchUserWithRecommendations(userId) {
  const { data, error } = await supabase
    .from('users')
    .select(`
      *,
      tracked_items (
        *,
        recommendations (
          *
        )
      )
    `)
    .eq('id', userId)
    .single()
  
  if (error) throw error
  return data
}
```

### 4. Real-time Subscriptions

```javascript
// src/lib/realtime.js
import { supabase } from './supabase'

// Subscribe to table changes
export function subscribeToItems(userId, callback) {
  const channel = supabase
    .channel('items_changes')
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'tracked_items',
        filter: `user_id=eq.${userId}`
      },
      callback
    )
    .subscribe()
  
  return () => {
    supabase.removeChannel(channel)
  }
}

// Subscribe to specific events
export function subscribeToInserts(callback) {
  const channel = supabase
    .channel('items_inserts')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'tracked_items'
      },
      callback
    )
    .subscribe()
  
  return () => {
    supabase.removeChannel(channel)
  }
}
```

### 5. Storage Operations

```javascript
// src/lib/storage.js
import { supabase } from './supabase'

// Upload file
export async function uploadItemImage(file, itemId) {
  const fileExt = file.name.split('.').pop()
  const fileName = `${itemId}_${Date.now()}.${fileExt}`
  const filePath = `${fileName}`
  
  const { data, error } = await supabase.storage
    .from('item-images')
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false
    })
  
  if (error) throw error
  
  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from('item-images')
    .getPublicUrl(filePath)
  
  return publicUrl
}

// Download file
export async function downloadItemImage(filePath) {
  const { data, error } = await supabase.storage
    .from('item-images')
    .download(filePath)
  
  if (error) throw error
  
  return URL.createObjectURL(data)
}

// Delete file
export async function deleteItemImage(filePath) {
  const { error } = await supabase.storage
    .from('item-images')
    .remove([filePath])
  
  if (error) throw error
}
```

### 6. Row Level Security (RLS) Policies

```sql
-- Enable RLS on tracked_items table
ALTER TABLE tracked_items ENABLE ROW LEVEL SECURITY;

-- Users can view their own items
CREATE POLICY "Users can view own items" ON tracked_items
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own items
CREATE POLICY "Users can insert own items" ON tracked_items
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own items
CREATE POLICY "Users can update own items" ON tracked_items
  FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can delete their own items
CREATE POLICY "Users can delete own items" ON tracked_items
  FOR DELETE
  USING (auth.uid() = user_id);
```

### 7. Database Schema

```sql
-- tracked_items table
CREATE TABLE tracked_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  category TEXT,
  price DECIMAL(10,2),
  source_url TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- recommendations table
CREATE TABLE recommendations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  item_id UUID REFERENCES tracked_items(id) ON DELETE CASCADE,
  recommended_item JSONB NOT NULL,
  confidence_score FLOAT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_tracked_items_user_id ON tracked_items(user_id);
CREATE INDEX idx_tracked_items_category ON tracked_items(category);
CREATE INDEX idx_recommendations_item_id ON recommendations(item_id);
```

## Common Pitfalls

1. **Not handling auth state changes** - Always listen for auth state changes
2. **Forgetting RLS policies** - Always enable RLS and define proper policies
3. **Not cleaning up subscriptions** - Always unsubscribe when components unmount
4. **Exposing service key** - Never expose service key in client-side code
5. **Not handling errors** - Always handle Supabase errors properly

## References

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase JS Client](https://supabase.com/docs/reference/javascript/introduction)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
