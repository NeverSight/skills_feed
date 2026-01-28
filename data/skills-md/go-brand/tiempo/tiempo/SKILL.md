---
name: tiempo
description: Use when working with dates, times, timezones, or datetime conversions in TypeScript/JavaScript. Provides guidance on using the tiempo library for timezone-safe datetime handling with the Temporal API.
---

# tiempo - Timezone-Safe Datetime Handling

Lightweight utility library for timezone conversions built on the Temporal API.

```bash
npm install @gobrand/tiempo
```

## Best Practices

- **Always use explicit timezones** - Never rely on implicit timezone behavior. [details](references/best-practices/explicit-timezone.md)
- **Don't use JavaScript Date** - Use tiempo instead of Date for timezone work. [details](references/best-practices/no-js-date.md)
- **Store UTC, display local** - Backend stores UTC, frontend converts for display. [details](references/best-practices/utc-storage.md)

---

## Conversion

| Function | Description | Reference |
|----------|-------------|-----------|
| `toZonedTime()` | Convert to a timezone-aware ZonedDateTime | [details](references/conversion/to-zoned-time.md) |
| `toPlainTime()` | Parse a plain time or extract wall-clock time from a datetime | [details](references/conversion/to-plain-time.md) |
| `toPlainDate()` | Parse a plain date or extract calendar date from a datetime | [details](references/conversion/to-plain-date.md) |
| `toUtc()` | Convert to a UTC Instant | [details](references/conversion/to-utc.md) |
| `toIso()` | Convert to an ISO 8601 string | [details](references/conversion/to-iso.md) |
| `toIso9075()` | Convert to ISO 9075 (SQL) format string | [details](references/conversion/to-iso9075.md) |
| `toDate()` | Convert to a JavaScript Date object | [details](references/conversion/to-date.md) |

## Current Time

| Function | Description | Reference |
|----------|-------------|-----------|
| `now()` | Get the current date and time as a ZonedDateTime | [details](references/current-time/now.md) |
| `today()` | Get today's date as a PlainDate | [details](references/current-time/today.md) |

## Formatting

| Function | Description | Reference |
|----------|-------------|-----------|
| `format()` | Format a datetime using date-fns-like format tokens | [details](references/formatting/format.md) |
| `formatPlainDate()` | Format a PlainDate using date-fns-like format tokens | [details](references/formatting/format-plain-date.md) |
| `simpleFormat()` | Human-friendly date/time formatting with explicit control over what to display | [details](references/formatting/simple-format.md) |
| `intlFormatDistance()` | Format the distance between dates as human-readable, internationalized strings | [details](references/formatting/intl-format-distance.md) |

## Arithmetic

| Function | Description | Reference |
|----------|-------------|-----------|
| `addYears()` | Add years to a datetime | [details](references/arithmetic/add-years.md) |
| `addMonths()` | Add months to a datetime | [details](references/arithmetic/add-months.md) |
| `addWeeks()` | Add weeks to a datetime | [details](references/arithmetic/add-weeks.md) |
| `addDays()` | Add days to a datetime (DST-safe) | [details](references/arithmetic/add-days.md) |
| `addHours()` | Add hours to a datetime | [details](references/arithmetic/add-hours.md) |
| `addMinutes()` | Add minutes to a datetime | [details](references/arithmetic/add-minutes.md) |
| `addSeconds()` | Add seconds to a datetime | [details](references/arithmetic/add-seconds.md) |
| `addMilliseconds()` | Add milliseconds to a datetime | [details](references/arithmetic/add-milliseconds.md) |
| `addMicroseconds()` | Add microseconds to a datetime | [details](references/arithmetic/add-microseconds.md) |
| `addNanoseconds()` | Add nanoseconds to a datetime | [details](references/arithmetic/add-nanoseconds.md) |
| `subYears()` | Subtract years from a datetime | [details](references/arithmetic/sub-years.md) |
| `subMonths()` | Subtract months from a datetime | [details](references/arithmetic/sub-months.md) |
| `subWeeks()` | Subtract weeks from a datetime | [details](references/arithmetic/sub-weeks.md) |
| `subDays()` | Subtract days from a datetime | [details](references/arithmetic/sub-days.md) |
| `subHours()` | Subtract hours from a datetime | [details](references/arithmetic/sub-hours.md) |
| `subMinutes()` | Subtract minutes from a datetime | [details](references/arithmetic/sub-minutes.md) |
| `subSeconds()` | Subtract seconds from a datetime | [details](references/arithmetic/sub-seconds.md) |
| `subMilliseconds()` | Subtract milliseconds from a datetime | [details](references/arithmetic/sub-milliseconds.md) |
| `subMicroseconds()` | Subtract microseconds from a datetime | [details](references/arithmetic/sub-microseconds.md) |
| `subNanoseconds()` | Subtract nanoseconds from a datetime | [details](references/arithmetic/sub-nanoseconds.md) |

## Boundaries

| Function | Description | Reference |
|----------|-------------|-----------|
| `startOfDay()` | Get the first moment of the day | [details](references/boundaries/start-of-day.md) |
| `endOfDay()` | Get the last moment of the day | [details](references/boundaries/end-of-day.md) |
| `startOfWeek()` | Get the first moment of the week (Monday) | [details](references/boundaries/start-of-week.md) |
| `endOfWeek()` | Get the last moment of the week (Sunday) | [details](references/boundaries/end-of-week.md) |
| `startOfMonth()` | Get the first moment of the month | [details](references/boundaries/start-of-month.md) |
| `endOfMonth()` | Get the last moment of the month | [details](references/boundaries/end-of-month.md) |
| `startOfYear()` | Get the first moment of the year | [details](references/boundaries/start-of-year.md) |
| `endOfYear()` | Get the last moment of the year | [details](references/boundaries/end-of-year.md) |

## Comparison

| Function | Description | Reference |
|----------|-------------|-----------|
| `isBefore()` | Check if one datetime is before another | [details](references/comparison/is-before.md) |
| `isAfter()` | Check if one datetime is after another | [details](references/comparison/is-after.md) |
| `isWithinInterval()` | Check if a datetime falls within an interval | [details](references/comparison/is-within-interval.md) |
| `isFuture()` | Check if a datetime is in the future | [details](references/comparison/is-future.md) |
| `isPast()` | Check if a datetime is in the past | [details](references/comparison/is-past.md) |
| `isSameDay()` | Check if two datetimes are on the same calendar day | [details](references/comparison/is-same-day.md) |
| `isSameWeek()` | Check if two datetimes are in the same ISO week | [details](references/comparison/is-same-week.md) |
| `isSameMonth()` | Check if two datetimes are in the same calendar month | [details](references/comparison/is-same-month.md) |
| `isSameYear()` | Check if two datetimes are in the same calendar year | [details](references/comparison/is-same-year.md) |
| `isSameHour()` | Check if two datetimes are in the same hour | [details](references/comparison/is-same-hour.md) |
| `isSameMinute()` | Check if two datetimes are in the same minute | [details](references/comparison/is-same-minute.md) |
| `isSameSecond()` | Check if two datetimes are in the same second | [details](references/comparison/is-same-second.md) |
| `isSameMillisecond()` | Check if two datetimes are in the same millisecond | [details](references/comparison/is-same-millisecond.md) |
| `isSameMicrosecond()` | Check if two datetimes are in the same microsecond | [details](references/comparison/is-same-microsecond.md) |
| `isSameNanosecond()` | Check if two datetimes are in the same nanosecond | [details](references/comparison/is-same-nanosecond.md) |
| `isPlainDateBefore()` | Check if a PlainDate is before another PlainDate | [details](references/comparison/is-plain-date-before.md) |
| `isPlainDateAfter()` | Check if a PlainDate is after another PlainDate | [details](references/comparison/is-plain-date-after.md) |
| `isPlainDateEqual()` | Check if two PlainDates are equal | [details](references/comparison/is-plain-date-equal.md) |
| `isPlainTimeBefore()` | Check if a PlainTime is before another PlainTime | [details](references/comparison/is-plain-time-before.md) |
| `isPlainTimeAfter()` | Check if a PlainTime is after another PlainTime | [details](references/comparison/is-plain-time-after.md) |
| `isPlainTimeEqual()` | Check if two PlainTimes are equal | [details](references/comparison/is-plain-time-equal.md) |

## Difference

| Function | Description | Reference |
|----------|-------------|-----------|
| `differenceInYears()` | Calculate the difference between two dates in years | [details](references/difference/difference-in-years.md) |
| `differenceInMonths()` | Calculate the difference between two dates in months | [details](references/difference/difference-in-months.md) |
| `differenceInWeeks()` | Calculate the difference between two dates in weeks | [details](references/difference/difference-in-weeks.md) |
| `differenceInDays()` | Calculate the difference between two dates in days | [details](references/difference/difference-in-days.md) |
| `differenceInHours()` | Calculate the difference between two dates in hours | [details](references/difference/difference-in-hours.md) |
| `differenceInMinutes()` | Calculate the difference between two dates in minutes | [details](references/difference/difference-in-minutes.md) |
| `differenceInSeconds()` | Calculate the difference between two dates in seconds | [details](references/difference/difference-in-seconds.md) |
| `differenceInMilliseconds()` | Calculate the difference between two datetimes in milliseconds | [details](references/difference/difference-in-milliseconds.md) |
| `differenceInMicroseconds()` | Calculate the difference between two datetimes in microseconds | [details](references/difference/difference-in-microseconds.md) |
| `differenceInNanoseconds()` | Calculate the difference between two datetimes in nanoseconds | [details](references/difference/difference-in-nanoseconds.md) |

## Intervals

| Function | Description | Reference |
|----------|-------------|-----------|
| `eachYearOfInterval()` | Get all years in an interval as ZonedDateTime array | [details](references/intervals/each-year-of-interval.md) |
| `eachMonthOfInterval()` | Get all months in an interval as ZonedDateTime array | [details](references/intervals/each-month-of-interval.md) |
| `eachWeekOfInterval()` | Get all weeks (ISO Monday start) in an interval as ZonedDateTime array | [details](references/intervals/each-week-of-interval.md) |
| `eachDayOfInterval()` | Get all days in an interval as ZonedDateTime array | [details](references/intervals/each-day-of-interval.md) |
| `eachHourOfInterval()` | Get all hours in an interval as ZonedDateTime array | [details](references/intervals/each-hour-of-interval.md) |
| `eachMinuteOfInterval()` | Get all minutes in an interval as ZonedDateTime array | [details](references/intervals/each-minute-of-interval.md) |

## Utilities

| Function | Description | Reference |
|----------|-------------|-----------|
| `browserTimezone()` | Get the browser/device timezone | [details](references/utilities/browser-timezone.md) |
| `roundToNearestHour()` | Round a datetime to the nearest hour boundary | [details](references/utilities/round-to-nearest-hour.md) |
| `roundToNearestMinute()` | Round a datetime to the nearest minute boundary | [details](references/utilities/round-to-nearest-minute.md) |
| `roundToNearestSecond()` | Round a datetime to the nearest second boundary | [details](references/utilities/round-to-nearest-second.md) |

## Types

```ts
import type { Timezone, IANATimezone } from '@gobrand/tiempo';

// Timezone: accepts IANA timezones + "UTC"
const tz: Timezone = 'America/New_York';  // Autocomplete for 400+ timezones

// IANATimezone: strictly IANA identifiers (excludes "UTC")
const iana: IANATimezone = 'Europe/London';
```
