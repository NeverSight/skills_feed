---
name: spam-prevention
description: When the user needs to prevent spam signups, bot accounts, fake registrations, or abuse of signup/trial flows. Also use when mentioning "spam accounts," "fake signups," "bot registrations," "disposable emails," "signup abuse," or "trial fraud." For broader security concerns, see saas-security.
---

# Spam & Bot Prevention for SaaS

Expert guidance for preventing spam signups, bot accounts, and abuse of registration and trial flows in SaaS applications.

## Core Principles

- **Layer defenses** — no single technique stops all spam; combine multiple signals
- **Minimize friction for real users** — invisible protections first, visible challenges only when needed
- **Fail closed on high-risk signals** — block or queue for review rather than letting spam through
- **Monitor and adapt** — spammers evolve; your defenses must too

## Defense Layers (Priority Order)

### Layer 1: Invisible Protections (Zero Friction)

These run silently — real users never notice them.

#### Honeypot Fields

Add hidden form fields that real users won't fill in but bots will.

```html
<!-- Hidden from real users via CSS -->
<div style="position: absolute; left: -9999px;" aria-hidden="true">
  <label for="website">Website</label>
  <input type="text" name="website" id="website" tabindex="-1" autocomplete="off" />
</div>
```

```elixir
# Server-side: reject if honeypot field has a value
def create(conn, %{"user" => user_params}) do
  if user_params["website"] && user_params["website"] != "" do
    # Bot detected — return fake success (don't reveal detection)
    conn
    |> put_flash(:info, "Check your email to confirm your account.")
    |> redirect(to: ~p"/")
  else
    # Real signup flow
    Accounts.register_user(user_params)
  end
end
```

#### Time-Based Detection

Bots submit forms instantly. Real users take time.

```elixir
# Add a hidden timestamp field
def new(conn, _params) do
  token = Phoenix.Token.sign(conn, "form_time", System.system_time(:second))
  render(conn, :new, form_token: token)
end

def create(conn, %{"form_token" => token} = params) do
  case Phoenix.Token.verify(conn, "form_time", token, max_age: 3600) do
    {:ok, timestamp} ->
      elapsed = System.system_time(:second) - timestamp
      if elapsed < 3 do
        # Submitted in under 3 seconds — likely bot
        fake_success_response(conn)
      else
        real_signup(conn, params)
      end
    {:error, _} ->
      fake_success_response(conn)
  end
end
```

#### JavaScript Challenge

Many bots don't execute JavaScript. Require a JS-generated token.

```javascript
// On page load, generate a token after a delay
setTimeout(() => {
  document.getElementById('js_token').value = btoa(Date.now().toString());
}, 1000);
```

```elixir
# Server: reject if js_token is missing or invalid
if is_nil(params["js_token"]) or params["js_token"] == "" do
  fake_success_response(conn)
end
```

### Layer 2: Email Verification

#### Disposable Email Blocking

Block known throwaway email domains.

```elixir
# Use a library like `disposable_email_domains` or maintain your own list
@disposable_domains File.read!("priv/disposable_domains.txt")
  |> String.split("\n", trim: true)
  |> MapSet.new()

def validate_email_domain(changeset) do
  validate_change(changeset, :email, fn :email, email ->
    domain = email |> String.split("@") |> List.last() |> String.downcase()
    if MapSet.member?(@disposable_domains, domain) do
      [email: "please use a permanent email address"]
    else
      []
    end
  end)
end
```

**Sources for disposable domain lists:**
- [disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains) (community-maintained, 100k+ domains)
- Services: Kickbox, ZeroBounce, NeverBounce (API-based, real-time)

#### Email Confirmation Flow

Require email verification before activating accounts.

```elixir
def register_user(attrs) do
  %User{}
  |> User.registration_changeset(attrs)
  |> Ecto.Changeset.put_change(:confirmed_at, nil)
  |> Repo.insert()
  |> case do
    {:ok, user} ->
      deliver_confirmation_email(user)
      {:ok, user}
    error -> error
  end
end

# Don't allow login until confirmed
def get_user_by_email_and_password(email, password) do
  user = Repo.get_by(User, email: email)
  if user && user.confirmed_at && User.valid_password?(user, password) do
    user
  end
end
```

#### MX Record Validation

Verify the email domain actually has mail servers.

```elixir
def valid_mx_record?(email) do
  domain = email |> String.split("@") |> List.last()
  case :inet_res.lookup(to_charlist(domain), :in, :mx) do
    [] -> false
    _records -> true
  end
end
```

### Layer 3: Rate Limiting

#### IP-Based Rate Limiting

```elixir
# Using Hammer (Elixir rate limiter)
def create(conn, params) do
  ip = conn.remote_ip |> :inet.ntoa() |> to_string()

  case Hammer.check_rate("signup:#{ip}", 60_000, 5) do
    {:allow, _count} ->
      real_signup(conn, params)
    {:deny, _limit} ->
      conn
      |> put_status(429)
      |> put_flash(:error, "Too many signup attempts. Please try again later.")
      |> render(:new)
  end
end
```

#### Fingerprint-Based Rate Limiting

IP alone isn't enough — use browser fingerprinting for additional signal.

```javascript
// Client-side: generate a fingerprint hash
// Use a library like FingerprintJS (free tier available)
import FingerprintJS from '@fingerprintjs/fingerprintjs';
const fp = await FingerprintJS.load();
const result = await fp.get();
document.getElementById('fp').value = result.visitorId;
```

```elixir
# Server: rate limit per fingerprint too
case Hammer.check_rate("signup:fp:#{params["fp"]}", 86_400_000, 3) do
  {:allow, _} -> proceed()
  {:deny, _} -> block()
end
```

### Layer 4: CAPTCHA (Visible Friction)

Use only when invisible layers aren't enough, or as escalation for suspicious behavior.

#### Progressive CAPTCHA

Don't show CAPTCHA to everyone — only when risk signals are present.

```elixir
def needs_captcha?(conn, params) do
  ip = conn.remote_ip |> :inet.ntoa() |> to_string()

  cond do
    # High signup rate from this IP
    Hammer.check_rate_inc("signup_check:#{ip}", 3_600_000, 10) == {:deny, 10} -> true
    # Disposable email domain
    disposable_email?(params["email"]) -> true
    # Missing JS token (possible bot)
    is_nil(params["js_token"]) -> true
    # Default: no captcha needed
    true -> false
  end
end
```

**CAPTCHA Options (ranked by UX):**
1. **Cloudflare Turnstile** — invisible/managed, free, privacy-friendly
2. **hCaptcha** — privacy-focused, pays publishers
3. **ALTCHA** — self-hosted, GDPR-compliant, proof-of-work based
4. **reCAPTCHA v3** — invisible scoring (but Google tracking concerns)
5. **reCAPTCHA v2** — checkbox/image challenges (most friction)

### Layer 5: Post-Signup Detection

Catch spam that gets through initial defenses.

#### Behavioral Signals

```elixir
defmodule MyApp.SpamDetection do
  def spam_score(user) do
    score = 0

    # No profile completed within 24 hours
    score = if is_nil(user.name), do: score + 1, else: score

    # No meaningful actions taken
    score = if user.actions_count == 0 and hours_since_signup(user) > 2,
      do: score + 2, else: score

    # Suspicious email patterns (random strings)
    score = if random_looking_email?(user.email), do: score + 2, else: score

    # Signed up from known VPN/proxy
    score = if vpn_ip?(user.signup_ip), do: score + 1, else: score

    score
  end

  defp random_looking_email?(email) do
    local = email |> String.split("@") |> List.first()
    # High ratio of digits to letters, or very long random strings
    digit_ratio = local |> String.graphemes() |> Enum.count(&(&1 =~ ~r/\d/)) |> Kernel./(String.length(local))
    digit_ratio > 0.5 or String.length(local) > 20
  end
end
```

#### Automated Cleanup

```elixir
# Oban job to clean unconfirmed accounts
defmodule MyApp.Workers.CleanupUnconfirmed do
  use Oban.Worker, queue: :maintenance

  @impl Oban.Worker
  def perform(_job) do
    cutoff = DateTime.utc_now() |> DateTime.add(-72, :hour)

    from(u in User,
      where: is_nil(u.confirmed_at),
      where: u.inserted_at < ^cutoff
    )
    |> Repo.delete_all()

    :ok
  end
end
```

## Implementation Checklist

### Minimum Viable Protection (Start Here)
- [ ] Honeypot field on signup form
- [ ] Email confirmation required before account activation
- [ ] Disposable email domain blocking
- [ ] IP-based rate limiting (5 signups/hour per IP)
- [ ] Clean up unconfirmed accounts after 72 hours

### Enhanced Protection
- [ ] Time-based form submission detection
- [ ] JavaScript challenge token
- [ ] MX record validation
- [ ] Progressive CAPTCHA (Cloudflare Turnstile)
- [ ] Browser fingerprint rate limiting

### Advanced Protection
- [ ] Post-signup behavioral scoring
- [ ] VPN/proxy detection
- [ ] Phone number verification for high-value actions
- [ ] Machine learning anomaly detection
- [ ] Manual review queue for borderline cases

## Monitoring & Metrics

Track these to know if your defenses are working:

| Metric | What It Tells You |
|--------|-------------------|
| Signup-to-confirmation rate | Low = spam getting through signup |
| Confirmation-to-activation rate | Low = real users having trouble |
| Signups per IP per hour | Spikes = bot attack |
| Disposable email block rate | Rising = targeted by spam |
| CAPTCHA trigger rate | Too high = too aggressive; too low = too lenient |
| False positive rate | Real users being blocked (monitor support tickets) |

## Common Mistakes

- **Blocking too aggressively** — false positives lose real customers. Start lenient, tighten based on data.
- **Relying on CAPTCHA alone** — bots solve CAPTCHAs. Layer defenses.
- **Revealing detection** — don't tell bots they were caught. Return fake success responses.
- **Hardcoding disposable domains** — the list grows daily. Use an updated source or API.
- **No monitoring** — you won't know defenses failed until spam is everywhere.
- **Blocking VPNs entirely** — many legitimate users use VPNs. Use as a signal, not a block.

## Related Skills

- **saas-security**: Broader security (auth, API protection, account takeover)
- **stripe-integration**: Payment verification as anti-spam signal
- **email-sequence**: Confirmation and verification email flows
