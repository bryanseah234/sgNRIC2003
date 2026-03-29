---
name: javascript-vue3-composition
description: Vue 3 Composition API patterns and best practices for frontend development
technologies: [JavaScript, Vue 3, Composition API]
repositories: [ticketremaster-f, source-repo-code]
---

# Vue 3 Composition API Development

## When to Use

Use this skill when creating or modifying Vue 3 components using the Composition API.

## Prerequisites

- JavaScript ES6+ fundamentals
- Basic Vue.js understanding
- Familiarity with reactive programming concepts

## Step-by-Step Instructions

### 1. Component Structure

Always use `<script setup>` syntax for cleaner code:

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from '@/stores/main'

// Props
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['update', 'delete'])

// Reactive state
const loading = ref(false)
const error = ref(null)

// Computed
const filteredItems = computed(() => {
  return props.items.filter(item => item.active)
})

// Methods
const handleUpdate = async (id) => {
  loading.value = true
  try {
    const response = await fetch(`/api/items/${id}`)
    const data = await response.json()
    emit('update', data)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div class="component">
    <h2>{{ props.title }}</h2>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <ul v-else>
      <li v-for="item in filteredItems" :key="item.id">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.component {
  padding: 1rem;
}
</style>
```

### 2. Composable Functions

Create reusable logic with composables:

```javascript
// composables/useFetch.js
import { ref } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchData = async () => {
    loading.value = true
    try {
      const response = await fetch(url)
      if (!response.ok) throw new Error('Network response was not ok')
      data.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
}

// Usage in component
<script setup>
import { useFetch } from '@/composables/useFetch'

const { data: users, loading, error, fetchData } = useFetch('/api/users')

onMounted(() => {
  fetchData()
})
</script>
```

### 3. State Management with Pinia

```javascript
// stores/counter.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0)
  const name = ref('counter')

  // Getters
  const doubleCount = computed(() => count.value * 2)

  // Actions
  function increment() {
    count.value++
  }

  function incrementBy(amount) {
    count.value += amount
  }

  return { count, doubleCount, name, increment, incrementBy }
})

// Usage in component
<script setup>
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const { count, doubleCount } = storeToRefs(store)
const { increment, incrementBy } = store

// Use directly
increment()
incrementBy(5)
</script>
```

### 4. Event Handling

```vue
<script setup>
const handleSubmit = (event) => {
  event.preventDefault()
  // Handle form submission
}

const handleKeydown = (event) => {
  if (event.key === 'Enter') {
    // Handle enter key
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <input @keydown="handleKeydown" />
    <button type="submit">Submit</button>
  </form>
</template>
```

### 5. Watchers

```vue
<script setup>
import { ref, watch, watchEffect } from 'vue'

const searchTerm = ref('')
const results = ref([])

// Watch specific source
watch(searchTerm, async (newVal, oldVal) => {
  if (newVal.length > 2) {
    results.value = await searchApi(newVal)
  }
})

// Watch multiple sources
watch([searchTerm, filters], ([newSearch, newFilters]) => {
  // React to changes in both
})

// WatchEffect - automatically track dependencies
watchEffect(async () => {
  if (searchTerm.value.length > 2) {
    results.value = await searchApi(searchTerm.value)
  }
})
</script>
```

## Common Pitfalls

1. **Not using `ref()` for primitive values** - Always wrap primitives in `ref()`
2. **Forgetting `.value`** - Access ref values with `.value` in script, auto-unwrapped in template
3. **Mutating props directly** - Always emit events to change props
4. **Not cleaning up watchers** - Use `onUnmounted` to clean up side effects
5. **Overusing `watchEffect`** - Prefer explicit `watch` for better control

## References

- [Vue 3 Composition API Documentation](https://vuejs.org/guide/reusability/composables.html)
- [Vue 3 Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [Pinia State Management](https://pinia.vuejs.org/)
