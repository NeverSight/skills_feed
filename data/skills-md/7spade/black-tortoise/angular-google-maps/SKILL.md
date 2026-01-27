---
name: angular-google-maps
description: Angular Google Maps (@angular/google-maps) integration for interactive map features. Use when embedding Google Maps, adding markers, polylines, polygons, info windows, or implementing map controls and event handling in Angular applications. Supports clustering, heatmaps, and drawing tools.
license: Complete terms in LICENSE.txt
---

# Angular Google Maps Skill

## Rules

### Setup and Configuration
- Import `GoogleMapsModule` from `@angular/google-maps`
- Load Google Maps script in `index.html` with API key
- Use `@types/google.maps` for TypeScript types
- Restrict API key by domain/IP for security

### Map Component
- Use `<google-map>` component with `[center]`, `[zoom]`, `[options]` bindings
- Set explicit height on `google-map` element (required for display)
- Use `google.maps.LatLngLiteral` type for positions: `{ lat: number, lng: number }`
- Handle map events: `(mapClick)`, `(mapDrag)`, `(zoomChanged)`

### Markers
- Use `<map-marker>` component inside `<google-map>`
- Set marker properties: `[position]`, `[label]`, `[title]`, `[options]`
- Handle marker events: `(mapClick)`, `(mapDragend)`
- Use marker clustering for more than 100 markers

### Info Windows
- Use `<map-info-window>` component for marker popups
- Reference info window using `@ViewChild(MapInfoWindow)`
- Call `infoWindow.open()` to display, `infoWindow.close()` to hide
- Show info window content conditionally based on selected marker

### Drawing Tools
- Use `<map-polygon>` for polygon shapes with `[paths]` and `[options]`
- Use `<map-polyline>` for lines with `[path]` and `[options]`
- Use `<map-circle>` for circles with `[center]`, `[radius]`, `[options]`
- Configure styles: `fillColor`, `strokeColor`, `opacity`, `strokeWeight`

### Geocoding
- Use `google.maps.Geocoder` for address/coordinate conversion
- Cache geocoding results to avoid repeated API calls
- Debounce geocoding requests (300-500ms) for user input
- Handle geocoding errors gracefully

### Performance
- Lazy load Google Maps script only when needed
- Use marker clustering for large datasets (>100 markers)
- Filter markers by viewport bounds
- NEVER load all markers at once for large datasets
- NEVER geocode on every keystroke without debouncing

### Security
- NEVER expose API key in client code without restrictions
- Store API key in environment configuration
- Enable Google Cloud Console API restrictions (HTTP referrers, API scope)

---

## Context

### Summary
Angular Google Maps provides official Angular bindings for Google Maps JavaScript API, enabling declarative map integration with markers, polygons, info windows, and geocoding services.

### When to Use This Skill

Activate this skill when you need to:
- Embed Google Maps in Angular components
- Add and customize map markers
- Draw polylines, polygons, and circles
- Implement info windows and custom overlays
- Handle map events (click, drag, zoom)
- Implement marker clustering
- Add heatmap layers
- Use Google Maps drawing tools
- Geocode addresses and reverse geocode coordinates
- Optimize map performance for large datasets

### Installation

```bash
npm install @angular/google-maps

# Types for TypeScript
npm install @types/google.maps
```

### Setup Steps

#### Get API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable Maps JavaScript API
4. Create API key credentials
5. Restrict API key (recommended)

#### Load Google Maps Script

```html
<!-- index.html -->
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
```

### Basic Map Component Example

```typescript
import { Component } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [GoogleMapsModule],
  template: `
    <google-map 
      [center]="center" 
      [zoom]="zoom"
      [options]="options"
      (mapClick)="onMapClick($event)">
      
      <map-marker 
        *ngFor="let marker of markers"
        [position]="marker.position"
        [label]="marker.label"
        [title]="marker.title"
        (mapClick)="onMarkerClick(marker)">
      </map-marker>
    </google-map>
  `,
  styles: [`
    google-map {
      height: 400px;
      width: 100%;
    }
  `]
})
export class MapComponent {
  center: google.maps.LatLngLiteral = { lat: 25.033, lng: 121.565 }; // Taipei
  zoom = 12;
  
  options: google.maps.MapOptions = {
    mapTypeId: 'roadmap',
    disableDefaultUI: false,
    zoomControl: true,
    scrollwheel: true
  };
  
  markers: Marker[] = [
    { position: { lat: 25.033, lng: 121.565 }, label: 'A', title: 'Taipei 101' }
  ];
  
  onMapClick(event: google.maps.MapMouseEvent) {
    if (event.latLng) {
      const newMarker = {
        position: event.latLng.toJSON(),
        label: String.fromCharCode(65 + this.markers.length),
        title: 'New Location'
      };
      this.markers.push(newMarker);
    }
  }
  
  onMarkerClick(marker: Marker) {
    console.log('Marker clicked:', marker);
  }
}

interface Marker {
  position: google.maps.LatLngLiteral;
  label?: string;
  title?: string;
}
```

### Map with Info Window Example

```typescript
@Component({
  template: `
    <google-map [center]="center" [zoom]="zoom">
      <map-marker 
        *ngFor="let marker of markers"
        [position]="marker.position"
        (mapClick)="openInfo(marker, infoWindow)">
      </map-marker>
      
      <map-info-window #infoWindow>
        <div *ngIf="selectedMarker">
          <h3>{{ selectedMarker.title }}</h3>
          <p>{{ selectedMarker.description }}</p>
        </div>
      </map-info-window>
    </google-map>
  `
})
export class MapWithInfoComponent {
  @ViewChild(MapInfoWindow) infoWindow!: MapInfoWindow;
  selectedMarker: any;
  
  openInfo(marker: any, infoWindow: MapInfoWindow) {
    this.selectedMarker = marker;
    infoWindow.open();
  }
}
```

### Marker Clustering Example

```typescript
import { MarkerClusterer } from '@googlemaps/markerclusterer';

@Component({
  template: `
    <google-map #map [center]="center" [zoom]="zoom">
      <map-marker 
        *ngFor="let marker of markers"
        [position]="marker.position">
      </map-marker>
    </google-map>
  `
})
export class ClusteredMapComponent implements AfterViewInit {
  @ViewChild('map') mapComponent!: GoogleMap;
  markers: Marker[] = [];
  
  ngAfterViewInit() {
    if (this.mapComponent.googleMap) {
      const markerClusterer = new MarkerClusterer({
        map: this.mapComponent.googleMap,
        markers: this.getGoogleMarkers()
      });
    }
  }
  
  private getGoogleMarkers(): google.maps.Marker[] {
    return this.markers.map(m => 
      new google.maps.Marker({ position: m.position })
    );
  }
}
```

### Drawing Tools Example

```typescript
@Component({
  template: `
    <google-map [center]="center" [zoom]="zoom">
      <map-polygon 
        [paths]="polygonPaths"
        [options]="polygonOptions">
      </map-polygon>
      
      <map-polyline 
        [path]="polylinePath"
        [options]="polylineOptions">
      </map-polyline>
      
      <map-circle 
        [center]="circleCenter"
        [radius]="circleRadius"
        [options]="circleOptions">
      </map-circle>
    </google-map>
  `
})
export class DrawingMapComponent {
  polygonPaths: google.maps.LatLngLiteral[] = [
    { lat: 25.033, lng: 121.565 },
    { lat: 25.035, lng: 121.567 },
    { lat: 25.031, lng: 121.569 }
  ];
  
  polygonOptions: google.maps.PolygonOptions = {
    fillColor: '#FF0000',
    fillOpacity: 0.3,
    strokeColor: '#FF0000',
    strokeOpacity: 1,
    strokeWeight: 2
  };
  
  polylinePath: google.maps.LatLngLiteral[] = [
    { lat: 25.030, lng: 121.560 },
    { lat: 25.035, lng: 121.565 }
  ];
  
  polylineOptions: google.maps.PolylineOptions = {
    strokeColor: '#0000FF',
    strokeOpacity: 1.0,
    strokeWeight: 3
  };
  
  circleCenter: google.maps.LatLngLiteral = { lat: 25.033, lng: 121.565 };
  circleRadius = 1000; // meters
  
  circleOptions: google.maps.CircleOptions = {
    fillColor: '#00FF00',
    fillOpacity: 0.2,
    strokeColor: '#00FF00',
    strokeOpacity: 0.8,
    strokeWeight: 2
  };
}
```

### Geocoding Service Example

```typescript
import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class GeocodingService {
  private geocoder = new google.maps.Geocoder();
  
  geocodeAddress(address: string): Observable<google.maps.LatLngLiteral | null> {
    return from(
      this.geocoder.geocode({ address })
    ).pipe(
      map(response => {
        if (response.results && response.results[0]) {
          const location = response.results[0].geometry.location;
          return { lat: location.lat(), lng: location.lng() };
        }
        return null;
      })
    );
  }
  
  reverseGeocode(location: google.maps.LatLngLiteral): Observable<string | null> {
    return from(
      this.geocoder.geocode({ location })
    ).pipe(
      map(response => {
        if (response.results && response.results[0]) {
          return response.results[0].formatted_address;
        }
        return null;
      })
    );
  }
}
```

### References

- [Angular Google Maps Documentation](https://github.com/angular/components/tree/main/src/google-maps)
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [MarkerClusterer](https://googlemaps.github.io/js-markerclusterer/)
