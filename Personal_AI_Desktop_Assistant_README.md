# Personal AI Desktop Assistant

> A local-first, general-purpose AI assistant that runs on a user's
> computer, understands natural-language goals, uses authorized tools
> and services to accomplish those goals, maintains user-approved
> memory, and can perform multi-step and eventually proactive tasks.

**Project type:** Learning project / desktop application\
**Initial interface:** CLI\
**Deployment model:** Local-first, downloadable desktop application\
**Primary user:** One individual per installation\
**Status:** Project definition / architecture planning

------------------------------------------------------------------------

## 1. Project Vision

The goal is to build a personal AI assistant that lives on a user's
computer and can interact with the user's digital life.

The assistant should not merely answer questions. It should be able to:

-   understand what the user wants to accomplish
-   determine what information it needs
-   decide which tools it needs
-   execute tools
-   combine multiple tools into workflows
-   remember useful, user-approved information
-   perform actions with appropriate permissions
-   schedule work for later
-   eventually act proactively when useful

The assistant is intended to feel like a general-purpose personal agent
rather than a chatbot, productivity app, or developer copilot.

### Core principle

> **The user expresses what they want to accomplish; the agent
> determines how to accomplish it using the capabilities available to
> it.**

------------------------------------------------------------------------

# 2. Why This Project Exists

This is explicitly a **learning project**.

The objective is not to blindly assemble an AI application using
frameworks and APIs. Every major part of the system should be built to
understand the underlying concepts.

The project will be used to learn:

-   LLM APIs
-   prompting
-   structured outputs
-   tool/function calling
-   agent loops
-   planning
-   tool selection
-   tool chaining
-   state and context
-   memory
-   MCP
-   OAuth and external APIs
-   permissions
-   local computer interaction
-   scheduling
-   background jobs
-   notifications
-   security
-   desktop application architecture
-   packaging and distribution
-   reliability and failure handling

### Development philosophy

> **Understand → design → implement → experiment → break → fix.**

We should prefer understanding a small system completely over blindly
using a large framework.

Every major technology should have a reason for being introduced.

------------------------------------------------------------------------

# 3. Product Definition

The product is a **downloadable desktop application** that runs
primarily on the user's computer.

The core assistant runtime is local.

External services such as email, calendar, Spotify, and web search
remain external services and are accessed only after the user grants the
required permissions.

Conceptually:

``` text
                         USER
                           |
                           v
                  +------------------+
                  | Desktop Assistant|
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |   Agent Runtime  |
                  |                  |
                  | Planning         |
                  | Tool Selection   |
                  | Memory          |
                  | Permissions      |
                  | State            |
                  +--------+---------+
                           |
                     Tool / MCP Layer
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
     Local PC          External APIs        Web
        |                  |                  |
   Files/Terminal      Gmail/Calendar     Search/etc.
```

------------------------------------------------------------------------

# 4. Target User

The initial target is a single person using their own computer.

The assistant is designed for everyday personal use:

-   organizing information
-   managing time
-   handling digital tasks
-   researching things
-   interacting with personal services
-   working with files
-   remembering useful information
-   planning activities
-   automating repetitive tasks

It is **not initially designed for** teams, enterprises, organizations,
or multi-user environments.

------------------------------------------------------------------------

# 5. Interaction Model

## V1: CLI

The first interface is intentionally command-line based.

Example:

``` text
You > What's on my schedule tomorrow?

Assistant >
You have:
10:00 AM - College
2:00 PM  - Project meeting
7:00 PM  - Free
```

Another example:

``` text
You > Remind me to submit the assignment at 8 PM.

Assistant >
I'll remind you at 8:00 PM.
```

The CLI is deliberately simple so that UI development does not distract
from learning the underlying AI and agent architecture.

## Future Interfaces

Possible future interfaces include:

-   desktop GUI
-   system tray
-   global keyboard shortcut
-   voice
-   desktop notifications
-   mobile client

These are **not part of the initial implementation**.

------------------------------------------------------------------------

# 6. Capability Model

Capabilities are organized into domains.

The exact implementation can evolve, but the following represents the
intended product scope.

------------------------------------------------------------------------

## 6.1 Time and Scheduling

The assistant should eventually understand time as a first-class
capability.

### Capabilities

-   current time
-   current date
-   timezone conversion
-   time differences
-   date calculations
-   timers
-   alarms
-   reminders
-   recurring reminders
-   scheduled tasks
-   relative time expressions

### Examples

``` text
"What time is it in Tokyo?"

"Remind me in 40 minutes."

"Remind me every Sunday to plan my week."

"How long until 6 PM?"
```

------------------------------------------------------------------------

## 6.2 Calendar

The assistant can interact with one or more supported calendar services.

### Capabilities

-   read events
-   create events
-   modify events
-   delete events
-   recurring events
-   find free time
-   detect conflicts
-   summarize schedules
-   schedule reminders around events

### Examples

``` text
"What do I have tomorrow?"

"Find a two-hour free slot this week."

"Schedule a meeting with Rahul tomorrow at 4."

"Do I have anything conflicting with my appointment?"
```

------------------------------------------------------------------------

## 6.3 Email

The assistant can interact with a supported email service.

### Read / Search

-   search emails
-   read emails
-   search by sender
-   search by date
-   search by topic
-   summarize threads
-   find attachments

### Understand

-   identify important emails
-   identify action items
-   extract deadlines
-   extract dates
-   extract appointments
-   identify conversations requiring attention

### Actions

-   draft replies
-   save drafts
-   send emails with appropriate confirmation

### Examples

``` text
"Find all emails from college this month containing deadlines."

"Summarize my unread emails."

"Which emails need my attention?"

"Draft a reply to this email."
```

------------------------------------------------------------------------

## 6.4 Notes and Personal Knowledge

The assistant can maintain a personal notes system.

### Capabilities

-   create notes
-   read notes
-   search notes
-   update notes
-   delete notes
-   organize notes
-   summarize notes
-   maintain personal lists
-   maintain bookmarks
-   store user-approved information

### Examples

``` text
"Remember that I want to visit Japan."

"Save this idea."

"What travel ideas have I saved?"

"Find my notes about system design."
```

------------------------------------------------------------------------

## 6.5 Memory

Memory is separate from ordinary notes.

The assistant may maintain useful, user-approved long-term context such
as:

-   preferences
-   goals
-   routines
-   interests
-   important information
-   recurring patterns
-   relevant personal context

### Memory principles

-   The assistant should not treat everything it sees as permanent
    memory.
-   The user should be able to inspect important remembered information.
-   The user should be able to request that information be forgotten.
-   Sensitive information should receive additional consideration and
    protection.
-   Memory should be designed deliberately rather than implemented as
    "store every conversation in a vector database."

### Examples

``` text
"What do you remember about me?"

"Remember that I prefer afternoon meetings."

"Forget that preference."
```

------------------------------------------------------------------------

## 6.6 Files and Documents

The assistant can interact with files on the local computer.

### Capabilities

-   search files
-   read files
-   create files
-   edit files
-   rename files
-   move files
-   copy files
-   create folders
-   summarize documents
-   extract information
-   organize files

### Examples

``` text
"Find all PDFs related to my project."

"Summarize this document."

"Create a folder called Travel and move these files there."

"Find the PDF I downloaded last week."
```

File operations should be permission-aware, especially destructive
operations.

------------------------------------------------------------------------

## 6.7 Computer and System

The assistant can interact with the local computer.

### Potential capabilities

-   terminal commands
-   process information
-   system information
-   disk information
-   filesystem operations
-   clipboard
-   desktop notifications
-   installed application information
-   application launching

### Terminal

The assistant may eventually execute commands such as:

``` text
pwd
ls
git status
docker compose up
```

but command execution must go through a permission and safety layer.

The LLM should not receive unrestricted direct control of the machine.

------------------------------------------------------------------------

## 6.8 Web

The web provides external information.

### Capabilities

-   search
-   open pages
-   extract information
-   research topics
-   compare sources
-   summarize pages
-   find products
-   find events
-   find places
-   retrieve current information

### Examples

``` text
"Research good resources for learning distributed systems."

"Find interesting things happening this weekend."

"Compare these two products."

"Research this topic and give me a summary."
```

The assistant should distinguish retrieved facts from its own reasoning
and should preserve source information where appropriate.

------------------------------------------------------------------------

## 6.9 Entertainment

Entertainment should be treated as a broader capability rather than
simply "Spotify control."

Potential domains:

-   music
-   movies
-   TV shows
-   books
-   games

Potential capabilities:

-   maintain watch/read/listen lists
-   search entertainment
-   track what the user has consumed
-   provide recommendations
-   interact with supported media services

Spotify may provide music-related capabilities such as:

-   playback control
-   search
-   playlists
-   queue management
-   recommendations

The goal is not to make users type commands like "play a song" when the
native application already does that well.

The interesting use case is contextual assistance, for example:

``` text
"I have two hours tonight. What should I watch?"

"Find something from my watchlist that fits a two-hour window."

"I'm studying. Find something suitable to listen to."
```

------------------------------------------------------------------------

## 6.10 Tasks and Lists

The assistant can maintain lightweight task and list systems.

### Potential lists

-   tasks
-   shopping lists
-   reading lists
-   watch lists
-   ideas
-   custom lists

### Capabilities

-   create
-   update
-   complete
-   postpone
-   prioritize
-   assign deadlines
-   create recurring tasks
-   organize lists

Example:

``` text
"Add toothpaste and shampoo to my shopping list."

"What do I need to get done today?"

"Move this task to tomorrow."
```

------------------------------------------------------------------------

## 6.11 Research and Decision Support

The assistant can perform multi-step research.

Example:

``` text
User:
"I need a laptop under ₹80,000.
Research some options and explain the tradeoffs."

Agent:
Understand requirements
        |
        v
Search
        |
        v
Collect information
        |
        v
Compare
        |
        v
Analyze
        |
        v
Present findings
```

The assistant should inform the user rather than make consequential
decisions on the user's behalf.

------------------------------------------------------------------------

## 6.12 Planning

The assistant can convert goals into actionable plans.

Example:

``` text
"I want to learn Go in two months."

Goal
 |
 v
Break into milestones
 |
 v
Create tasks
 |
 v
Allocate time
 |
 v
Schedule work
 |
 v
Track progress
 |
 v
Adapt
```

The user remains in control of the plan.

------------------------------------------------------------------------

# 7. Cross-Capability Workflows

This is one of the central goals of the project.

The assistant should be able to combine multiple capabilities when a
user's request requires it.

### Example: Interview preparation

``` text
User:
"I have an interview next Friday. Get everything organized."

Email
  |
  v
Find interview details
  |
  v
Calendar
  |
  v
Create event
  |
  v
Notes
  |
  v
Create preparation notes
  |
  v
Tasks
  |
  v
Create preparation checklist
  |
  v
Reminders
  |
  v
Schedule reminders
```

### Example: Weekend planning

``` text
User:
"Plan something interesting for Saturday."

Calendar
  |
  v
Find free time
  |
  v
Web / Places
  |
  v
Find activities
  |
  v
Weather
  |
  v
Check conditions
  |
  v
Memory / Preferences
  |
  v
Present suitable options
```

### Important principle

Individual tools are not the primary value.

**The agent's ability to combine tools to accomplish a goal is a primary
value of the system.**

------------------------------------------------------------------------

# 8. Proactive Behavior

The assistant should eventually be capable of initiating useful
interactions.

Examples:

``` text
"Your meeting starts in 30 minutes."

"You have an unresolved task due today."

"You have an email that appears to require a response."

"You have a conflict between two calendar events."
```

This will require:

-   scheduling
-   background workers
-   event detection
-   notifications
-   persistent state

Proactive behavior will be added only after the core agent is reliable.

The assistant should avoid becoming noisy or annoying.

------------------------------------------------------------------------

# 9. Agent Architecture

The conceptual agent loop is:

``` text
User Request
     |
     v
Understand Goal
     |
     v
Determine Required Context
     |
     v
Plan / Select Tools
     |
     v
Execute Tool
     |
     v
Observe Result
     |
     +-------> Need another tool?
     |              |
     |             Yes
     |              |
     |              v
     |         Execute again
     |
     No
     |
     v
Produce Result
```

The agent should be capable of:

-   planning
-   tool selection
-   tool chaining
-   interpreting tool results
-   handling failures
-   retrying where appropriate
-   asking for clarification when necessary
-   asking for permission when necessary
-   completing multi-step goals

------------------------------------------------------------------------

# 10. Tool Architecture

Capabilities should be represented as tools.

Conceptually:

``` text
                    Agent
                      |
                  Tool Layer
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
   Calendar         Email          Files
       |              |              |
    Service         Service        Local PC
```

The agent should not need to know the internal implementation of a tool.

A tool should have:

-   a name
-   a description
-   a structured input schema
-   execution logic
-   structured output
-   error behavior
-   permission requirements

------------------------------------------------------------------------

# 11. MCP

MCP (Model Context Protocol) will be used as an important part of the
project's tool integration architecture.

The project will use MCP to learn and experiment with:

-   MCP clients
-   MCP servers
-   tools
-   resources
-   tool discovery
-   capability exposure
-   permissions
-   external integrations

Conceptually:

``` text
                    Agent
                      |
                  MCP / Tools
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
   Calendar         Email          Spotify
       |              |              |
    Google           Gmail        Spotify
```

Local capabilities can also be exposed through local tool/MCP servers:

``` text
              Local Tools / MCP
                    |
          +---------+---------+
          |         |         |
          v         v         v
       Files     Terminal   System
```

### Learning principle

MCP should not be treated as magic.

Before relying heavily on MCP, we should understand ordinary
tool/function calling and then understand the problem MCP is solving.

------------------------------------------------------------------------

# 12. Permissions and Safety

Permissions are a core part of the architecture.

The assistant must distinguish between:

### Read operations

Examples:

-   read calendar
-   search notes
-   read files
-   inspect system information

### Low-risk actions

Examples:

-   create a reminder
-   create a note
-   start a timer

### Consequential actions

Examples:

-   send email
-   delete files
-   modify important calendar events
-   execute potentially destructive commands

These should require appropriate confirmation.

Example:

``` text
Assistant:
I want to delete 14 files from Downloads.
Do you want me to proceed?

[Allow] [Deny]
```

The system should support permissions such as:

-   allow once
-   allow for this session
-   always allow for this tool
-   deny

The exact permission model will be designed and implemented as we learn
more.

------------------------------------------------------------------------

# 13. Security Principles

Because the assistant may eventually have access to personal information
and powerful local capabilities, security is a first-class concern.

Important principles:

-   least privilege
-   explicit permissions
-   secure credential storage
-   OAuth where appropriate
-   no hard-coded secrets
-   avoid unrestricted shell execution
-   validate tool arguments
-   distinguish read/write/destructive actions
-   log important actions
-   make consequential actions visible to the user
-   avoid unnecessary collection of personal data

The assistant should not silently perform high-impact actions.

------------------------------------------------------------------------

# 14. Local-First Architecture

The core application should run locally.

Conceptually:

``` text
User Computer
|
+-- Desktop Assistant
|    |
|    +-- CLI / UI
|    +-- Agent Runtime
|    +-- Tool Registry
|    +-- Memory
|    +-- Scheduler
|    +-- Permission System
|    +-- Local Tools
|    +-- MCP Client / Servers
|
+-- Local Data
|
+-- External Services
     |
     +-- Gmail
     +-- Calendar
     +-- Spotify
     +-- Web
     +-- Other integrations
```

The project does not initially require a public backend.

------------------------------------------------------------------------

# 15. Deployment

The long-term goal is a downloadable desktop application.

A user should eventually be able to:

1.  download the application
2.  install it
3.  configure an AI provider
4.  connect desired services
5.  grant permissions
6.  start using the assistant

The exact packaging technology is intentionally not decided yet.

------------------------------------------------------------------------

# 16. Model Strategy

The model provider should remain replaceable as much as practical.

Possible approaches include:

-   cloud LLM APIs
-   local models
-   hybrid local/cloud models

The initial implementation may use a cloud model for simplicity and
learning.

Local model support can be explored later.

The model itself is **not the entire assistant**.

The assistant consists of:

``` text
Model
+
Agent Runtime
+
Tools
+
Memory
+
State
+
Permissions
+
Scheduler
+
External Services
```

------------------------------------------------------------------------

# 17. State and Persistence

The assistant will eventually need persistent state for things such as:

-   conversations
-   tasks
-   reminders
-   notes
-   memories
-   tool configuration
-   permissions
-   scheduled jobs
-   user preferences

The exact database/storage technology will be chosen during architecture
design.

The choice should be driven by learning goals and actual requirements
rather than by popularity.

------------------------------------------------------------------------

# 18. Error Handling

Tools will fail.

The system should learn to distinguish:

``` text
Tool succeeded
Tool failed temporarily
Tool returned invalid data
Tool is unavailable
User denied permission
Authentication expired
User input is ambiguous
```

The agent should not hallucinate successful actions.

If a tool fails:

``` text
Bad:
"Done!"

Good:
"I couldn't create the calendar event because your calendar connection has expired."
```

Tool results should be treated as data, not blindly trusted.

------------------------------------------------------------------------

# 19. Observability

Since this is a learning project, understanding what the agent is doing
is important.

The development version should provide useful logs such as:

``` text
[AGENT] User request received
[AGENT] Selecting tools
[TOOL] calendar.list_events
[TOOL] Result received
[AGENT] Selecting tools
[TOOL] reminder.create
[TOOL] Success
[AGENT] Generating response
```

We should be able to inspect:

-   tool calls
-   tool arguments
-   tool results
-   errors
-   execution time
-   agent decisions
-   retries

The final user experience does not necessarily need to expose all of
this.

------------------------------------------------------------------------

# 20. What the Assistant Is NOT

The following are intentionally outside the initial product definition.

## Not a developer-specific assistant

It may have terminal access, but the target use case is general personal
assistance.

## Not simply a chatbot

Conversation is the interface; action is the purpose.

## Not an unrestricted autonomous agent

The user remains in control.

## Not a surveillance system

It should not secretly monitor everything happening on the computer.

## Not automatically omniscient

Access to files, email, calendar, etc. must be explicitly granted.

## Not a mobile application initially

Desktop first.

## Not a hosted SaaS initially

The core runtime is local.

## Not a multi-user system

One installation is initially intended for one user.

## Not an OS replacement

The assistant augments the operating system.

## Not an attempt to automate every possible task

Capabilities should be added when they are useful and when they provide
learning value.

------------------------------------------------------------------------

# 21. Explicit V1 Limitations

To prevent uncontrolled scope growth, V1 will NOT include:

-   mobile application
-   graphical UI
-   multi-user support
-   public API
-   cloud backend
-   distributed architecture
-   home automation
-   unrestricted computer control
-   autonomous financial transactions
-   autonomous communication without safeguards
-   fully autonomous background behavior
-   dozens of integrations from day one

These may be reconsidered later.

------------------------------------------------------------------------

# 22. Initial Capability Set

The eventual assistant may have many capabilities, but development
starts with a small set.

### Initial local capabilities

-   clock
-   notes
-   files
-   terminal

### Initial agent capabilities

-   natural-language conversation
-   tool calling
-   tool selection
-   basic multi-step execution
-   basic error handling

After the foundation works, capabilities can be added progressively:

``` text
Calendar
    |
Email
    |
Web
    |
Spotify / Entertainment
    |
Tasks
    |
Memory
    |
Notifications
    |
Scheduling
    |
More integrations
```

The order can change based on what we learn.

------------------------------------------------------------------------

# 23. Development Roadmap

## Phase 0 --- Understand

Learn the concepts before implementing the full system.

Topics:

-   LLMs
-   prompts
-   context
-   structured outputs
-   function/tool calling
-   agents
-   agent loops
-   MCP

------------------------------------------------------------------------

## Phase 1 --- Basic CLI Assistant

Build:

-   CLI
-   model interface
-   conversation loop
-   configuration
-   basic logging

Goal:

Understand the simplest possible LLM application.

------------------------------------------------------------------------

## Phase 2 --- Tool Calling

Create simple tools such as:

``` text
get_current_time()
create_note()
search_notes()
```

Learn:

-   tool schemas
-   structured arguments
-   tool execution
-   tool results
-   validation

------------------------------------------------------------------------

## Phase 3 --- Agent Loop

Move from:

``` text
User -> Tool -> Response
```

toward:

``` text
User
 |
 v
Agent
 |
 v
Choose tool
 |
 v
Execute
 |
 v
Observe
 |
 v
Choose next action
 |
 v
Finish
```

Learn:

-   planning
-   tool chaining
-   state
-   retries
-   termination

------------------------------------------------------------------------

## Phase 4 --- Persistence

Add:

-   conversations
-   notes
-   tasks
-   state
-   configuration

Learn:

-   persistence
-   data modeling
-   state management

------------------------------------------------------------------------

## Phase 5 --- MCP

Introduce MCP after understanding ordinary tool calling.

Learn:

-   MCP client
-   MCP server
-   tools
-   resources
-   discovery
-   integration patterns

------------------------------------------------------------------------

## Phase 6 --- Local Computer Capabilities

Add:

-   files
-   terminal
-   system information
-   notifications

Learn:

-   OS interaction
-   processes
-   security
-   permissions
-   local tool execution

------------------------------------------------------------------------

## Phase 7 --- External Services

Add integrations progressively:

1.  Calendar
2.  Email
3.  Web
4.  Entertainment / Spotify
5.  Other useful services

Learn:

-   OAuth
-   external APIs
-   token management
-   API failures
-   rate limits

------------------------------------------------------------------------

## Phase 8 --- Memory

Add:

-   long-term memory
-   user-approved memory
-   memory retrieval
-   memory updates
-   memory deletion

Learn:

-   memory architecture
-   structured vs semantic memory
-   retrieval
-   context management

------------------------------------------------------------------------

## Phase 9 --- Scheduling and Background Work

Add:

-   reminders
-   recurring tasks
-   scheduled jobs
-   background workers
-   notifications

Learn:

-   schedulers
-   event-driven systems
-   background execution
-   reliability

------------------------------------------------------------------------

## Phase 10 --- Reliability and Security

Improve:

-   permissions
-   authentication
-   secret management
-   validation
-   retries
-   error handling
-   logging
-   testing
-   failure recovery

------------------------------------------------------------------------

## Phase 11 --- Desktop Packaging

Only after the underlying system works:

-   package application
-   installer
-   configuration flow
-   service connections
-   application lifecycle
-   updates

------------------------------------------------------------------------

## Phase 12 --- Optional Future Interfaces

Only if the core assistant is valuable:

-   graphical UI
-   system tray
-   global shortcut
-   voice
-   mobile client

------------------------------------------------------------------------

# 24. Project Rules

These rules should guide development throughout the project.

### Rule 1 --- Learning comes first

If we use a framework, library, or abstraction, understand what problem
it solves.

### Rule 2 --- Build small things ourselves first

When practical, implement a minimal version before replacing it with a
framework.

### Rule 3 --- Avoid premature complexity

Do not introduce distributed systems, microservices, cloud
infrastructure, or unnecessary abstractions without a real need.

### Rule 4 --- Every feature needs a reason

A feature should provide meaningful utility, learning value, or both.

### Rule 5 --- Keep the agent general

Do not let the project become primarily a developer tool.

### Rule 6 --- Tools should be modular

Adding a new capability should not require rewriting the agent core.

### Rule 7 --- User control matters

The assistant should ask for permission before consequential actions.

### Rule 8 --- Never pretend an action succeeded

Tool results determine whether an action succeeded.

### Rule 9 --- Understand failures

When something breaks, investigate why rather than immediately replacing
it with another library.

### Rule 10 --- Scope is controlled deliberately

New ideas are welcome, but they go into a backlog rather than
automatically becoming part of the current milestone.

------------------------------------------------------------------------

# 25. Success Criteria

The project is successful if, over time, a user can naturally say things
like:

``` text
"What do I have tomorrow?"

"Find that email about the interview."

"Put it on my calendar."

"Remind me tomorrow morning."

"Find the document related to it."

"Summarize it."

"Research this topic."

"Remember this."

"Find everything I have about this."

"Plan my Saturday."

"Clean up my Downloads folder."

"Check whether I have enough free time this week."

"Prepare me for tomorrow's meeting."
```

and the assistant can determine the required steps, use the appropriate
tools, handle failures, ask for permissions when necessary, and explain
what it did.

------------------------------------------------------------------------

# 26. Long-Term Vision

The long-term goal is not to create the most feature-rich assistant
possible.

The goal is to create a **general-purpose personal agent platform** that
can continuously gain new capabilities without its core architecture
becoming fragile.

The desired relationship is:

``` text
                 USER
                   |
             "I want X"
                   |
                   v
                AGENT
                   |
        +----------+----------+
        |          |          |
        v          v          v
      Memory     Tools      Context
        |          |          |
        +----------+----------+
                   |
                   v
              PLAN / ACT
                   |
                   v
             USER RESULT
```

The assistant should increasingly become capable of answering:

> **"What are you trying to accomplish?"**

rather than merely:

> **"Which command would you like me to execute?"**

------------------------------------------------------------------------

# 27. Current Project Status

### Completed

-   Product concept defined
-   Local-first approach chosen
-   CLI-first development approach chosen
-   General-purpose scope defined
-   Initial capability domains defined
-   Agent/MCP direction established
-   Learning-first development philosophy established
-   Initial roadmap defined

### Current milestone

**Architecture and foundational learning**

### Next major task

Design the internal architecture of the assistant:

``` text
CLI
 |
Agent Runtime
 |
LLM Interface
 |
Tool Registry
 |
Tool Execution
 |
MCP
 |
State / Memory
 |
Permissions
 |
Scheduler
 |
Local + External Integrations
```

Before implementation, each component should be understood and
justified.

------------------------------------------------------------------------

# 28. Project North Star

> **Build a personal AI assistant that is genuinely useful because it
> can understand goals and act across the user's digital life---not
> because it has the largest number of integrations.**

And throughout the project:

> **Learn the system. Don't blindly build the system.**
