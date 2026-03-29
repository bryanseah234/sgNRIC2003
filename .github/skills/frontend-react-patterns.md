---
name: frontend-react-patterns
description: React patterns and best practices for Chrome extensions and web applications
technologies: [JavaScript, React, Vite, Chrome Extensions]
repositories: [dejavista, source-repo-code]
---

# React Patterns for Chrome Extensions

## When to Use

Use this skill when creating or modifying React components in Chrome extensions or web applications.

## Prerequisites

- JavaScript ES6+ fundamentals
- Basic React understanding
- Familiarity with Chrome extension architecture

## Step-by-Step Instructions

### 1. Chrome Extension Structure

```
src/
├── manifest.json           # Extension configuration
├── background/             # Service worker
│   └── index.js
├── content/                # Content scripts
│   ├── index.js
│   └── styles.css
├── sidepanel/              # React UI
│   ├── App.jsx
│   ├── main.jsx
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── ItemList.jsx
│   │   └── Recommendation.jsx
│   └── utils/
│       └── api.js
└── public/
    └── icons/
```

### 2. Manifest Configuration

```json
{
  "manifest_version": 3,
  "name": "DejaVista",
  "version": "1.0.0",
  "description": "AI Fashion Memory - Track and recommend outfits",
  "permissions": [
    "storage",
    "sidePanel",
    "tabs",
    "activeTab"
  ],
  "background": {
    "service_worker": "background/index.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content/index.js"],
      "css": ["content/styles.css"],
      "run_at": "document_idle"
    }
  ],
  "side_panel": {
    "default_path": "sidepanel/index.html"
  },
  "action": {
    "default_title": "Open DejaVista"
  }
}
```

### 3. React Component Pattern

```jsx
// sidepanel/components/ItemList.jsx
import { useState, useEffect } from 'react'
import { fetchTrackedItems } from '../utils/api'

function ItemList({ onSelectItem }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadItems()
  }, [])

  async function loadItems() {
    try {
      setLoading(true)
      const data = await fetchTrackedItems()
      setItems(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="item-list">
      {items.map(item => (
        <div 
          key={item.id} 
          className="item-card"
          onClick={() => onSelectItem(item)}
        >
          <img src={item.image} alt={item.name} />
          <div className="item-info">
            <h3>{item.name}</h3>
            <p className="price">${item.price}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ItemList
```

### 4. Custom Hook Pattern

```jsx
// sidepanel/hooks/useStorage.js
import { useState, useEffect } from 'react'

export function useStorage(key, defaultValue = null) {
  const [value, setValue] = useState(defaultValue)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load from Chrome storage
    chrome.storage.local.get([key], (result) => {
      setValue(result[key] || defaultValue)
      setLoading(false)
    })
  }, [key, defaultValue])

  const updateValue = async (newValue) => {
    await chrome.storage.local.set({ [key]: newValue })
    setValue(newValue)
  }

  return [value, updateValue, loading]
}

// Usage
function App() {
  const [trackedItems, setTrackedItems, loading] = useStorage('trackedItems', [])
  
  // Component logic
}
```

### 5. API Communication Pattern

```javascript
// sidepanel/utils/api.js
const API_BASE_URL = import.meta.env.VITE_VERCEL_API_URL

export async function fetchTrackedItems() {
  const response = await fetch(`${API_BASE_URL}/api/items`)
  if (!response.ok) throw new Error('Failed to fetch items')
  return response.json()
}

export async function getRecommendations(itemId) {
  const response = await fetch(`${API_BASE_URL}/api/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ itemId })
  })
  if (!response.ok) throw new Error('Failed to get recommendations')
  return response.json()
}

export async function trackItem(itemData) {
  const response = await fetch(`${API_BASE_URL}/api/track`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(itemData)
  })
  if (!response.ok) throw new Error('Failed to track item')
  return response.json()
}
```

### 6. Content Script Pattern

```javascript
// content/index.js
(function() {
  'use strict'

  // Track clothing items on page
  function trackClothingItems() {
    const clothingSelectors = [
      'img[src*="clothing"]',
      'img[alt*="shirt"]',
      'img[alt*="dress"]',
      // Add more selectors
    ]

    const items = document.querySelectorAll(clothingSelectors.join(','))
    
    items.forEach(img => {
      if (!img.dataset.tracked) {
        img.dataset.tracked = 'true'
        img.addEventListener('click', () => {
          chrome.runtime.sendMessage({
            type: 'TRACK_ITEM',
            item: {
              image: img.src,
              name: img.alt || 'Clothing Item',
              url: window.location.href
            }
          })
        })
      }
    })
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', trackClothingItems)
  } else {
    trackClothingItems()
  }

  // Re-scan when page changes (for SPAs)
  const observer = new MutationObserver(trackClothingItems)
  observer.observe(document.body, { childList: true, subtree: true })
})()
```

### 7. Background Service Worker

```javascript
// background/index.js
import { trackItem, getRecommendations } from './api.js'

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.type) {
    case 'TRACK_ITEM':
      handleTrackItem(message.item)
        .then(result => sendResponse(result))
        .catch(error => sendResponse({ error: error.message }))
      return true // Keep channel open for async response

    case 'GET_RECOMMENDATIONS':
      handleGetRecommendations(message.itemId)
        .then(result => sendResponse(result))
        .catch(error => sendResponse({ error: error.message }))
      return true

    default:
      console.warn('Unknown message type:', message.type)
  }
})

async function handleTrackItem(item) {
  try {
    const result = await trackItem(item)
    
    // Update badge
    chrome.action.setBadgeText({ text: '✓' })
    setTimeout(() => chrome.action.setBadgeText({ text: '' }), 2000)
    
    return { success: true, data: result }
  } catch (error) {
    return { success: false, error: error.message }
  }
}

async function handleGetRecommendations(itemId) {
  try {
    const recommendations = await getRecommendations(itemId)
    return { success: true, data: recommendations }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
```

## Common Pitfalls

1. **Not handling async properly** - Always use proper error handling with try/catch
2. **Forgetting to clean up** - Remove event listeners and observers when components unmount
3. **Blocking the main thread** - Use Web Workers for heavy computations
4. **Not testing in incognito** - Chrome extensions behave differently in incognito mode
5. **Hardcoding URLs** - Use environment variables for API endpoints

## References

- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
