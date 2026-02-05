---
name: mapbox-search-integration
description: Complete workflow for implementing Mapbox search in applications - from discovery questions to production-ready integration with best practices
---

# Mapbox Search Integration Skill

Expert guidance for implementing Mapbox search functionality in applications. Covers the complete workflow from asking the right discovery questions, selecting the appropriate search product, to implementing production-ready integrations following best practices from the Mapbox search team.

## Use This Skill When

User says things like:
- "I need to add search to my map"
- "I need a search bar for my mapping app"
- "How do I implement location search?"
- "I want users to search for places/addresses"
- "I need geocoding in my application"

**This skill complements `mapbox-search-patterns`:**
- `mapbox-search-patterns` = Tool and parameter selection
- `mapbox-search-integration` = Complete implementation workflow

## Discovery Phase: Ask the Right Questions

Before jumping into code, ask these questions to understand requirements:

### Question 1: What are users searching for?

**Ask:** "What do you want users to search for?"

**Common answers and implications:**
- **"Addresses"** → Focus on address geocoding, consider Search Box API or Geocoding API
- **"Points of interest / businesses"** → POI search, use Search Box API with category search
- **"Both addresses and POIs"** → Search Box API (unified search)
- **"Specific types of places"** (restaurants, hotels, etc.) → Category search or filtered POI search
- **"Custom locations"** (user-created places) → May need custom data + search integration

### Question 2: What's the geographic scope?

**Ask:** "Where will users be searching?"

**Common answers and implications:**
- **"Single country"** (e.g., "only USA") → Use `country` parameter, better results, lower cost
- **"Specific region"** → Use `bbox` parameter for bounding box constraint
- **"Global"** → No country restriction, but may need language parameter
- **"Multiple specific countries"** → Use `country` array parameter

**Follow-up:** "Do you need to limit results to a specific area?" (delivery zone, service area, etc.)

### Question 3: What's the search interaction pattern?

**Ask:** "How will users interact with search?"

**Common answers and implications:**
- **"Search-as-you-type / autocomplete"** → Use Search Box API with `autocomplete: true`, implement debouncing
- **"Search button / final query"** → Can use either API, no autocomplete needed
- **"Both"** (autocomplete + refine) → Two-stage search, autocomplete then detailed results
- **"Voice input"** → Consider speech-to-text integration, handle longer queries

### Question 4: What platform?

**Ask:** "What platform is this for?"

**Common answers and implications:**
- **"Web application"** → Mapbox Search JS (easiest), or direct API calls for advanced cases
- **"iOS app"** → Search SDK for iOS (recommended), or direct API integration for advanced cases
- **"Android app"** → Search SDK for Android (recommended), or direct API integration for advanced cases
- **"Multiple platforms"** → Platform-specific SDKs (recommended), or direct API approach for consistency
- **"React app"** → Mapbox Search JS React (easiest with UI), or Search JS Core for custom UI
- **"Vue / Angular / Other framework"** → Mapbox Search JS Core or Web, or direct API calls

### Question 5: How will results be used?

**Ask:** "What happens when a user selects a result?"

**Common answers and implications:**
- **"Fly to location on map"** → Need coordinates, map integration
- **"Show details / info"** → Need to retrieve and display result properties
- **"Fill form fields"** → Need to parse address components
- **"Start navigation"** → Need coordinates, integrate with directions
- **"Multiple selection"** → Need to handle selection state, possibly show markers

### Question 6: Expected usage volume?

**Ask:** "How many searches do you expect per month?"

**Implications:**
- **Low volume** (< 10k) → Free tier sufficient, simple implementation
- **Medium volume** (10k-100k) → Consider caching, optimize API calls
- **High volume** (> 100k) → Implement debouncing, caching, batch operations, monitor costs

## Product Selection Decision Tree

Based on discovery answers, recommend the right product:

### Recommended: Search Box API (Modern, Unified)

**Use when:**
- User needs both addresses AND POIs
- Building a modern web/mobile app
- Want autocomplete functionality
- Need session-based pricing
- Want the simplest integration

**Advantages:**
- ✅ Unified search (addresses + POIs)
- ✅ Session-based pricing (cheaper for autocomplete)
- ✅ Modern API design
- ✅ Built-in autocomplete support
- ✅ Better POI coverage

**Products:**
- **Search Box API** (REST) - Direct API integration
- **Mapbox Search JS** (SDK) - Web integration with three components:
  - **Search JS React** - Easy search integration via React library with UI
  - **Search JS Web** - Easy search integration via Web Components with UI
  - **Search JS Core** - JavaScript (node or web) wrapper for API, build your own UI
- **Search SDK for iOS** - Native iOS integration
- **Search SDK for Android** - Native Android integration

### Geocoding API

**Use when:**
- Only need address geocoding (no POIs)
- Existing integration to maintain
- Need permanent geocoding (not search)
- Batch geocoding jobs

**Note:** Prefer Search Box API unless the user specifically says they only want address geocoding.

## Integration Patterns by Platform

**Important:** Always prefer using SDKs (Mapbox Search JS, Search SDK for iOS/Android) over calling APIs directly. SDKs handle debouncing, session tokens, error handling, and provide UI components. Only use direct API calls for advanced use cases.

### Web: Mapbox Search JS (Recommended)

#### Option 1: Search JS React (Easiest - React apps with UI)

**When to use:** React application, want autocomplete UI component, fastest implementation

**Installation:**
```bash
npm install @mapbox/search-js-react
```

**Complete implementation:**
```jsx
import { SearchBox } from '@mapbox/search-js-react';
import mapboxgl from 'mapbox-gl';

function App() {
  const [map, setMap] = React.useState(null);

  React.useEffect(() => {
    mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
    const mapInstance = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-122.4194, 37.7749],
      zoom: 12
    });
    setMap(mapInstance);
  }, []);

  const handleRetrieve = (result) => {
    const [lng, lat] = result.features[0].geometry.coordinates;
    map.flyTo({ center: [lng, lat], zoom: 14 });

    new mapboxgl.Marker()
      .setLngLat([lng, lat])
      .addTo(map);
  };

  return (
    <div>
      <SearchBox
        accessToken="YOUR_MAPBOX_TOKEN"
        onRetrieve={handleRetrieve}
        placeholder="Search for places"
      />
      <div id="map" style={{ height: '600px' }} />
    </div>
  );
}
```

#### Option 2: Search JS Web (Web Components with UI)

**When to use:** Vanilla JavaScript, Web Components, or any framework, want autocomplete UI

**Complete implementation:**

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://api.mapbox.com/search-js/v1.0.0-beta.18/web.js"></script>
  <link href="https://api.mapbox.com/search-js/v1.0.0-beta.18/web.css" rel="stylesheet">
  <script src='https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.js'></script>
  <link href='https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.css' rel='stylesheet' />
</head>
<body>
  <div id="search"></div>
  <div id="map" style="height: 600px;"></div>

  <script>
    // Initialize map
    mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-122.4194, 37.7749],
      zoom: 12
    });

    // Initialize Search Box
    const search = new MapboxSearchBox();
    search.accessToken = 'YOUR_MAPBOX_TOKEN';

    // CRITICAL: Set options based on discovery
    search.options = {
      language: 'en',
      country: 'US', // If single-country (from Question 2)
      proximity: 'ip', // Or specific coordinates
      types: 'address,poi', // Based on Question 1
    };

    search.mapboxgl = mapboxgl;
    search.marker = true; // Auto-add marker on result selection

    // Handle result selection
    search.addEventListener('retrieve', (event) => {
      const result = event.detail;

      // Fly to result
      map.flyTo({
        center: result.geometry.coordinates,
        zoom: 15,
        essential: true
      });

      // Optional: Show popup with details
      new mapboxgl.Popup()
        .setLngLat(result.geometry.coordinates)
        .setHTML(`<h3>${result.properties.name}</h3>
                  <p>${result.properties.full_address || ''}</p>`)
        .addTo(map);
    });

    // Attach to DOM
    document.getElementById('search').appendChild(search);
  </script>
</body>
</html>
```

**Key implementation notes:**
- ✅ Set `country` if single-country search (better results, lower cost)
- ✅ Set `types` based on what users search for
- ✅ Use `proximity` to bias results to user location
- ✅ Handle `retrieve` event for result selection
- ✅ Integrate with map (flyTo, markers, popups)

#### Option 3: Search JS Core (Custom UI)

**When to use:** Need custom UI design, full control over UX, works in any framework or Node.js

**Installation:**
```bash
npm install @mapbox/search-js-core
```

**Complete implementation:**
```javascript
import { SearchSession } from '@mapbox/search-js-core';
import mapboxgl from 'mapbox-gl';

// Initialize search session
const search = new SearchSession({
  accessToken: 'YOUR_MAPBOX_TOKEN'
});

// Initialize map
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-122.4194, 37.7749],
  zoom: 12
});

// Your custom search input
const searchInput = document.getElementById('search-input');
const resultsContainer = document.getElementById('results');

// Handle user input
searchInput.addEventListener('input', async (e) => {
  const query = e.target.value;

  if (query.length < 2) {
    resultsContainer.innerHTML = '';
    return;
  }

  // Get suggestions (Search JS Core handles debouncing and session tokens)
  const response = await search.suggest(query, {
    proximity: map.getCenter().toArray(),
    country: 'US', // Optional
    types: ['address', 'poi']
  });

  // Render custom results UI
  resultsContainer.innerHTML = response.suggestions.map(suggestion => `
    <div class="result-item" data-id="${suggestion.mapbox_id}">
      <strong>${suggestion.name}</strong>
      <div>${suggestion.place_formatted}</div>
    </div>
  `).join('');
});

// Handle result selection
resultsContainer.addEventListener('click', async (e) => {
  const resultItem = e.target.closest('.result-item');
  if (!resultItem) return;

  const mapboxId = resultItem.dataset.id;

  // Retrieve full details
  const result = await search.retrieve(mapboxId);
  const feature = result.features[0];
  const [lng, lat] = feature.geometry.coordinates;

  // Update map
  map.flyTo({ center: [lng, lat], zoom: 15 });
  new mapboxgl.Marker().setLngLat([lng, lat]).addTo(map);

  // Clear search
  searchInput.value = feature.properties.name;
  resultsContainer.innerHTML = '';
});
```

**Key benefits:**
- ✅ Full control over UI/UX
- ✅ Search JS Core handles session tokens automatically
- ✅ Works in any framework (React, Vue, Angular, etc.)
- ✅ Can use in Node.js for server-side search

#### Option 4: Direct API Integration (Advanced - Last Resort)

**When to use:** Very specific requirements that SDKs don't support, or server-side integration where Search JS Core doesn't fit

**Important:** Only use direct API calls when SDKs don't meet your needs. You'll need to handle debouncing and session tokens manually.

**When to use:** Custom UI, framework integration, need full control

**Complete implementation with debouncing:**

```javascript
import mapboxgl from 'mapbox-gl';

class MapboxSearch {
  constructor(accessToken, options = {}) {
    this.accessToken = accessToken;
    this.options = {
      country: options.country || null, // e.g., 'US'
      language: options.language || 'en',
      proximity: options.proximity || 'ip',
      types: options.types || 'address,poi',
      limit: options.limit || 5,
      ...options
    };

    this.debounceTimeout = null;
    this.sessionToken = this.generateSessionToken();
  }

  generateSessionToken() {
    return `${Date.now()}-${Math.random().toString(36).substring(7)}`;
  }

  // CRITICAL: Debounce to avoid API spam
  async search(query, callback, debounceMs = 300) {
    clearTimeout(this.debounceTimeout);

    this.debounceTimeout = setTimeout(async () => {
      const results = await this.performSearch(query);
      callback(results);
    }, debounceMs);
  }

  async performSearch(query) {
    if (!query || query.length < 2) return [];

    const params = new URLSearchParams({
      q: query,
      access_token: this.accessToken,
      session_token: this.sessionToken,
      language: this.options.language,
      limit: this.options.limit,
    });

    // Add optional parameters
    if (this.options.country) {
      params.append('country', this.options.country);
    }

    if (this.options.types) {
      params.append('types', this.options.types);
    }

    if (this.options.proximity && this.options.proximity !== 'ip') {
      params.append('proximity', this.options.proximity);
    }

    try {
      const response = await fetch(
        `https://api.mapbox.com/search/searchbox/v1/suggest?${params}`
      );

      if (!response.ok) {
        throw new Error(`Search API error: ${response.status}`);
      }

      const data = await response.json();
      return data.suggestions || [];
    } catch (error) {
      console.error('Search error:', error);
      return [];
    }
  }

  async retrieve(suggestionId) {
    const params = new URLSearchParams({
      access_token: this.accessToken,
      session_token: this.sessionToken,
    });

    try {
      const response = await fetch(
        `https://api.mapbox.com/search/searchbox/v1/retrieve/${suggestionId}?${params}`
      );

      if (!response.ok) {
        throw new Error(`Retrieve API error: ${response.status}`);
      }

      const data = await response.json();

      // Session ends on retrieve - generate new token for next search
      this.sessionToken = this.generateSessionToken();

      return data.features[0];
    } catch (error) {
      console.error('Retrieve error:', error);
      return null;
    }
  }
}

// Usage example
const search = new MapboxSearch('YOUR_MAPBOX_TOKEN', {
  country: 'US', // Based on discovery Question 2
  types: 'poi', // Based on discovery Question 1
  proximity: [-122.4194, 37.7749] // Or 'ip' for user location
});

// Attach to input field
const input = document.getElementById('search-input');
const resultsContainer = document.getElementById('search-results');

input.addEventListener('input', (e) => {
  const query = e.target.value;

  search.search(query, (results) => {
    displayResults(results);
  });
});

function displayResults(results) {
  resultsContainer.innerHTML = results.map(result => `
    <div class="result" data-id="${result.mapbox_id}">
      <strong>${result.name}</strong>
      <p>${result.place_formatted || ''}</p>
    </div>
  `).join('');

  // Handle result selection
  resultsContainer.querySelectorAll('.result').forEach(el => {
    el.addEventListener('click', async () => {
      const feature = await search.retrieve(el.dataset.id);
      handleResultSelection(feature);
    });
  });
}

function handleResultSelection(feature) {
  const [lng, lat] = feature.geometry.coordinates;

  // Fly map to result
  map.flyTo({
    center: [lng, lat],
    zoom: 15
  });

  // Add marker
  new mapboxgl.Marker()
    .setLngLat([lng, lat])
    .addTo(map);

  // Close results
  resultsContainer.innerHTML = '';
  input.value = feature.properties.name;
}
```

**Critical implementation details:**
1. ✅ **Debouncing**: Wait 300ms after user stops typing before API call
2. ✅ **Session tokens**: Use same token for suggest + retrieve, generate new after
3. ✅ **Error handling**: Handle API errors gracefully
4. ✅ **Parameter optimization**: Only send parameters you need
5. ✅ **Result display**: Show name + formatted address
6. ✅ **Selection handling**: Retrieve full feature on selection

### React Integration Pattern

**Best Practice:** Use Search JS React for easiest implementation, or Search JS Core for custom UI.

#### Option 1: Search JS React (Recommended - Easiest)

```javascript
import { SearchBox } from '@mapbox/search-js-react';
import mapboxgl from 'mapbox-gl';
import { useState } from 'react';

function MapboxSearchComponent() {
  const [map, setMap] = useState(null);

  useEffect(() => {
    const mapInstance = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-122.4194, 37.7749],
      zoom: 12
    });
    setMap(mapInstance);
  }, []);

  const handleRetrieve = (result) => {
    const [lng, lat] = result.features[0].geometry.coordinates;
    map.flyTo({ center: [lng, lat], zoom: 14 });

    new mapboxgl.Marker()
      .setLngLat([lng, lat])
      .addTo(map);
  };

  return (
    <div>
      <SearchBox
        accessToken="YOUR_MAPBOX_TOKEN"
        onRetrieve={handleRetrieve}
        placeholder="Search for places"
        options={{
          country: 'US', // Optional
          types: 'address,poi'
        }}
      />
      <div id="map" style={{ height: '600px' }} />
    </div>
  );
}
```

**Benefits:**
- ✅ Complete UI component provided
- ✅ No manual debouncing needed
- ✅ No manual session token management
- ✅ Production-ready out of the box

#### Option 2: Search JS Core (Custom UI)

```javascript
import { useState, useEffect } from 'react';
import { SearchSession } from '@mapbox/search-js-core';
import mapboxgl from 'mapbox-gl';

function MapboxSearchComponent({ country, types = 'address,poi' }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Search JS Core handles debouncing and session tokens automatically
  const searchSession = new SearchSession({
    accessToken: 'YOUR_MAPBOX_TOKEN'
  });

  useEffect(() => {
    const performSearch = async () => {
      if (!query || query.length < 2) {
        setResults([]);
        return;
      }

      setIsLoading(true);
      try {
        const response = await searchSession.suggest(query, {
          country,
          types,
          limit: 5
        });
        setResults(response.suggestions || []);
      } catch (error) {
        console.error('Search error:', error);
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    };

    performSearch();
  }, [query]);

  const handleResultClick = async (suggestion) => {
    try {
      const result = await searchSession.retrieve(suggestion);
      const feature = result.features[0];

      // Handle result (fly to location, add marker, etc.)
      onResultSelect(feature);

      setQuery(feature.properties.name);
      setResults([]);
    } catch (error) {
      console.error('Retrieve error:', error);
    }
  };

  return (
    <div className="search-container">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for a place..."
        className="search-input"
      />

      {isLoading && <div className="loading">Searching...</div>}

      {results.length > 0 && (
        <div className="search-results">
          {results.map((result) => (
            <div
              key={result.mapbox_id}
              className="search-result"
              onClick={() => handleResultClick(result)}
            >
              <strong>{result.name}</strong>
              {result.place_formatted && <p>{result.place_formatted}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

**Benefits:**
- ✅ Full control over UI design
- ✅ Search JS Core handles debouncing automatically
- ✅ Search JS Core handles session tokens automatically
- ✅ Cleaner code than direct API calls

**Note:** For React apps, prefer Search JS React (Option 1) unless you need a completely custom UI design.

### iOS: Search SDK for iOS (Recommended)

#### Option 1: Search SDK with UI (Easiest)

**When to use:** iOS app, want pre-built search UI, fastest implementation

**Installation:**
```swift
// Add to Package.swift or SPM
dependencies: [
    .package(url: "https://github.com/mapbox/mapbox-search-ios.git", from: "2.0.0")
]
```

**Complete implementation with built-in UI:**
```swift
import MapboxSearch
import MapboxMaps

class SearchViewController: UIViewController {
    private var searchController: MapboxSearchController!
    private var mapView: MapView!

    override func viewDidLoad() {
        super.viewDidLoad()

        setupMap()
        setupSearchWithUI()
    }

    func setupMap() {
        mapView = MapView(frame: view.bounds)
        view.addSubview(mapView)
    }

    func setupSearchWithUI() {
        // MapboxSearchController provides complete UI automatically
        searchController = MapboxSearchController()
        searchController.delegate = self

        // Present the search UI
        present(searchController, animated: true)
    }
}

extension SearchViewController: SearchControllerDelegate {
    func searchResultSelected(_ searchResult: SearchResult) {
        // SDK handled all the search interaction
        // Just respond to selection

        mapView.camera.fly(to: CameraOptions(
            center: searchResult.coordinate,
            zoom: 15
        ))

        let annotation = PointAnnotation(coordinate: searchResult.coordinate)
        mapView.annotations.pointAnnotations = [annotation]

        dismiss(animated: true)
    }
}
```

#### Option 2: Search SDK Core (Custom UI)

**When to use:** Need custom UI, integrate with UISearchController, full control over UX

**Complete implementation:**
```swift
import MapboxSearch
import MapboxMaps

class SearchViewController: UIViewController {
    private var searchEngine: SearchEngine!
    private var mapView: MapView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Initialize Search Engine (SDK handles debouncing and session tokens)
        searchEngine = SearchEngine(accessToken: "YOUR_MAPBOX_TOKEN")

        setupSearchBar()
        setupMap()
    }

    func setupSearchBar() {
        let searchController = UISearchController(searchResultsController: nil)
        searchController.searchResultsUpdater = self
        searchController.obscuresBackgroundDuringPresentation = false
        navigationItem.searchController = searchController
    }

    func setupMap() {
        mapView = MapView(frame: view.bounds)
        view.addSubview(mapView)
    }
}

extension SearchViewController: UISearchResultsUpdating {
    func updateSearchResults(for searchController: UISearchController) {
        guard let query = searchController.searchBar.text, !query.isEmpty else {
            return
        }

        // Search SDK handles debouncing automatically
        searchEngine.search(query: query) { [weak self] result in
            switch result {
            case .success(let results):
                self?.displayResults(results)
            case .failure(let error):
                print("Search error: \(error)")
            }
        }
    }

    func displayResults(_ results: [SearchResult]) {
        // Display results in custom table view
        // When user selects a result:
        handleResultSelection(results[0])
    }

    func handleResultSelection(_ result: SearchResult) {
        mapView.camera.fly(to: CameraOptions(
            center: result.coordinate,
            zoom: 15
        ))

        let annotation = PointAnnotation(coordinate: result.coordinate)
        mapView.annotations.pointAnnotations = [annotation]
    }
}
```

#### Option 3: Direct API Integration (Advanced)

**When to use:** Very specific requirements, server-side iOS backend

**Important:** Only use if SDK doesn't meet your needs. You must handle debouncing and session tokens manually.

```swift
// Direct API calls - see Web direct API example
// Not recommended for iOS - use Search SDK instead
```

### Android: Search SDK for Android (Recommended)

#### Option 1: Search SDK with UI (Easiest)

**When to use:** Android app, want pre-built search UI, fastest implementation

**Installation:**
```gradle
// Add to build.gradle
dependencies {
    implementation 'com.mapbox.search:mapbox-search-android-ui:2.0.0'
    implementation 'com.mapbox.maps:android:11.0.0'
}
```

**Complete implementation with built-in UI:**
```kotlin
import com.mapbox.search.ui.view.SearchBottomSheetView
import com.mapbox.maps.MapView

class SearchActivity : AppCompatActivity() {
    private lateinit var searchView: SearchBottomSheetView
    private lateinit var mapView: MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search)

        mapView = findViewById(R.id.map_view)

        // SearchBottomSheetView provides complete UI automatically
        searchView = findViewById(R.id.search_view)
        searchView.initializeSearch(
            savedInstanceState,
            SearchBottomSheetView.Configuration()
        )

        // Handle result selection
        searchView.addOnSearchResultClickListener { searchResult ->
            // SDK handled all the search interaction
            val coordinate = searchResult.coordinate

            mapView.getMapboxMap().flyTo(
                CameraOptions.Builder()
                    .center(Point.fromLngLat(coordinate.longitude, coordinate.latitude))
                    .zoom(15.0)
                    .build()
            )

            searchView.hide()
        }
    }
}
```

#### Option 2: Search SDK Core (Custom UI)

**When to use:** Need custom UI, integrate with SearchView, full control over UX

**Complete implementation:**
```kotlin
import com.mapbox.search.SearchEngine
import com.mapbox.search.SearchEngineSettings
import com.mapbox.search.SearchOptions
import com.mapbox.maps.MapView

class SearchActivity : AppCompatActivity() {
    private lateinit var searchEngine: SearchEngine
    private lateinit var mapView: MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Initialize Search Engine (SDK handles debouncing and session tokens)
        searchEngine = SearchEngine.createSearchEngine(
            SearchEngineSettings("YOUR_MAPBOX_TOKEN")
        )

        setupSearchView()
        setupMap()
    }

    private fun setupSearchView() {
        val searchView = findViewById<SearchView>(R.id.search_view)

        searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String): Boolean {
                performSearch(query)
                return true
            }

            override fun onQueryTextChange(newText: String): Boolean {
                if (newText.length >= 2) {
                    // Search SDK handles debouncing automatically
                    performSearch(newText)
                }
                return true
            }
        })
    }

    private fun performSearch(query: String) {
        val options = SearchOptions(
            countries = listOf("US"),
            limit = 5
        )

        searchEngine.search(query, options) { results ->
            results.onSuccess { searchResults ->
                displayResults(searchResults)
            }.onFailure { error ->
                Log.e("Search", "Error: $error")
            }
        }
    }

    private fun displayResults(results: List<SearchResult>) {
        // Display in custom RecyclerView
        handleResultSelection(results[0])
    }

    private fun handleResultSelection(result: SearchResult) {
        val coordinate = result.coordinate

        mapView.getMapboxMap().flyTo(
            CameraOptions.Builder()
                .center(Point.fromLngLat(coordinate.longitude, coordinate.latitude))
                .zoom(15.0)
                .build()
        )
    }
}
```

#### Option 3: Direct API Integration (Advanced)

**When to use:** Very specific requirements, server-side Android backend

**Important:** Only use if SDK doesn't meet your needs. You must handle debouncing and session tokens manually.

```kotlin
// Direct API calls - see Web direct API example
// Not recommended for Android - use Search SDK instead
```

### Node.js: Mapbox Search JS Core (Recommended)

#### Option 1: Search JS Core (Recommended)

**When to use:** Server-side search, backend API, serverless functions

**Installation:**
```bash
npm install @mapbox/search-js-core
```

**Complete implementation:**
```javascript
import { SearchSession } from '@mapbox/search-js-core';

// Initialize search session (handles session tokens automatically)
const search = new SearchSession({
  accessToken: process.env.MAPBOX_TOKEN
});

// Express.js API endpoint example
app.get('/api/search', async (req, res) => {
  const { query, proximity, country } = req.query;

  try {
    // Get suggestions (Search JS Core handles session management)
    const response = await search.suggest(query, {
      proximity: proximity ? proximity.split(',').map(Number) : undefined,
      country: country,
      limit: 10
    });

    res.json(response.suggestions);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Retrieve full details for a selected result
app.get('/api/search/:id', async (req, res) => {
  try {
    const result = await search.retrieve(req.params.id);
    res.json(result.features[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

**Key benefits:**
- ✅ Search JS Core handles session tokens automatically
- ✅ Perfect for serverless (Vercel, Netlify, AWS Lambda)
- ✅ Same API as browser Search JS Core
- ✅ No manual debouncing needed (handle at API gateway level)

#### Option 2: Direct API Integration (Advanced)

**When to use:** Very specific requirements, need features not in Search JS Core

**Implementation:**
```javascript
import fetch from 'node-fetch';

async function searchPlaces(query, options = {}) {
  const params = new URLSearchParams({
    q: query,
    access_token: process.env.MAPBOX_TOKEN,
    session_token: generateSessionToken(), // You must manage this
    ...options
  });

  const response = await fetch(
    `https://api.mapbox.com/search/searchbox/v1/suggest?${params}`
  );

  return response.json();
}
```

**Important:** Only use direct API calls if Search JS Core doesn't meet your needs. You'll need to handle session tokens manually.

## Best Practices: "The Good Parts"

### 1. Debouncing (CRITICAL for Autocomplete)

**Note:** Debouncing is only a concern if you are calling the API directly. Mapbox Search JS and the Search SDKs handle debouncing automatically.

**Problem:** Every keystroke = API call = expensive + slow

**Solution:** Wait until user stops typing (for direct API integration)

```javascript
let debounceTimeout;

function debouncedSearch(query) {
  clearTimeout(debounceTimeout);

  debounceTimeout = setTimeout(() => {
    performSearch(query);
  }, 300); // 300ms is optimal for most use cases
}
```

**Why 300ms?**
- Fast enough to feel responsive
- Slow enough to avoid spam
- Industry standard (Google uses ~300ms)

### 2. Session Token Management

**Note:** Session tokens are only a concern if you are calling the API directly. Mapbox Search JS and the Search SDKs for iOS/Android handle session tokens automatically.

**Problem:** Search Box API charges per session, not per request

**What's a session?**
- Starts with first suggest request
- Ends with retrieve request
- Use same token for all requests in session

**Implementation (direct API calls only):**

```javascript
class SearchSession {
  constructor() {
    this.token = this.generateToken();
  }

  generateToken() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  async suggest(query) {
    // Use this.token for all suggest requests
    return fetch(`...?session_token=${this.token}`);
  }

  async retrieve(id) {
    const result = await fetch(`...?session_token=${this.token}`);
    // Session ends - generate new token
    this.token = this.generateToken();
    return result;
  }
}
```

**Cost impact:**
- ✅ Correct: 1 session = unlimited suggests + 1 retrieve = 1 charge
- ❌ Wrong: No session token = each request charged separately

### 3. Geographic Filtering

**Always set location context when possible:**

```javascript
// GOOD: Specific country
{ country: 'US' }

// GOOD: Proximity to user
{ proximity: [-122.4194, 37.7749] }

// GOOD: Bounding box for service area
{ bbox: [-122.5, 37.7, -122.3, 37.9] }

// BAD: No geographic context
{ } // Returns global results, slower, less relevant
```

**Tip:** Use the [Location Helper tool](https://labs.mapbox.com/location-helper/) to easily calculate bounding boxes for your service area.

**Why it matters:**
- ✅ Better result relevance
- ✅ Faster response times
- ✅ Lower ambiguity
- ✅ Better user experience

### 4. Error Handling

**Handle all failure cases:**

```javascript
async function performSearch(query) {
  try {
    const response = await fetch(searchUrl);

    // Check HTTP status
    if (!response.ok) {
      if (response.status === 429) {
        // Rate limited
        showError('Too many requests. Please wait a moment.');
        return [];
      } else if (response.status === 401) {
        // Invalid token
        showError('Search is unavailable. Please check configuration.');
        return [];
      } else {
        // Other error
        showError('Search failed. Please try again.');
        return [];
      }
    }

    const data = await response.json();

    // Check for results
    if (!data.suggestions || data.suggestions.length === 0) {
      showMessage('No results found. Try a different search.');
      return [];
    }

    return data.suggestions;

  } catch (error) {
    // Network error
    console.error('Search error:', error);
    showError('Network error. Please check your connection.');
    return [];
  }
}
```

### 5. Result Display UX

**Show enough context for disambiguation:**

```html
<div class="search-result">
  <div class="result-name">Starbucks</div>
  <div class="result-address">123 Main St, San Francisco, CA</div>
  <div class="result-type">Coffee Shop</div>
</div>
```

**Not just:**
```html
<div>Starbucks</div>  <!-- Which Starbucks? -->
```

### 6. Loading States

**Always show loading feedback:**

```javascript
function performSearch(query) {
  showLoadingSpinner();

  fetch(searchUrl)
    .then(response => response.json())
    .then(data => {
      hideLoadingSpinner();
      displayResults(data.suggestions);
    })
    .catch(error => {
      hideLoadingSpinner();
      showError('Search failed');
    });
}
```

### 7. Accessibility

**Make search keyboard-navigable:**

```html
<input
  type="search"
  role="combobox"
  aria-autocomplete="list"
  aria-controls="search-results"
  aria-expanded="false"
/>

<ul id="search-results" role="listbox">
  <li role="option" tabindex="0">Result 1</li>
  <li role="option" tabindex="0">Result 2</li>
</ul>
```

**Keyboard support:**
- ⬆️⬇️ Arrow keys: Navigate results
- Enter: Select result
- Escape: Close results

### 8. Mobile Optimizations

**iOS/Android specific considerations:**

```swift
// iOS: Adjust for keyboard
NotificationCenter.default.addObserver(
    forName: UIResponder.keyboardWillShowNotification,
    object: nil,
    queue: .main
) { notification in
    // Adjust view for keyboard
}

// Handle tap outside to dismiss
let tapGesture = UITapGestureRecognizer(target: self, action: #selector(dismissKeyboard))
view.addGestureRecognizer(tapGesture)
```

**Make touch targets large enough:**
- Minimum: 44x44pt (iOS) / 48x48dp (Android)
- Ensure adequate spacing between results

### 9. Caching (For High-Volume Apps)

**Cache recent/popular searches:**

```javascript
class SearchCache {
  constructor(maxSize = 50) {
    this.cache = new Map();
    this.maxSize = maxSize;
  }

  get(query) {
    const key = query.toLowerCase();
    return this.cache.get(key);
  }

  set(query, results) {
    const key = query.toLowerCase();

    // LRU eviction
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(key, {
      results,
      timestamp: Date.now()
    });
  }

  isValid(entry, maxAgeMs = 5 * 60 * 1000) {
    return entry && (Date.now() - entry.timestamp) < maxAgeMs;
  }
}

// Usage
const cache = new SearchCache();

async function search(query) {
  const cached = cache.get(query);
  if (cache.isValid(cached)) {
    return cached.results;
  }

  const results = await performAPISearch(query);
  cache.set(query, results);
  return results;
}
```

### 10. Token Security

**CRITICAL: Scope tokens properly:**

```javascript
// Create token with only search scopes
// In Mapbox dashboard or via API:
{
  "scopes": [
    "search:read",
    "styles:read",  // Only if showing map
    "fonts:read"    // Only if showing map
  ],
  "allowedUrls": [
    "https://yourdomain.com/*"
  ]
}
```

**Never:**
- ❌ Use secret tokens (sk.*) in client-side code
- ❌ Give tokens more scopes than needed
- ❌ Skip URL restrictions on public tokens

See `mapbox-token-security` skill for details.

## Common Pitfalls and How to Avoid Them

### ❌ Pitfall 1: No Debouncing

**Problem:**
```javascript
input.addEventListener('input', (e) => {
  performSearch(e.target.value); // API call on EVERY keystroke!
});
```

**Impact:**
- 🔥 Expensive (hundreds of unnecessary API calls)
- 🐌 Slow (race conditions, outdated results)
- 💥 Rate limiting (429 errors)

**Solution:** Always debounce (see Best Practice #1)

### ❌ Pitfall 2: Ignoring Session Tokens

**Problem:**
```javascript
// No session token = each request charged separately
fetch('...suggest?q=query&access_token=xxx');
```

**Impact:**
- 💰 Costs 10-100x more than necessary
- Budget blown on redundant charges

**Solution:** Use session tokens (see Best Practice #2)

### ❌ Pitfall 3: No Geographic Context

**Problem:**
```javascript
// Searching globally for "Paris"
{ q: 'Paris' } // Paris, France? Paris, Texas? Paris, Kentucky?
```

**Impact:**
- 😕 Confusing results (wrong country)
- 🐌 Slower responses
- 😞 Poor user experience

**Solution:**
```javascript
// Much better
{ q: 'Paris', country: 'US', proximity: user_location }
```

### ❌ Pitfall 4: Poor Mobile UX

**Problem:**
```html
<!-- Tiny touch targets -->
<div style="height: 20px; padding: 2px;">Search result</div>
```

**Impact:**
- 😤 Frustrating to tap
- 🎯 Accidental selections
- ⭐ Bad reviews

**Solution:**
```css
.search-result {
  min-height: 48px;  /* Android minimum */
  padding: 12px;
  margin: 4px 0;
}
```

### ❌ Pitfall 5: Not Handling Empty Results

**Problem:**
```javascript
// Just shows empty container
displayResults([]); // User sees blank space - is it loading? broken?
```

**Impact:**
- ❓ User confusion
- 🤔 Is it working?

**Solution:**
```javascript
if (results.length === 0) {
  showMessage('No results found. Try a different search term.');
}
```

### ❌ Pitfall 6: Blocking on Slow Networks

**Problem:**
```javascript
// No timeout = waits forever on slow network
await fetch(searchUrl);
```

**Impact:**
- ⏰ Appears frozen
- 😫 User frustration

**Solution:**
```javascript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

fetch(searchUrl, { signal: controller.signal })
  .finally(() => clearTimeout(timeout));
```

### ❌ Pitfall 7: Ignoring Result Types

**Problem:**
```javascript
// Treating all results the same
displayResult(result.name); // But is it an address? POI? Region?
```

**Impact:**
- 🤷 Unclear what was selected
- 🗺️ Wrong zoom level
- 📍 Inappropriate markers

**Solution:**
```javascript
function handleResult(result) {
  const type = result.feature_type;

  if (type === 'poi') {
    map.flyTo({ center: coords, zoom: 17 }); // Close zoom
    addPOIMarker(result);
  } else if (type === 'address') {
    map.flyTo({ center: coords, zoom: 16 });
    addAddressMarker(result);
  } else if (type === 'place') {
    map.flyTo({ center: coords, zoom: 12 }); // Wider view for city
  }
}
```

### ❌ Pitfall 8: Race Conditions

**Problem:**
```javascript
// Fast typing: "san francisco"
// API responses arrive out of order:
// "san f" results arrive AFTER "san francisco" results
```

**Impact:**
- 🔀 Wrong results displayed
- 😵 Confusing UX

**Solution:**
```javascript
let searchCounter = 0;

async function performSearch(query) {
  const currentSearch = ++searchCounter;
  const results = await fetchResults(query);

  // Only display if this is still the latest search
  if (currentSearch === searchCounter) {
    displayResults(results);
  }
}
```

## Framework-Specific Guidance

### React Best Practices

**Best Practice:** Use Search JS React or Search JS Core instead of building custom hooks with direct API calls.

#### Option 1: Use Search JS React (Recommended)

```javascript
import { SearchBox } from '@mapbox/search-js-react';

// Easiest - just use the SearchBox component
function MyComponent() {
  return (
    <SearchBox
      accessToken="YOUR_TOKEN"
      onRetrieve={(result) => {
        // Handle result
      }}
      options={{
        country: 'US',
        types: 'address,poi'
      }}
    />
  );
}
```

#### Option 2: Custom Hook with Search JS Core

```javascript
import { useState, useCallback, useRef, useEffect } from 'react';
import { SearchSession } from '@mapbox/search-js-core';

// Custom hook using Search JS Core (handles debouncing and session tokens)
function useMapboxSearch(accessToken, options = {}) {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Search JS Core handles session tokens automatically
  const searchSessionRef = useRef(null);

  useEffect(() => {
    searchSessionRef.current = new SearchSession({ accessToken });
  }, [accessToken]);

  const search = useCallback(async (query) => {
    if (!query || query.length < 2) {
      setResults([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Search JS Core handles debouncing and session tokens
      const response = await searchSessionRef.current.suggest(query, options);
      setResults(response.suggestions || []);
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  }, [options]);

  const retrieve = useCallback(async (suggestion) => {
    try {
      // Search JS Core handles session tokens automatically
      const result = await searchSessionRef.current.retrieve(suggestion);
      return result.features[0];
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  return { results, isLoading, error, search, retrieve };
}
```

**Benefits of using Search JS Core:**
- ✅ No manual session token management
- ✅ No manual debouncing needed
- ✅ No race condition handling needed (SDK handles it)
- ✅ Cleaner, simpler code
- ✅ Production-ready error handling built-in

### Vue Composition API (Using Search JS Core - Recommended)

```javascript
import { ref, watch } from 'vue';
import { SearchSession } from '@mapbox/search-js-core';

export function useMapboxSearch(accessToken, options = {}) {
  const query = ref('');
  const results = ref([]);
  const isLoading = ref(false);

  // Use Search JS Core - handles debouncing and session tokens automatically
  const searchSession = new SearchSession({ accessToken });

  const performSearch = async (searchQuery) => {
    if (!searchQuery || searchQuery.length < 2) {
      results.value = [];
      return;
    }

    isLoading.value = true;

    try {
      // Search JS Core handles debouncing and session tokens
      const response = await searchSession.suggest(searchQuery, options);
      results.value = response.suggestions || [];
    } catch (error) {
      console.error('Search error:', error);
      results.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // Watch query changes (Search JS Core handles debouncing)
  watch(query, (newQuery) => {
    performSearch(newQuery);
  });

  const retrieve = async (suggestion) => {
    // Search JS Core handles session tokens automatically
    const feature = await searchSession.retrieve(suggestion);
    return feature;
  };

  return {
    query,
    results,
    isLoading,
    retrieve
  };
}
```

**Key benefits:**
- ✅ Search JS Core handles debouncing automatically (no lodash needed)
- ✅ Session tokens managed automatically (no manual token generation)
- ✅ Simpler code, fewer dependencies
- ✅ Same API works in browser and Node.js

## Testing Strategy

### Unit Tests

```javascript
// Mock fetch for testing
global.fetch = jest.fn();

describe('MapboxSearch', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('debounces search requests', async () => {
    const search = new MapboxSearch('fake-token');

    // Rapid-fire searches
    search.search('san');
    search.search('san f');
    search.search('san fr');
    search.search('san francisco');

    // Wait for debounce
    await new Promise(resolve => setTimeout(resolve, 400));

    // Should only make one API call
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  test('handles empty results', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ suggestions: [] })
    });

    const search = new MapboxSearch('fake-token');
    const results = await search.performSearch('xyz');

    expect(results).toEqual([]);
  });

  test('handles API errors', async () => {
    fetch.mockResolvedValue({
      ok: false,
      status: 429
    });

    const search = new MapboxSearch('fake-token');
    const results = await search.performSearch('test');

    expect(results).toEqual([]);
  });
});
```

### Integration Tests

```javascript
describe('Search Integration', () => {
  test('complete search flow', async () => {
    const search = new MapboxSearch(process.env.MAPBOX_TOKEN);

    // Perform search
    const suggestions = await search.performSearch('San Francisco');
    expect(suggestions.length).toBeGreaterThan(0);

    // Retrieve first result
    const feature = await search.retrieve(suggestions[0].mapbox_id);
    expect(feature.geometry.coordinates).toBeDefined();
    expect(feature.properties.name).toBe('San Francisco');
  });
});
```

## Monitoring and Analytics

### Track Key Metrics

```javascript
// Track search usage
function trackSearch(query, resultsCount) {
  analytics.track('search_performed', {
    query_length: query.length,
    results_count: resultsCount,
    had_results: resultsCount > 0
  });
}

// Track selections
function trackSelection(result, position) {
  analytics.track('search_result_selected', {
    result_type: result.feature_type,
    result_position: position,
    had_address: !!result.properties.full_address
  });
}

// Track errors
function trackError(errorType, query) {
  analytics.track('search_error', {
    error_type: errorType,
    query_length: query.length
  });
}
```

### Monitor for Issues

- 📊 Zero-result rate (should be < 20%)
- ⚡ Average response time
- 💥 Error rate
- 🎯 Selection rate (users selecting vs abandoning)
- 💰 API usage vs budget

## Checklist: Production-Ready Search

Before launching, verify:

**Configuration:**
- [ ] Token properly scoped (search:read only)
- [ ] URL restrictions configured
- [ ] Geographic filtering set (country, proximity, or bbox)
- [ ] Types parameter set based on use case
- [ ] Language parameter set if needed

**Implementation:**
- [ ] Debouncing implemented (300ms recommended)
- [ ] Session tokens used correctly
- [ ] Error handling for all failure cases
- [ ] Loading states shown
- [ ] Empty results handled gracefully
- [ ] Race conditions prevented

**UX:**
- [ ] Touch targets at least 44pt/48dp
- [ ] Results show enough context (name + address)
- [ ] Keyboard navigation works
- [ ] Accessibility attributes set
- [ ] Mobile keyboard handled properly

**Performance:**
- [ ] Caching implemented (if high volume)
- [ ] Request timeout set
- [ ] Minimal data fetched
- [ ] Bundle size optimized

**Testing:**
- [ ] Unit tests for core logic
- [ ] Integration tests with real API
- [ ] Tested on slow networks
- [ ] Tested with various query types
- [ ] Mobile device testing

**Monitoring:**
- [ ] Analytics tracking set up
- [ ] Error logging configured
- [ ] Usage monitoring in place
- [ ] Budget alerts configured

## Integration with Other Skills

**Works with:**
- **mapbox-search-patterns**: Parameter selection and optimization
- **mapbox-web-integration-patterns**: Framework-specific patterns
- **mapbox-token-security**: Token management and security
- **mapbox-web-performance-patterns**: Optimizing search performance

## Resources

- [Search Box API Documentation](https://docs.mapbox.com/api/search/search-box/)
- [Geocoding API Documentation](https://docs.mapbox.com/api/search/geocoding/)
- [Mapbox Search JS](https://docs.mapbox.com/mapbox-search-js/api/)
  - [Search JS React](https://docs.mapbox.com/mapbox-search-js/api/react/)
  - [Search JS Web](https://docs.mapbox.com/mapbox-search-js/api/web/)
  - [Search JS Core](https://docs.mapbox.com/mapbox-search-js/api/core/)
- [Search SDK for iOS](https://docs.mapbox.com/ios/search/guides/)
- [Search SDK for Android](https://docs.mapbox.com/android/search/guides/)
- [Location Helper Tool](https://labs.mapbox.com/location-helper/) - Calculate bounding boxes

## Quick Decision Guide

**User says: "I need location search"**

1. **Ask discovery questions** (Questions 1-6 above)
2. **Recommend product:**
   - Search Box API (most cases)
   - Direct API (custom needs)
   - Platform SDK (mobile)
3. **Implement with:**
   - ✅ Debouncing
   - ✅ Session tokens
   - ✅ Geographic filtering
   - ✅ Error handling
   - ✅ Good UX
4. **Test thoroughly**
5. **Monitor in production**

**Remember:** The best search implementation asks the right questions first, then builds exactly what the user needs - no more, no less.
