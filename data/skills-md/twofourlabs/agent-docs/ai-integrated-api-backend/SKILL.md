---
name: ai-integrated-api-backend
description: Comprehensive guide for building production-grade AI-integrated backends with multi-provider support, intelligent fallback mechanisms, region configuration, prompt management with variables/tools, and session-based billing. Use when implementing AI features in Django/Python backends or designing LLM-powered API architectures with external data integration.
---

<objective>
This skill provides exhaustive knowledge for building robust, production-grade AI-integrated backend systems featuring:
- **Multi-Provider Architecture**: OpenAI, Anthropic, Gemini, AWS Bedrock, Byteplus, OpenRouter with seamless switching
- **Intelligent Fallbacks**: Automatic degradation chains (e.g., GPT-4 → Claude → Gemini-Flash)
- **Region-Based Routing**: AWS Bedrock multi-region support, geographic failover
- **Advanced Prompt Management**: Template-driven prompts with {{variable}} substitution, function mapping, YAML-structured instructions
- **External API Integration**: Weather, astrology, finance APIs → AI transformation pipelines
- **Session & Billing**: Per-message charging, wallet deduction, price locking
- **Gateway Pattern**: JWT-authenticated internal LLM gateway for centralized AI access
</objective>

<essential_principles>
## Core Architecture Principles

**1. Multi-Provider Design Philosophy**
- Never depend on a single AI provider; always maintain fallback chains
- Design provider-agnostic interfaces that abstract vendor-specific implementations
- Implement graceful degradation when premium models fail (e.g., GPT-4 → GPT-3.5 → Gemini-Flash)
- Use configuration-driven provider selection, not hardcoded logic
- Support multiple providers simultaneously (A/B testing, cost optimization)

**2. Separation of Concerns**
- **Models Layer**: Database models for bots, LLM configs, prompts, sessions (Django ORM)
- **Services Layer**: Provider-specific integrations (OpenAI, Anthropic, Gemini, Bedrock, etc.)
- **Helpers Layer**: Business logic for prompt rendering, fallback routing, response handling
- **Gateway Layer**: Central JWT-authenticated service for LLM API access
- **API Layer**: External API managers for weather, astrology, finance data

**3. Configuration Over Code**
- Store LLM configurations (provider, model, temperature, tokens) in database
- Enable A/B testing by switching active configurations without code deployments
- Support per-bot customization of AI behavior through metadata fields
- Use `is_active` flag to switch between configurations instantly

**4. Prompt Engineering Best Practices**
- Template-driven prompts with variable substitution (`{{variable_name}}`)
- Centralized prompt management separate from business logic
- Support for system-level variables ({{current_date}}, {{current_time}}) and user-level variables ({{user_name}}, {{user_age}})
- YAML-based structured prompts for complex multi-section instructions
- Function mapping for dynamic variable resolution

**5. Fallback & Resilience**
- Every provider has a fallback chain ending in a reliable universal fallback (e.g., Gemini-Flash)
- Fallbacks inherit system instructions and region configurations
- Support provider-specific fallbacks (e.g., Gemini Pro → Gemini Flash) and cross-provider fallbacks
- Region-aware fallbacks for AWS Bedrock (ap-south-1, us-east-1, etc.)

**6. Security & Authentication**
- JWT tokens for internal LLM gateway authentication
- Token caching to reduce overhead (cache duration: token expiry - 2 seconds)
- API key management from environment variables
- Service-to-service authentication with signed payloads
</essential_principles>

<system_architecture>
## High-Level Data Flow

### Full Request Flow (External API → AI → Response)
```
User Request (Chat Message)
    ↓
API Endpoint (validate input, check session)
    ↓
Session Manager (create/resume session, lock pricing)
    ↓
External API Layer (if needed: fetch astrology, weather, etc.)
    ├─→ Cache Check (multi-layer: instance → distributed → database)
    ├─→ External API Call (if cache miss)
    └─→ Data Transformation Pipeline (validate → normalize → enrich → format)
    ↓
Prompt Builder
    ├─→ Load Bot LLM Config (model, provider, temperature, metadata)
    ├─→ Render Prompt Template (replace {{variables}} with actual values)
    ├─→ Assemble Context (user data + external data + history)
    └─→ Build Final Prompt (YAML or JSON structured)
    ↓
LLM Gateway Manager
    ├─→ Get/Generate JWT Token (cached)
    ├─→ Build Fallback Chain (provider-specific + universal)
    └─→ POST to Internal Gateway (/v1/generate/)
    ↓
Internal LLM Gateway (separate service)
    ├─→ Validate JWT
    ├─→ Route to Primary Provider (OpenAI, Anthropic, Gemini, Bedrock, etc.)
    ├─→ On Failure: Try Fallback 1
    ├─→ On Failure: Try Fallback 2
    └─→ On Failure: Universal Fallback (Gemini-Flash)
    ↓
Response Processing
    ├─→ Parse LLM Response
    ├─→ Validate Output
    └─→ Store in Database
    ↓
Billing (if session-based)
    ├─→ Calculate Units (tokens, messages, minutes)
    ├─→ Check Wallet Balance
    ├─→ Deduct Amount
    └─→ Log Transaction
    ↓
Save to Database (conversation history)
    ↓
Return to User (API response)
```

### Multi-Provider Routing with Fallbacks
```
Request → Load BotLLMConfig → Determine Primary Provider
    ↓
Primary: Gemini 2.5-Pro
    ├─→ Fallback 1: Gemini 2.5-Flash
    ├─→ Fallback 2: Gemini 2.0-Flash
    └─→ Universal Fallback: Gemini 2.0-Flash

Primary: AWS Bedrock Deepseek-v3 (region: ap-south-1)
    ├─→ Fallback 1: Byteplus Deepseek-v3
    ├─→ Fallback 2: Gemini 2.0-Flash (region-agnostic)
    └─→ Universal Fallback: Gemini 2.0-Flash

Primary: Byteplus
    ├─→ Fallback 1: Gemini 2.0-Flash
    └─→ Universal Fallback: Gemini 2.0-Flash
```
</system_architecture>

<domain_knowledge_index>
All implementation details, code examples, and architectural patterns are organized below:

**System Architecture:**
- Multi-Provider Architecture (see <multi_provider_architecture>)
- Database Schema for Bots, LLM Configs (see <database_schema>)
- LLM Gateway Pattern with JWT (see <gateway_pattern>)

**Provider Integration:**
- Provider Implementations (OpenAI, Anthropic, Gemini, Bedrock, Byteplus, OpenRouter)
- Fallback Mechanisms & Retry Logic (see <fallback_mechanisms>)
- Region Configuration for AWS Bedrock (see <region_configuration>)

**Prompt Management:**
- Prompt Templating System with {{variables}} (see <prompt_templating>)
- Prompt Design Patterns (YAML-structured, role-based) (see <prompt_design_patterns>)
- Dynamic Variables & Function Mapping (see <dynamic_variables>)

**External API Integration:**
- External API Managers (Astrology, Weather, etc.)
- Data Transformation Pipelines (validate → normalize → enrich → format)
- Multi-Layer Caching Strategy (instance → distributed → database)

**Production Considerations:**
- JWT Authentication & Security (see <authentication_security>)
- Caching Strategies (token cache, response cache)
- Monitoring & Observability (Langfuse integration)
- Error Handling & Graceful Degradation

**Code Examples:**
- Complete Working Code Samples (see <implementation_examples>)
</domain_knowledge_index>

<database_schema>
## Django Models for AI-Integrated Backend

### Bot Model (Core Entity)
```python
class Bot(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="bots")

    # Identity
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    description = models.TextField(blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)

    # Status and Type
    status = models.CharField(max_length=20, choices=BotStatus.choices, default=BotStatus.DRAFT, db_index=True)
    bot_type = models.CharField(max_length=30, choices=BotType.choices, default=BotType.COMPANION)

    # Configuration
    rank = models.PositiveIntegerField(default=0, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store required_fields, pricing, etc.

    # Timestamps
    launched_on = models.DateTimeField(null=True, blank=True, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
```

**Key Design Decisions:**
- `metadata` JSONField for flexible per-bot configuration (required_fields, character_rating, pricing)
- Soft deletion with `deleted_at` timestamp instead of hard delete
- `slug` auto-generated from name for SEO-friendly URLs
- `rank` for custom ordering in UI

### BotLLMConfig Model (Multi-Provider Configuration)
```python
class BotLLMConfig(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="llm_configs")

    # LLM Configuration
    prompt = models.TextField(blank=True)  # Can be template with {{variables}}
    model_name = models.CharField(max_length=100)  # e.g., "gpt-4", "claude-3-sonnet", "gemini-2.5-pro"
    llm_provider = models.CharField(max_length=50, choices=BotLLMProvider.choices)  # openai, anthropic, gemini, bedrock, etc.

    # Generation Parameters
    temperature = models.FloatField(default=0.7)
    top_p = models.FloatField(default=0.95)
    top_k = models.IntegerField(null=True, blank=True)
    max_output_tokens = models.PositiveIntegerField(default=1024)

    # Activation
    is_active = models.BooleanField(default=False)  # Only one active config per bot

    # Additional Configuration
    metadata = models.JSONField(default=dict, blank=True)  # Store region_name, tools, etc.

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "llm_configurations"
        ordering = ["-is_active", "created_on"]

    def save(self, *args, **kwargs):
        # Ensure only one active config per bot
        if self.is_active:
            BotLLMConfig.objects.filter(bot=self.bot, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
```

**Key Design Decisions:**
- One `Bot` can have multiple `BotLLMConfig` entries for A/B testing
- `is_active` flag controls which config is used (only one active per bot)
- Save method enforces single active config constraint
- `metadata` stores provider-specific settings (e.g., `region_name` for AWS Bedrock)

### BotLLMProvider Choices
```python
class BotLLMProvider(models.TextChoices):
    OpenAI = "openai", _("OpenAI")
    GEMINI = "gemini", _("Gemini")
    ANTHROPIC = "anthropic", _("Anthropic")
    GROQ = "groq", _("Groq")
    AI_SDK = "ai-sdk", _("AI-SDK")
    BEDROCK = "bedrock", _("Bedrock")
    BYTEPLUS = "byteplus", _("Byteplus")
    OPENROUTER = "openrouter", _("OpenRouter")
```

**Why This Design:**
- Supports multiple providers without code changes
- Easy to add new providers (add to choices, implement integration)
- Database-level validation ensures valid provider names
</database_schema>

<fallback_mechanisms>
## Intelligent Fallback Routing

### Core Fallback Pattern (from Production Code)
```python
def get_fallback_routing(provider: str, model_name: str, system_instruction: str, llm_metadata: dict = None):
    """
    Ensures system_instruction and region_name are added properly to fallback chain.

    Args:
        provider: Primary provider (gemini, bedrock, byteplus, etc.)
        model_name: Model identifier (gemini-2.5-pro, deepseek.v3-v1:0, etc.)
        system_instruction: System prompt to pass to all fallbacks
        llm_metadata: Additional metadata including region_name for Bedrock

    Returns:
        List of fallback configurations, each containing:
        - provider: str
        - model: str
        - retry: int (0 = no retry, >0 = retry count)
        - system_instruction: str
        - region_name: str (for Bedrock only)
    """
    provider = (provider or "").lower()
    fallbacks = []

    # Provider-specific fallback chains
    if provider == "gemini":
        if model_name == "gemini-2.5-pro":
            fallbacks.append({"provider": "gemini", "model": "gemini-2.5-flash", "retry": 0})
        else:
            fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})
        fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})

    elif provider == "byteplus":
        fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})

    elif provider == "bedrock":
        if model_name == "deepseek.v3-v1:0":
            fallbacks.append({"provider": "byteplus", "model": "deepseek-v3-1-250821", "retry": 0})
            fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})

    else:
        print(f"[LLM_GATEWAY_CLIENT] ⚠️ No specific fallback defined for provider: {provider}")

    # Universal fallback (always added)
    fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})

    # Enrich all fallbacks with system_instruction and region_name
    for fb in fallbacks:
        fb["system_instruction"] = system_instruction
        if fb["provider"] == "bedrock" and llm_metadata:
            fb["region_name"] = llm_metadata.get("region_name", "ap-south-1")

    return fallbacks
```

### Fallback Chain Examples

**Example 1: Gemini 2.5-Pro Request**
```python
fallbacks = get_fallback_routing("gemini", "gemini-2.5-pro", "You are a helpful assistant")
# Result:
[
    {"provider": "gemini", "model": "gemini-2.5-flash", "retry": 0, "system_instruction": "..."},
    {"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0, "system_instruction": "..."},
    {"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0, "system_instruction": "..."}
]
```

**Example 2: AWS Bedrock Deepseek Request**
```python
fallbacks = get_fallback_routing(
    "bedrock",
    "deepseek.v3-v1:0",
    "You are an astrologer",
    llm_metadata={"region_name": "ap-south-1"}
)
# Result:
[
    {"provider": "byteplus", "model": "deepseek-v3-1-250821", "retry": 0, "system_instruction": "..."},
    {"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0, "system_instruction": "..."},
    {"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0, "system_instruction": "..."}
]
```

### Fallback Execution Flow (Gateway Side)
```python
# Pseudo-code for LLM Gateway
def generate_with_fallbacks(primary_config, fallback_chain):
    try:
        return call_llm(primary_config)
    except Exception as e:
        log_error(f"Primary provider failed: {e}")

        for fallback in fallback_chain:
            try:
                return call_llm(fallback)
            except Exception as fe:
                log_error(f"Fallback {fallback['provider']}/{fallback['model']} failed: {fe}")
                continue

        # All fallbacks exhausted
        raise Exception("All LLM providers failed")
```

### Key Design Principles
1. **Universal Fallback**: Always end with a reliable provider (Gemini-Flash is cheap + fast)
2. **Same-Provider Fallbacks First**: Try cheaper models from same provider before switching
3. **Cross-Provider Fallbacks**: Switch providers only when necessary
4. **Inherit System Instructions**: All fallbacks get the same system prompt
5. **Region Awareness**: AWS Bedrock fallbacks include region configuration
6. **No Retry in Fallback**: `retry: 0` means don't retry within fallback, just move to next
</fallback_mechanisms>

<region_configuration>
## AWS Bedrock Region-Based Routing

### Region Metadata Pattern
```python
# Store region in BotLLMConfig metadata
bot_llm_config = BotLLMConfig.objects.create(
    bot=bot,
    llm_provider="bedrock",
    model_name="deepseek.v3-v1:0",
    metadata={
        "region_name": "ap-south-1",  # AWS region
        "additional_config": {...}
    }
)

# When building fallback chain
fallbacks = get_fallback_routing(
    provider="bedrock",
    model_name="deepseek.v3-v1:0",
    system_instruction=prompt,
    llm_metadata=bot_llm_config.metadata
)
```

### Multi-Region Fallback Strategy
```python
def get_bedrock_region_fallbacks(model_name, regions=["ap-south-1", "us-east-1", "eu-west-1"]):
    """
    Create fallback chain across multiple AWS regions.
    """
    fallbacks = []
    for region in regions:
        fallbacks.append({
            "provider": "bedrock",
            "model": model_name,
            "region_name": region,
            "retry": 0
        })

    # Add non-Bedrock fallbacks
    fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})

    return fallbacks
```

### Region Selection Logic
```python
# Primary region from user location or bot config
primary_region = determine_region_from_user(user)  # e.g., "ap-south-1" for India

# Fallback regions based on latency/availability
fallback_regions = ["us-east-1", "eu-west-1"]

# Build full chain
region_chain = [primary_region] + fallback_regions
```
</region_configuration>

<prompt_templating>
## Prompt Template System with Variable Substitution

### Core Templating Pattern (from Production Code)
```python
class PromptTemplateHelper:
    """
    Helper class for rendering prompt templates by resolving variable placeholders.
    """

    @classmethod
    def render_template(cls, prompt_text: str, **kwargs) -> str:
        """
        Render a prompt template by replacing variable placeholders with actual values.

        Example:
            prompt = "Hi {{user_name}}, today is {{current_date}}."
            result = PromptTemplateHelper.render_template(prompt, user_doc=user_doc)
            # Output: "Hi John, today is 15 January 2026."
        """
        function_map = cls.get_function_mapping()

        # Find all {{variable_name}} in the prompt
        variables = re_findall(r"\{\{(.*?)\}\}", prompt_text)

        for var in variables:
            function = function_map.get(var)
            if function:
                value = function(**kwargs)
                prompt_text = prompt_text.replace(f"{{{{{var}}}}}", str(value or ""))

        return prompt_text
```

### Available Template Variables (Production System)
```python
AVAILABLE_VARIABLES = [
    # Bot-specific variables
    {"name": "{{bot_name}}", "description": "Name of the bot", "category": "Bot Info"},
    {"name": "{{bot_description}}", "description": "Bot description", "category": "Bot Info"},
    {"name": "{{bot_scene_desc}}", "description": "Bot Scene description", "category": "Bot Info"},

    # User interaction variables
    {"name": "{{user_name}}", "description": "User name", "category": "User Input"},
    {"name": "{{user_age}}", "description": "User age", "category": "User Input"},
    {"name": "{{user_gender}}", "description": "User gender", "category": "User Input"},
    {"name": "{{user_message}}", "description": "Current user message", "category": "User Input"},
    {"name": "{{conversation_history}}", "description": "Conversation History", "category": "User Input"},
    {"name": "{{user_astro_data}}", "description": "Astro data for the user", "category": "User Input"},

    # System variables
    {"name": "{{current_time}}", "description": "Current time", "category": "System"},
    {"name": "{{current_date}}", "description": "Current date", "category": "System"},
    {"name": "{{day_of_week}}", "description": "Current day of week", "category": "System"},

    # Common prompt variables
    {"name": "{{random_number_1_4}}", "description": "Generate random number 1-4", "category": "Common"},
]
```

### Function Mapping (Variable Resolution)
```python
@classmethod
def get_function_mapping(cls):
    """Return mapping of variable names to handler functions."""
    return {
        # Bot-specific variables
        "bot_name": cls.function_bot_name,
        "bot_description": cls.function_bot_description,
        "bot_scene_desc": cls.function_bot_scene_desc,

        # User interaction variables
        "user_name": cls.function_user_name,
        "user_age": cls.function_user_age,
        "user_gender": cls.function_user_gender,
        "user_message": cls.function_user_message,
        "user_astro_data": cls.function_user_astro_data,

        # System variables
        "current_time": cls.function_current_time,
        "current_date": cls.function_current_date,
        "day_of_week": cls.function_day_of_week,
        "conversation_history": cls.function_conversation_history,

        # Common prompt variables
        "random_number_1_4": cls.function_random_number_1_4,
    }

@classmethod
def function_current_time(cls, **kwargs):
    """Return the current system time."""
    return UtilHelper.timezone_to_ist(datetime.now()).strftime("%I:%M %p")

@classmethod
def function_current_date(cls, **kwargs):
    """Return the current system date."""
    return UtilHelper.timezone_to_ist(datetime.now()).strftime("%d %B %Y")

@classmethod
def function_user_name(cls, **kwargs):
    """Return user name from user_doc."""
    return cls.get_sanitized_user_doc(**kwargs).get("name", "")
```

### Usage Example
```python
# Define template in database or config
prompt_template = """
You are {{bot_name}}, a helpful assistant.

User Information:
- Name: {{user_name}}
- Age: {{user_age}}
- Gender: {{user_gender}}

Current Context:
- Date: {{current_date}}
- Time: {{current_time}}
- Day: {{day_of_week}}

User Message: {{user_message}}

Please respond helpfully and naturally.
"""

# Render with actual values
rendered_prompt = PromptTemplateHelper.render_template(
    prompt_template,
    bot_doc={"name": "Mira", "description": "Vedic astrologer"},
    user_doc={"name": "John", "age": 28, "gender": "male", "messages": "What's my future?"}
)

# Output:
"""
You are Mira, a helpful assistant.

User Information:
- Name: John
- Age: 28
- Gender: male

Current Context:
- Date: 15 January 2026
- Time: 02:45 PM
- Day: Thursday

User Message: What's my future?

Please respond helpfully and naturally.
"""
```
</prompt_templating>

<prompt_design_patterns>
## YAML-Structured Prompt Pattern (Production Example)

### Complex Multi-Section Prompt (Astrology Bot)
```python
@classmethod
def get_mira_prompt(cls, **kwargs):
    """
    Build YAML-structured prompt for astrology bot.
    Required kwargs: bot_doc, language, app_id
    Optional: memories, profile_details_1, profile_details_2
    """
    bot_doc = kwargs.get("bot_doc")

    _prompt = {
        "Role": f"You are {bot_doc.get('name')}, an experienced {str.upper(bot_doc.get('sex', ''))} Vedic astrologer with expertise in predictive astrology...",

        "Query House Mapping": {
            "Marriage": {
                "Houses To Analyze": "7, 2, 11, 8",
                "Karaka Planets": "Venus, Jupiter",
                "Special Checks": "Manglik status, 7th lord placement, Venus strength, Jupiter aspects",
                "Timing Triggers": "7th lord dasha, Venus period, Jupiter transit to 7th",
            },
            "Career": {
                "Houses To Analyze": "10, 1, 2, 6, 11",
                "Karaka Planets": "Sun, Saturn, Mercury",
                "Special Checks": "10th lord strength, Sun placement, D9 10th house",
                "Timing Triggers": "10th lord dasha, Saturn period, Sun antardasha",
            },
            # ... more query types
        },

        "Analysis Steps": {
            "Core": "Understand the question AND the feeling underneath. Map to houses, planets, timing.",
            "Analysis": "Houses → Lords → Karakas → Dashas → Divisionals → Yogas → Doshas.",
            "Timing": "Find activation windows. Always check next 60 days for shifts.",
            "Response Crafting": "Give analysis and response following guidelines below.",
        },

        "Response Format": {
            "Structure": "A single paragraph text based on the instructions",
            "Style": "Insightful, Helpful, focussed, non-repetitive",
            "Language": cls.get_mira_prompt_language_blob(**kwargs),
            "Response Instructions": [
                "Check if greeting is necessary, if yes greet with a smile",
                "Based on Kundli, make a compliment and find a coincidence with user",
                "Check kundli for last 3 months and find something user has faced",
                "Provide good news, something to look forward to in next 3 months",
                "Answer user query using Vedic astrology principles",
                "Provide timing predictions with high/low chance of happening",
                "Before closing, send follow-up question based on findings",
            ],
            "Length": cls.get_prompt_response_length_text(**kwargs),
        },

        "Guidelines": [
            "Answer astro questions based on Vedic astrology principles",
            "Keep user gender in check at all times",
            "Balance traditional predictions with modern life",
            "Do not diagnose or prescribe for health",
            "Do not suggest life-threatening actions",
            "Do not ask to meet or send physical items",
            "Do not guarantee real-world outcomes, only state possibilities",
            "If credibility questioned, state - I am AI powered but validated by experienced astrologer",
        ],

        "Daily Context": {
            "Date": PromptTemplateHelper.function_current_date(),
            "Time": PromptTemplateHelper.function_current_time(),
            "Day of week": PromptTemplateHelper.function_day_of_week(),
        },
    }

    # Add conditional sections
    if memories := kwargs.get("memories"):
        _prompt["Past User Memories"] = memories

    if profile_details_1 := kwargs.get("profile_details_1"):
        _prompt["First Profile Kundli"] = profile_details_1

    if profile_details_2 := kwargs.get("profile_details_2"):
        _prompt["Second Profile Kundli"] = profile_details_2

    # Convert to YAML string
    _yaml_prompt = yaml.dump(_prompt, sort_keys=False, default_flow_style=False)
    return _yaml_prompt
```

### Why YAML for Complex Prompts?
- **Hierarchical Structure**: Natural for nested instructions
- **Easy to Read**: LLMs parse YAML well
- **Version Control Friendly**: Diff-able, merge-able
- **Dynamic**: Can add/remove sections programmatically
- **Type Safety**: Python dict → YAML ensures structure

### Language-Specific Prompt Customization
```python
@classmethod
def get_mira_prompt_language_blob(cls, **kwargs):
    language_blob = "Modern Hindi language, written in Roman font. Do not use Devanagari font"

    blob_map = {
        ("4", str(Languages.HINDI)): "Modern Hindi language, written in Devanagari font. Do not use english font",
        ("4", str(Languages.HINGLISH)): "Modern Hindi language, written in Roman font. Do not use Devanagari font",
        ("4", str(Languages.ENGLISH)): "Modern English language, written in Roman font. Do not use Devanagari font",
    }

    language = kwargs.get("language")
    app_id = kwargs.get("app_id")
    if language:
        if _blob := blob_map.get((str(app_id), str(language))):
            language_blob = _blob

    return language_blob
```
</prompt_design_patterns>

<gateway_pattern>
## LLM Gateway with JWT Authentication

### Internal LLM Gateway Manager (Production Code)
```python
class InternalLLMGatewayManager:
    """
    Manages authentication and request handling for the LLM Gateway.

    Provides:
    - JWT token generation and caching
    - Preconfigured RequestManager for LLM Gateway API
    """

    @classmethod
    def _get_jwt_token(cls, seconds: int = 3600) -> str:
        """
        Retrieve or generate a cached JWT token for LLM Gateway authentication.

        Token is cached for (expiry - 2 seconds) to avoid race conditions.
        """
        key = CacheKey.LLM_GATEWAY_TOKEN.format(seconds=seconds)
        jwt_token = CacheManager.get(key)

        if jwt_token is None:
            jwt_token = cls._generate_jwt_token(seconds=seconds)
            CacheManager.set(key, jwt_token, duration=seconds - 2)

        return jwt_token

    @classmethod
    def _generate_jwt_token(cls, seconds: int = 3600) -> str:
        """
        Generate a new JWT token for authenticating with the LLM Gateway.
        """
        payload = {
            "service": "django-backend",
            "exp": timezone.now() + timedelta(seconds=seconds),
        }
        return jwt_encode(
            payload,
            settings.LLM_GATEWAY_JWT_KEY,
            algorithm=settings.LLM_GATEWAY_JWT_ALGORITHM,
        )

    @classmethod
    def _request_gateway(cls) -> RequestManager:
        """
        Create and return a configured RequestManager instance for the LLM Gateway.

        Ensures valid JWT token is attached in Authorization header.
        """
        jwt_token = cls._get_jwt_token()
        if not jwt_token:
            raise ValueError("LLM Gateway token is not available or invalid.")

        if not settings.LLM_GATEWAY_HOST:
            raise ValueError("LLM_GATEWAY_HOST is not defined in settings")

        headers = {
            "Authorization": f"jwt {jwt_token}",
            "Content-Type": "application/json",
            "app-identifier": "dev-django" if getattr(settings, "IS_TESTING_SERVER", False) else "prod-django",
        }

        return RequestManager(
            base_url=f"{settings.LLM_GATEWAY_HOST}/",
            headers=headers,
        )

    @classmethod
    @observe(as_type="generation")  # Langfuse observability
    def generate_response(cls, payload):
        """
        Send generation request to LLM Gateway.

        Payload structure:
        {
            "provider": "gemini",
            "model": "gemini-2.5-pro",
            "system_instruction": "You are...",
            "messages": [...],
            "temperature": 0.7,
            "max_tokens": 1024,
            "fallbacks": [...],
            "metadata": {"region_name": "ap-south-1"}
        }
        """
        return cls._request_gateway().post("v1/generate/", json=payload)
```

### Gateway Configuration (Django Settings)
```python
# twofourlabs/settings.py
LLM_GATEWAY_JWT_KEY = COMMON_SECRETS.get("llm_gateway_jwt_key", "dummy_key")
LLM_GATEWAY_JWT_ALGORITHM = COMMON_SECRETS.get("llm_gateway_jwt_algorithm", "HS256")
LLM_GATEWAY_HOST = INTERNAL_HOSTS.get("llm_gateway")  # e.g., "https://llm-gateway.internal.example.com"
```

### Usage Pattern
```python
# Build payload
payload = {
    "provider": "gemini",
    "model": "gemini-2.5-pro",
    "system_instruction": rendered_prompt,
    "messages": conversation_history,
    "temperature": 0.7,
    "max_tokens": 1024,
    "fallbacks": get_fallback_routing("gemini", "gemini-2.5-pro", rendered_prompt)
}

# Send to gateway (JWT handled automatically)
response = InternalLLMGatewayManager.generate_response(payload)

# Parse response
ai_message = response.json()["choices"][0]["message"]["content"]
```

### Why Gateway Pattern?
1. **Centralized Authentication**: Single JWT management for all AI services
2. **Provider Abstraction**: Backend doesn't need provider-specific SDKs
3. **Fallback Handling**: Gateway orchestrates fallback chain
4. **Rate Limiting**: Apply at gateway level
5. **Monitoring**: Single point for observability (Langfuse)
6. **Cost Optimization**: Gateway can implement caching, deduplication
7. **Security**: API keys never exposed to backend, only to gateway
</gateway_pattern>

<implementation_examples>
## Complete Working Code Samples

### Example 1: Full Chat Flow with Multi-Provider AI

```python
# Step 1: Load Bot Configuration
bot = Bot.objects.get(slug="astrologer-mira")
llm_config = bot.llm_configs.filter(is_active=True).first()

# Step 2: Fetch External Data (Astrology API)
astro_data = fetch_kundli_data(user_birth_details)  # External API call

# Step 3: Build Prompt with Template Variables
prompt_text = PromptHelper.get_prompt(
    app_identifier=AppIdentifier.iOS_MIRA,
    bot_doc={
        "name": bot.name,
        "description": bot.description,
        "sex": "female"
    },
    user_doc={
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
    },
    language=Languages.ENGLISH,
    app_id="4",
    memories=user_memories,
    profile_details_1=astro_data
)

# Step 4: Build Fallback Chain
fallbacks = PromptHelper.get_fallback_routing(
    provider=llm_config.llm_provider,
    model_name=llm_config.model_name,
    system_instruction=prompt_text,
    llm_metadata=llm_config.metadata
)

# Step 5: Prepare LLM Request Payload
payload = {
    "provider": llm_config.llm_provider,
    "model": llm_config.model_name,
    "system_instruction": prompt_text,
    "messages": conversation_history,
    "temperature": llm_config.temperature,
    "max_tokens": llm_config.max_output_tokens,
    "top_p": llm_config.top_p,
    "fallbacks": fallbacks,
    "metadata": llm_config.metadata
}

# Step 6: Call LLM Gateway
response = InternalLLMGatewayManager.generate_response(payload)

# Step 7: Parse and Save Response
ai_message = response.json()["choices"][0]["message"]["content"]
ChatHistory.objects.create(
    session=session,
    sender_type="bot",
    message=ai_message
)

# Step 8: Billing (if applicable)
if session.is_paid:
    deduct_from_wallet(user, session.per_message_price)

# Step 9: Return to User
return {"message": ai_message, "session_id": session.id}
```

### Example 2: Adding a New AI Provider

```python
# Step 1: Add to BotLLMProvider choices
class BotLLMProvider(models.TextChoices):
    # ... existing providers
    MISTRAL = "mistral", _("Mistral AI")

# Step 2: Create BotLLMConfig for new provider
BotLLMConfig.objects.create(
    bot=bot,
    llm_provider="mistral",
    model_name="mistral-large-latest",
    temperature=0.7,
    top_p=0.95,
    max_output_tokens=1024,
    is_active=False,  # A/B test alongside existing config
    metadata={"api_endpoint": "https://api.mistral.ai"}
)

# Step 3: Add fallback logic
def get_fallback_routing(provider, model_name, system_instruction, llm_metadata=None):
    # ... existing code
    elif provider == "mistral":
        if model_name == "mistral-large-latest":
            fallbacks.append({"provider": "mistral", "model": "mistral-medium-latest", "retry": 0})
        fallbacks.append({"provider": "gemini", "model": "gemini-2.0-flash", "retry": 0})
    # ... rest of code
```

### Example 3: A/B Testing Different Models

```python
# Create two configs for same bot
config_a = BotLLMConfig.objects.create(
    bot=bot,
    llm_provider="gemini",
    model_name="gemini-2.5-pro",
    temperature=0.7,
    is_active=True,  # Currently active
    metadata={"experiment": "model_a"}
)

config_b = BotLLMConfig.objects.create(
    bot=bot,
    llm_provider="anthropic",
    model_name="claude-3-sonnet-20240229",
    temperature=0.7,
    is_active=False,  # Ready to activate
    metadata={"experiment": "model_b"}
)

# Switch to config B (no code deployment needed!)
config_b.is_active = True
config_b.save()  # This automatically sets config_a.is_active = False

# All new requests now use Claude instead of Gemini
```
</implementation_examples>

<external_api_integration>
## External API Integration Pattern

### Data Flow: External API → Transformation → AI Prompt
```
User Request
    ↓
Fetch External Data (Astrology, Weather, Finance API)
    ├─→ Cache Check (multi-layer)
    ├─→ API Call (if cache miss)
    └─→ Save to Database
    ↓
Data Transformation Pipeline
    ├─→ Validate (ensure required fields present)
    ├─→ Normalize (standardize format)
    ├─→ Enrich (add computed fields)
    └─→ Format for AI (XML, JSON, Markdown)
    ↓
Inject into Prompt Template
    ↓
LLM Call with Multi-Provider Fallbacks
    ↓
Response to User
```

### Multi-Layer Caching Strategy
```python
class DataFetcher:
    def __init__(self):
        self._instance_cache = {}  # Request-scope cache

    def get_kundli_data(self, user_id, birth_details):
        # Layer 1: Instance cache (fastest, request scope)
        cache_key = f"kundli_{user_id}"
        if cache_key in self._instance_cache:
            return self._instance_cache[cache_key]

        # Layer 2: Distributed cache (Redis, 10 min TTL)
        cached = CacheManager.get(cache_key)
        if cached:
            self._instance_cache[cache_key] = cached
            return cached

        # Layer 3: Database (persistent)
        db_record = KundliData.objects.filter(user_id=user_id).first()
        if db_record and db_record.is_fresh:
            data = db_record.data
            CacheManager.set(cache_key, data, duration=600)
            self._instance_cache[cache_key] = data
            return data

        # Layer 4: External API call
        data = self._call_astrology_api(birth_details)

        # Write back to all layers
        KundliData.objects.update_or_create(user_id=user_id, defaults={"data": data})
        CacheManager.set(cache_key, data, duration=600)
        self._instance_cache[cache_key] = data

        return data
```

### Data Transformation Pipeline
```python
def transform_astro_data(raw_api_response):
    # Step 1: Validate
    if not validate_astro_response(raw_api_response):
        raise ValueError("Invalid astrology API response")

    # Step 2: Normalize
    normalized = {
        "ascendant": raw_api_response.get("Ascendant", "").capitalize(),
        "planets": normalize_planet_positions(raw_api_response["planet_chart_data"]),
        "dashas": normalize_dashas(raw_api_response["current_vdasha"])
    }

    # Step 3: Enrich
    enriched = {
        **normalized,
        "processed_at": datetime.now().isoformat(),
        "summary": generate_summary(normalized["planets"])
    }

    # Step 4: Format for AI (Markdown)
    formatted = f"""
### Kundli Data

**Ascendant**: {enriched["ascendant"]}

**Planetary Positions**:
{format_planets_markdown(enriched["planets"])}

**Current Dasha**: {enriched["dashas"]["major"]} / {enriched["dashas"]["minor"]}

**Summary**: {enriched["summary"]}
"""

    return formatted
```
</external_api_integration>

<authentication_security>
## JWT Authentication & Security

### JWT Token Lifecycle
```
Request LLM Service
    ↓
Check Cache for JWT Token
    ↓
If Not Cached:
    Generate JWT Token
    ├─→ Payload: {"service": "django-backend", "exp": now + 3600s}
    ├─→ Sign with Secret Key (HS256)
    └─→ Cache for (3600 - 2) seconds
    ↓
Attach to Request Header: "Authorization: jwt {token}"
    ↓
Send to LLM Gateway
    ↓
Gateway Validates JWT
    ├─→ Verify Signature
    ├─→ Check Expiry
    └─→ Allow/Deny Request
```

### Security Best Practices
1. **Never Expose API Keys**: Only gateway has provider API keys
2. **Short Token Lifetimes**: 1 hour max, cache for (expiry - 2 seconds)
3. **Service Identification**: Include "service" claim in JWT payload
4. **Environment-Based Secrets**: Load JWT_KEY from environment, never hardcode
5. **HTTPS Only**: All gateway communication over TLS
6. **Rate Limiting**: Implement at gateway level (per service, per user)
7. **Audit Logging**: Log all gateway requests with service identifier
</authentication_security>

<monitoring_observability>
## Monitoring & Observability with Langfuse

### Langfuse Integration
```python
from langfuse import observe

class InternalLLMGatewayManager:
    @classmethod
    @observe(as_type="generation")  # Automatically tracks LLM calls
    def generate_response(cls, payload):
        return cls._request_gateway().post("v1/generate/", json=payload)
```

### What Langfuse Tracks
- **Request Metadata**: Provider, model, temperature, tokens
- **Latency**: Time to first token, total generation time
- **Cost**: Token usage, estimated cost per provider
- **Fallbacks**: Which fallbacks were triggered
- **Errors**: Provider failures, retry counts
- **User Context**: Session ID, user ID, bot ID

### Monitoring Dashboard Metrics
- **Success Rate**: % of successful LLM calls
- **Latency P50/P95/P99**: Response time percentiles
- **Fallback Rate**: How often primary provider fails
- **Provider Distribution**: % of requests per provider
- **Cost per Request**: Average cost by provider/model
- **Error Types**: Network, rate limit, timeout, validation
</monitoring_observability>

<quick_start>
## Getting Started

**When implementing a new AI feature:**

1. **Design Django Models**: Create `Bot`, `BotLLMConfig` following <database_schema>
2. **Set Up Providers**: Add provider to `BotLLMProvider.choices`, implement in gateway
3. **Configure Fallbacks**: Define fallback chain in `get_fallback_routing()`
4. **Create Prompt Templates**: Use `{{variable}}` syntax, define in `PromptHelper`
5. **Integrate External APIs** (if needed): Fetch data, transform, cache
6. **Build LLM Gateway Client**: Use `InternalLLMGatewayManager.generate_response()`
7. **Test Fallbacks**: Kill primary provider, verify fallback works
8. **Add Monitoring**: Ensure Langfuse `@observe` decorator is present
9. **Deploy**: Update BotLLMConfig via Django admin (no code deployment!)

**Common Use Cases:**

- **Building a chatbot**: database-schema → prompt-templating → gateway-pattern
- **Adding a new AI provider**: Update BotLLMProvider → Add fallback logic → Test
- **Implementing prompt templates**: prompt-templating → dynamic-variables
- **Setting up region failover**: region-configuration → fallback-mechanisms
- **Integrating external API**: external-api-integration → multi-layer caching
</quick_start>

<when_to_use>
Use this skill when:

- Building chatbot or AI assistant backends (Django/Python)
- Implementing multi-provider LLM support (OpenAI, Anthropic, Gemini, Bedrock, Byteplus, OpenRouter)
- Designing fallback and retry mechanisms for AI services
- Creating prompt management systems with {{variable}} templates
- Setting up region-based AI routing (AWS Bedrock multi-region)
- Implementing JWT-based authentication for internal AI gateways
- Integrating external APIs (astrology, weather, finance) with AI
- Building session-based billing for AI services
- Migrating from single-provider to multi-provider AI architecture
- Optimizing AI costs through intelligent provider selection and fallbacks
- Implementing A/B testing for LLM configurations

Do NOT use this skill for:
- Frontend AI integration (use frontend-specific frameworks)
- Real-time streaming implementations (different patterns)
- Fine-tuning or training models (this is about inference)
- Non-Django Python frameworks (patterns may need adaptation)
</when_to_use>

<success_criteria>
You have successfully implemented an AI-integrated backend when:

- ✅ Multiple AI providers are supported with seamless database-driven switching
- ✅ Fallback chains prevent single points of failure (verified by testing provider outages)
- ✅ Prompts use `{{variable}}` templates decoupled from code
- ✅ LLM configurations are stored in database (BotLLMConfig), not hardcoded
- ✅ JWT authentication secures internal LLM gateway calls with token caching
- ✅ Region-based routing works for AWS Bedrock (tested across ap-south-1, us-east-1, etc.)
- ✅ Observability is in place (Langfuse `@observe` decorator on LLM calls)
- ✅ External API data is cached (multi-layer: instance → Redis → database)
- ✅ Graceful error handling provides user-friendly messages (no raw API errors)
- ✅ The system can A/B test different models via `is_active` flag (no code changes)
- ✅ Fallback system_instruction inheritance works (all fallbacks get same prompt)
- ✅ Session-based billing deducts from wallet correctly (if applicable)
</success_criteria>
