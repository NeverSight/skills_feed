---
name: weather-query
description: 查询中国各地实时天气和天气预报，包括温度、湿度、风速、空气质量等信息。Use when users ask about weather conditions, forecasts, or climate information for locations in China.
license: MIT
metadata:
  author: vikiboss
  version: "1.0"
  api_base: https://60s.viki.moe/v2
  tags:
    - weather
    - forecast
    - china
    - climate
---

# Weather Query Skill

This skill enables AI agents to fetch real-time weather information and forecasts for locations in China using the 60s API.

## When to Use This Skill

Use this skill when users:
- Ask about current weather conditions
- Want weather forecasts
- Need temperature, humidity, wind information
- Request air quality data
- Plan outdoor activities and need weather info

## API Endpoints

### 1. Real-time Weather
**URL:** `https://60s.viki.moe/v2/weather/realtime`  
**Method:** GET

### 2. Weather Forecast
**URL:** `https://60s.viki.moe/v2/weather/forecast`  
**Method:** GET

## Parameters

- `location` (required): Location name in Chinese
  - Can be city name: "北京", "上海", "广州"
  - Can be district name: "海淀区", "浦东新区"

## How to Use

### Get Real-time Weather

```python
import requests

def get_realtime_weather(location):
    url = 'https://60s.viki.moe/v2/weather/realtime'
    response = requests.get(url, params={'location': location})
    return response.json()

# Example
weather = get_realtime_weather('北京')
print(f"☁️ {weather['location']}天气")
print(f"🌡️ 温度：{weather['temperature']}°C")
print(f"💨 风速：{weather['wind']}")
print(f"💧 湿度：{weather['humidity']}")
```

### Get Weather Forecast

```python
def get_weather_forecast(location):
    url = 'https://60s.viki.moe/v2/weather/forecast'
    response = requests.get(url, params={'location': location})
    return response.json()

# Example
forecast = get_weather_forecast('上海')
for day in forecast['forecast']:
    print(f"{day['date']}: {day['weather']} {day['temp_low']}°C ~ {day['temp_high']}°C")
```

### Simple bash example

```bash
# Real-time weather
curl "https://60s.viki.moe/v2/weather/realtime?location=北京"

# Weather forecast
curl "https://60s.viki.moe/v2/weather/forecast?location=上海"
```

## Response Format

### Real-time Weather Response

```json
{
  "location": "北京",
  "weather": "晴",
  "temperature": "15",
  "humidity": "45%",
  "wind": "东北风3级",
  "air_quality": "良",
  "updated": "2024-01-15 14:00:00"
}
```

### Forecast Response

```json
{
  "location": "上海",
  "forecast": [
    {
      "date": "2024-01-15",
      "day_of_week": "星期一",
      "weather": "多云",
      "temp_low": "10",
      "temp_high": "18",
      "wind": "东风3-4级"
    },
    ...
  ]
}
```

## Example Interactions

### User: "北京今天天气怎么样？"

**Agent Response:**
```python
weather = get_realtime_weather('北京')
response = f"""
☁️ 北京今日天气

天气状况：{weather['weather']}
🌡️ 温度：{weather['temperature']}°C
💧 湿度：{weather['humidity']}
💨 风力：{weather['wind']}
🌫️ 空气质量：{weather['air_quality']}
"""
```

### User: "上海未来三天天气"

```python
forecast = get_weather_forecast('上海')
response = "📅 上海未来天气预报\n\n"
for day in forecast['forecast'][:3]:
    response += f"{day['date']} {day['day_of_week']}\n"
    response += f"  {day['weather']} {day['temp_low']}°C ~ {day['temp_high']}°C\n"
    response += f"  {day['wind']}\n\n"
```

### User: "深圳会下雨吗？"

```python
weather = get_realtime_weather('深圳')
if '雨' in weather['weather']:
    print("☔ 是的，深圳现在正在下雨")
    print("建议带伞出门！")
else:
    forecast = get_weather_forecast('深圳')
    rain_days = [d for d in forecast['forecast'] if '雨' in d['weather']]
    if rain_days:
        print(f"未来{rain_days[0]['date']}可能会下雨")
    else:
        print("近期没有降雨预报")
```

## Best Practices

1. **Location Names**: Always use Chinese characters for location names
2. **Error Handling**: Check if the location is valid before displaying results
3. **Context**: Provide relevant context based on weather conditions
   - Rain: Suggest bringing umbrella
   - Hot: Recommend staying hydrated
   - Cold: Advise wearing warm clothes
   - Poor AQI: Suggest wearing mask

4. **Caching**: Weather data is updated regularly but can be cached for short periods
5. **Fallbacks**: If a specific district doesn't work, try the city name

## Common Use Cases

### 1. Weather-based Recommendations

```python
def give_weather_advice(location):
    weather = get_realtime_weather(location)
    advice = []
    
    temp = int(weather['temperature'])
    if temp > 30:
        advice.append("🔥 天气炎热，注意防暑降温，多喝水")
    elif temp < 5:
        advice.append("🥶 天气寒冷，注意保暖")
    
    if '雨' in weather['weather']:
        advice.append("☔ 记得带伞")
    
    if weather['air_quality'] in ['差', '重度污染']:
        advice.append("😷 空气质量不佳，建议戴口罩")
    
    return '\n'.join(advice)
```

### 2. Multi-city Weather Comparison

```python
def compare_weather(cities):
    results = []
    for city in cities:
        weather = get_realtime_weather(city)
        results.append({
            'city': city,
            'temperature': int(weather['temperature']),
            'weather': weather['weather']
        })
    
    # Find hottest and coldest
    hottest = max(results, key=lambda x: x['temperature'])
    coldest = min(results, key=lambda x: x['temperature'])
    
    return f"🌡️ 最热: {hottest['city']} {hottest['temperature']}°C\n" \
           f"❄️ 最冷: {coldest['city']} {coldest['temperature']}°C"
```

### 3. Travel Weather Check

```python
def check_travel_weather(destination, days=3):
    forecast = get_weather_forecast(destination)
    suitable_days = []
    
    for day in forecast['forecast'][:days]:
        if '雨' not in day['weather'] and '雪' not in day['weather']:
            suitable_days.append(day['date'])
    
    if suitable_days:
        return f"✅ {destination}适合出行的日期：{', '.join(suitable_days)}"
    else:
        return f"⚠️ 未来{days}天{destination}天气不太适合出行"
```

## Troubleshooting

### Issue: Location not found
- **Solution**: Try using the main city name instead of district
- Example: Use "北京" instead of "朝阳区"

### Issue: No forecast data
- **Solution**: Verify the location name is correct
- Try standard city names: 北京, 上海, 广州, 深圳, etc.

### Issue: Data seems outdated
- **Solution**: The API updates regularly, but weather can change quickly
- Check the `updated` timestamp in the response

## Supported Locations

The weather API supports most cities and districts in China, including:
- Provincial capitals: 北京, 上海, 广州, 深圳, 成都, 杭州, 南京, 武汉, etc.
- Major cities: 苏州, 青岛, 大连, 厦门, etc.
- Districts: 海淀区, 朝阳区, 浦东新区, etc.

## Related Resources

- [60s API Documentation](https://docs.60s-api.viki.moe)
- [GitHub Repository](https://github.com/vikiboss/60s)
