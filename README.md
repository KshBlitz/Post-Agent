# 📘 Project Document

## Project Name: Daily AI-Powered Cyber News Content Engine

---

# 1️⃣ Problem Statement

Professionals consume cybersecurity newsletters daily to stay updated. However:

* The process is manual.
* News must be read individually.
* Relevant articles must be identified.
* Content must be reformulated manually for LinkedIn.
* Time is wasted filtering and rewriting.

The core problem:

> How can we automatically ingest daily cybersecurity news, intelligently rank it, allow human selection, and generate ready-to-post LinkedIn content — without manual research or repetitive prompting?

Constraints:

* Must run locally.
* Must not require paid APIs.
* Must not require 24/7 uptime.
* Must not overload laptop resources.
* Must be modular, testable, and stable.

---

# 2️⃣ Proposed Solution

We design a **modular, two-engine AI workflow** that:

1. Fetches cybersecurity news once per day.
2. Uses a local LLM (Ollama) to rank and summarize.
3. Notifies the user via Telegram.
4. Waits for user selection.
5. Fetches full article content.
6. Generates LinkedIn-ready content.
7. Cleans up temporary data.
8. Resets for next cycle.

Key architectural principle:

> AI is a processing engine — not the orchestrator.

Python handles orchestration.
Ollama handles reasoning and generation.

---

# 3️⃣ System Architecture Overview

High-level architecture:

```
[Trigger]
    ↓
Engine 1 (Daily Fetch + Ranking)
    ↓
Telegram Notification
    ↓
User Selection
    ↓
Engine 2 (Content Generation)
    ↓
Telegram Delivery
    ↓
Cleanup + State Update
```

The system is:

* Scheduled
* Stateless across days
* Temporarily stateful within a cycle
* Modular

---

# 4️⃣ Workflow Description

---

## 🔵 Engine 1 – Daily Fetch & Ranking

### Trigger Mechanism

* Manual run OR
* Windows Task Scheduler
* Date-based execution validation via `last_run.json`

### Execution Steps

1. Validate execution date
2. Fetch RSS feed from:
   `https://feeds.feedburner.com/TheHackersNews`
3. Parse structured XML via `feedparser`
4. Filter articles from last 24 hours
5. Extract:

   * Title
   * Link
   * Published Date
   * RSS Summary
6. Send summaries to Ollama model
7. Prompt model to:

   * Rank relevance
   * Provide short summary
   * Return structured JSON
8. Save ranked results to:
   `data/today_feed.json`
9. Send Telegram message containing:

   * Top 3 articles
   * Summaries
   * Selection instruction
10. Exit

---

## 🔵 Engine 2 – Article Expansion & Content Generation

### Trigger

* Manual script execution after user replies

### Execution Steps

1. Fetch latest Telegram reply
2. Parse selection number
3. Load selected article metadata from `today_feed.json`
4. Download full article HTML
5. Extract readable article body via BeautifulSoup
6. Send full article text to Ollama
7. Prompt model to:

   * Generate LinkedIn content
   * Follow predefined tone template
8. Send generated post to Telegram
9. Delete:

   * `today_feed.json`
10. Update:

* `last_run.json`

11. Exit

---

# 5️⃣ Dataflow Design

---

## 🟢 Dataflow – Engine 1

```
RSS XML
   ↓
feedparser
   ↓
Python List (RAM)
   ↓
Filtered Articles
   ↓
Ollama Inference
   ↓
Ranked JSON Output
   ↓
today_feed.json
   ↓
Telegram Message
```

---

## 🟢 Dataflow – Engine 2

```
Telegram Reply
   ↓
Load today_feed.json
   ↓
Selected Article Link
   ↓
requests.get()
   ↓
HTML
   ↓
BeautifulSoup Clean Text
   ↓
Ollama Inference
   ↓
Generated LinkedIn Post
   ↓
Telegram Delivery
   ↓
File Cleanup
```

---

# 6️⃣ In-Depth Logical Segmentation

---

## 📦 Module 1: RSS Fetcher

Responsibilities:

* Connect to RSS endpoint
* Parse XML
* Extract structured entries
* Filter by date

Independent of:

* LLM
* Telegram
* Storage

Failure here does not impact downstream logic beyond halting execution.

---

## 📦 Module 2: Ranking Engine (LLM Interaction Layer)

Responsibilities:

* Construct ranking prompt
* Send request to Ollama
* Parse JSON response
* Validate output structure

Key logic:

* Strict JSON enforcement
* Temperature control
* Output sanitation

Completely independent of:

* Telegram
* File deletion
* Scheduling

---

## 📦 Module 3: Communication Unit (Telegram Interface)

Responsibilities:

* Send formatted message
* Retrieve replies
* Parse user selection

No business logic.
No AI reasoning.
Pure transport layer.

---

## 📦 Module 4: Article Extraction Engine

Responsibilities:

* Fetch article HTML
* Extract readable text
* Remove navigation clutter
* Normalize whitespace

Isolated from:

* RSS logic
* Telegram logic
* Ranking logic

---

## 📦 Module 5: Content Generator (LLM Layer 2)

Responsibilities:

* Construct LinkedIn-specific prompt
* Apply style template
* Generate final post
* Validate tone and structure

Independent from:

* RSS parsing
* Telegram retrieval

---

## 📦 Module 6: State Manager

Responsibilities:

* Manage `last_run.json`
* Manage `today_feed.json`
* Handle file cleanup

Ensures:

* No duplicate runs
* No data persistence clutter
* Clean daily reset

---

# 7️⃣ Execution Strategy

---

## 🔹 Model Strategy

Model: `mistral:7b-instruct-q4` (Ollama)

Lifecycle:

* Model loads only during inference
* Unloads automatically after idle
* No 24/7 GPU strain

---

## 🔹 Scheduling Strategy

Option 1:

* Windows Task Scheduler (once per day)

Option 2:

* Manual trigger

Execution validation:

* Compare system date with `last_run.json`

No sleep loops.
No daemon processes.

---

## 🔹 Communication Strategy

* Telegram Bot API
* Polling mode
* No webhook
* No external server required

---

# 8️⃣ Failure Handling Strategy

Potential Failure Points:

| Layer          | Risk                  | Mitigation              |
| -------------- | --------------------- | ----------------------- |
| RSS Fetch      | Network failure       | Graceful exit           |
| LLM Ranking    | JSON malformed        | Retry once              |
| Telegram Send  | Network error         | Retry                   |
| Article Scrape | HTML structure change | Fallback to RSS summary |
| Duplicate Run  | Same day execution    | Date validation         |

---

# 9️⃣ Resource Efficiency

* No background processes
* No infinite loops
* No database overhead
* Model loads only during inference
* Minimal disk writes
* Temporary state only

Laptop remains safe.

---

# 🔟 Expected Outcome

After stabilization:

Daily workflow becomes:

* Wake laptop
* Run script
* Receive 3 curated cyber news summaries
* Select one
* Receive ready-to-post LinkedIn content
* Post within 60 seconds

No browsing.
No reading multiple sites.
No manual rewriting.

---

# 1️⃣1️⃣ System Characteristics

* Modular
* Deterministic
* Testable per module
* Low resource usage
* Stateless across days
* Semi-autonomous
* Human-in-the-loop controlled

---

# 1️⃣2️⃣ Long-Term Upgrade Potential

Future improvements (optional):

* Automatic posting to LinkedIn (risk-managed)
* Multi-source RSS ingestion
* Relevance tuning based on engagement
* Style memory per day
* Vector memory for historical posts
* Cloud migration
* Full automation mode

But none required for MVP.

---

# 1️⃣3️⃣ Final Architectural Summary

This is not:

* A chatbot
* An always-running AI agent
* An AutoGPT-style loop

This is:

> A deterministic, modular, scheduled AI workflow system with human oversight.

You are not building “AI hype.”

You are building:
A structured AI content production pipeline.

