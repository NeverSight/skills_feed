---
name: publishing-platforms
version: "2.0.0"
description: |
  Platform submission processes, certification requirements, and distribution
  across Steam, Epic, console, and mobile platforms.
sasmp_version: "1.3.0"
bonded_agent: 07-game-publishing
bond_type: PRIMARY_BOND

parameters:
  - name: platform
    type: string
    required: false
    validation:
      enum: [steam, epic, playstation, xbox, nintendo, ios, android]
  - name: submission_type
    type: string
    required: false
    validation:
      enum: [initial, update, dlc, patch]

retry_policy:
  enabled: true
  max_attempts: 3
  backoff: exponential

observability:
  log_events: [start, complete, error, submission, approval]
  metrics: [submission_count, approval_rate, review_time_days]
---

# Publishing Platforms

## Platform Requirements Matrix

```
┌─────────────────────────────────────────────────────────────┐
│ STEAM                                                        │
├─────────────────────────────────────────────────────────────┤
│ □ Steamworks SDK integration                                │
│ □ Achievements, Cloud Saves, Trading Cards                  │
│ □ Store assets:                                              │
│   • Header (460x215)                                        │
│   • Capsule (231x87, 467x181, 616x353)                     │
│   • Screenshots (1920x1080 min, 5+ required)               │
│   • Trailer (MP4, 1080p recommended)                        │
│ □ Age rating (IARC)                                         │
│ □ Review time: 1-5 business days                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PLAYSTATION                                                  │
├─────────────────────────────────────────────────────────────┤
│ □ PlayStation Partners registration                         │
│ □ DevKit access                                              │
│ □ TRC (Technical Requirements Checklist)                    │
│ □ Trophies (Platinum, Gold, Silver, Bronze)                │
│ □ ESRB/PEGI rating certificate                              │
│ □ Accessibility features                                    │
│ □ Certification: 2-4 weeks                                  │
│ □ Slot fee required                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ XBOX                                                         │
├─────────────────────────────────────────────────────────────┤
│ □ Xbox Partner Center access                                │
│ □ XR (Xbox Requirements) compliance                         │
│ □ Achievements (1000G base game)                            │
│ □ Smart Delivery support                                    │
│ □ Game Pass consideration                                   │
│ □ Certification: 1-3 weeks                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ iOS APP STORE                                                │
├─────────────────────────────────────────────────────────────┤
│ □ Apple Developer Program ($99/year)                        │
│ □ App Store Connect setup                                   │
│ □ App icons (1024x1024)                                     │
│ □ Screenshots per device size                               │
│ □ Privacy policy URL                                        │
│ □ App Review Guidelines compliance                          │
│ □ IAP testing with sandbox                                  │
│ □ Review time: 24-48 hours (typically)                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ GOOGLE PLAY                                                  │
├─────────────────────────────────────────────────────────────┤
│ □ Google Play Console ($25 one-time)                        │
│ □ App signing with Play App Signing                         │
│ □ Store listing assets                                      │
│ □ Content rating questionnaire                              │
│ □ Data safety form                                          │
│ □ Target API level compliance                               │
│ □ Review time: Hours to 7 days                             │
└─────────────────────────────────────────────────────────────┘
```

## Steam Integration

```csharp
// ✅ Production-Ready: Steamworks Integration
public class SteamManager : MonoBehaviour
{
    public static SteamManager Instance { get; private set; }
    public static bool Initialized { get; private set; }

    [SerializeField] private uint _appId = 480; // Test app ID

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        try
        {
            if (SteamAPI.RestartAppIfNecessary(new AppId_t(_appId)))
            {
                Application.Quit();
                return;
            }

            Initialized = SteamAPI.Init();
            if (!Initialized)
            {
                Debug.LogError("[Steam] Failed to initialize. Is Steam running?");
                return;
            }

            Debug.Log($"[Steam] Initialized. User: {SteamFriends.GetPersonaName()}");
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[Steam] Exception: {e.Message}");
        }
    }

    private void Update()
    {
        if (Initialized)
            SteamAPI.RunCallbacks();
    }

    public void UnlockAchievement(string achievementId)
    {
        if (!Initialized) return;

        SteamUserStats.SetAchievement(achievementId);
        SteamUserStats.StoreStats();
    }

    private void OnApplicationQuit()
    {
        if (Initialized)
            SteamAPI.Shutdown();
    }
}
```

## Submission Checklist

```
PRE-SUBMISSION CHECKLIST:
┌─────────────────────────────────────────────────────────────┐
│  BUILD PREPARATION:                                          │
│  □ Final QA pass completed                                  │
│  □ All known critical bugs fixed                            │
│  □ Performance targets met                                  │
│  □ Build size optimized                                     │
│  □ Version number updated                                   │
├─────────────────────────────────────────────────────────────┤
│  STORE ASSETS:                                               │
│  □ All required images uploaded                             │
│  □ Trailer uploaded and reviewed                            │
│  □ Store description finalized                              │
│  □ Tags and categories set                                  │
│  □ Pricing configured                                       │
├─────────────────────────────────────────────────────────────┤
│  LEGAL/COMPLIANCE:                                           │
│  □ Age rating obtained                                      │
│  □ Privacy policy published                                 │
│  □ EULA prepared (if needed)                                │
│  □ Copyright/trademark cleared                              │
├─────────────────────────────────────────────────────────────┤
│  PLATFORM-SPECIFIC:                                          │
│  □ SDK properly integrated                                  │
│  □ Achievements/trophies configured                         │
│  □ Cloud save working                                       │
│  □ Platform TRC/XR requirements checked                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Steam review rejected                              │
├─────────────────────────────────────────────────────────────┤
│ COMMON REASONS:                                              │
│ • Incorrect content descriptors                             │
│ • Missing EULA/privacy policy                               │
│ • Store assets don't meet specs                             │
│ • Build crashes on launch                                   │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Read rejection reason carefully                           │
│ → Update specific items mentioned                           │
│ → Retest before resubmitting                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Console certification failed                       │
├─────────────────────────────────────────────────────────────┤
│ COMMON REASONS:                                              │
│ • TRC/XR violation                                          │
│ • Crash during suspend/resume                               │
│ • Memory usage exceeds limits                               │
│ • Missing required features                                 │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Address each failure point specifically                   │
│ → Rerun full certification tests locally                    │
│ → Document fixes for future submissions                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: App Store rejection                                │
├─────────────────────────────────────────────────────────────┤
│ COMMON REASONS:                                              │
│ • Guideline 4.3 (spam/duplicate)                            │
│ • IAP issues                                                │
│ • Privacy concerns                                          │
│ • Crashes or bugs                                           │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Review App Store Guidelines                               │
│ → Appeal if rejection seems incorrect                       │
│ → Request phone call with reviewer                          │
└─────────────────────────────────────────────────────────────┘
```

## Platform Comparison

| Platform | Fee | Revenue Share | Review Time |
|----------|-----|---------------|-------------|
| Steam | $100/game | 70/30 (scaling) | 1-5 days |
| Epic | None | 88/12 | 1-2 weeks |
| PlayStation | Slot fee | 70/30 | 2-4 weeks |
| Xbox | Free (ID@Xbox) | 70/30 | 1-3 weeks |
| iOS | $99/year | 70/30 (85/15) | 1-2 days |
| Android | $25 one-time | 85/15 | Hours-7 days |

---

**Use this skill**: When publishing games, meeting platform requirements, or distributing across platforms.
