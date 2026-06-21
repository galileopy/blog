---
layout: post
title: "How I Don’t (Really) Do Vibe-Coding"
date: 2025-05-05 00:58:00 +0000
slug: how-i-dont-do-vibe-coding
lang: en
permalink: /how-i-dont-do-vibe-coding/
excerpt: "Using LLMs to Spec First, Slice Work, and Let the Code Write Itself"
original_status: published
---

When I first tried vibe-coding, I was drawn in by the promise of rapid progress—it felt exhilarating to see features come together quickly with minimal effort. I was determined to make this approach work consistently and deliver reliable results.

But as a colleague aptly put it, vibe-coding makes you feel like you're making fast progress, only to disrupt something else, forcing you to start over. You then make more progress, slightly better than before, but inevitably encounter another issue. I soon discovered this sentiment wasn’t unique to me—colleagues shared similar frustrations, and I found numerous mentions online echoing the same cycle of excitement and setbacks.

I experienced this firsthand: each burst of progress was followed by unexpected bugs or oversights, forcing me to backtrack and start over. That’s when I decided to rethink my approach, leading to the structured workflow I now rely on.

Everyone’s talking about vibe-coding these days, so I figured I’d share how I’m doing it — with the caveat that I don’t.

Vibe-coding, as coined by Andrej Karpathy, is a hands-off coding approach where developers use AI tools like LLMs to intuitively guide development through voice commands and minimal direct interaction with the code, often accepting AI suggestions without reviewing changes ([Karpathy’s post](<https://x.com/karpathy/status/1886192184808149383?lang=en>)).

What I am experimenting with instead, is to use LLMs to help write solid specs first. I try to make them detailed enough that they surface every key interaction, edge case, and data dependency before I even touch a line of code.

Once that's in place, I'll prepare "context slices", which are standalone units containing tasks, user flows, API specs, and UI components that anyone can easily pick up and work on. You could drop these into a ticket in project management tools like Jira or Linear and use them to kick off focused, efficient “mini vibe-coding” sessions.

Pete Hodgson’s [Chain-Of-Vibes](<https://blog.thepete.net/blog/2025/04/14/chain-of-vibes/>) excellently covers how to run mini vibe-coding sessions. Here, I’ll focus on how I ensure my upfront documentation is thorough before coding begins.

* * *

I follow a structured workflow that I’ve refined over time, using existing LLMs to accelerate a traditional SDLC process focused on sequential phases like requirements gathering and design.

I started by following the steps in [Harper Reed's Blog](<https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm>), which work well for simple apps. However, they fail miserably for more ambitious projects.

I’ve learned that skipping the step of creating a prompt plan for a code assistant and instead focusing on developing thorough specs upfront is a better choice. I’m currently experimenting with this approach, prioritizing the spec stage to create these four documents:

## Comprehensive User Journey

This document, inspired by the [4 Part Series | Painless Functional Specifications](<https://www.joelonsoftware.com/2000/10/03/painless-functional-specifications-part-2-whats-a-spec/>), aims for precision by including page descriptions and, if needed, hand-drawn wireframes. It must cover edge cases and user-facing details that can influence the implementation—for example, what happens if the user closes the page and opens it in another browser. These details clarify whether user preferences should be stored locally to persist across sessions, fetched once on page load, or updated via a subscription feed if the user’s state changes.

## Back-end Systems Component

This section includes a document specifying the requirements and interfaces for back-end systems.

  * **Overview** : Lists the endpoints to be described later, with references to the user flow steps it supports.
  * **Dependencies** : Includes items like a queue, database, or other services. If the database schema will be altered, it’s listed here.
  * **Detailed Endpoint Descriptions** : Covers methods, status, and request/response details in API Blueprint format.
  * I used to include Mermaid sequence diagrams, but I’ve found they’re only useful for complex components. I’m still identifying the best scenarios to include them.



## A Contract

This document defines the schema of data passed between boundaries (e.g., front-end/backend or backend to third-party services). It’s crucial for understanding how user-facing components interact with external services.

## Front-end Components

This section is still evolving as I refine my approach. It currently consists of one document with:

  * **Overview** : Outlines the general context, such as frameworks and component libraries.
  * **Page Definitions** : Lists pages, their URLs, main purposes, navigation paths, and components used.
  * **Interactive Component Definitions** : Details inputs, outputs, side effects, and user interactions, with an optional list of nested components.
    * A component can have nested components; I try to avoid complex elements and am still experimenting with what works best.
    * I’m still evaluating whether to explicitly define how each component interacts with the state management framework.
  * **Presentation Elements** : Usually not needed unless none exist or the existing ones don’t meet requirements. This is more relevant for greenfield projects than existing ones. Tools like Claude Code or Cline, which are AI-based, can index your existing front-end components for easy reference in a repository during vibe-coding.
  * **Services or Contracts** : Specifies logic for storing or presenting data.
  * **Short Endpoint Descriptions** : Describes endpoints, their side effects, and their role in user flows.
    * For example: `POST /orders` creates a new order tied to the logged-in user, and `GET /orders` will include this order with its current status.
    * These details help when writing tests or drafting Jira tickets to clarify functionality and endpoint behavior.



* * *

Don’t move on from documentation until you’re confident in its completeness. Review and refine it multiple times, expecting significant changes early on and fewer as you progress. This process may involve hours of iteration, using an LLM for drafting and a colleague for feedback.

Read your document once, rest on it, and revisit it after a day or a few hours. If you’re not tempted to make changes or clarifications, that’s usually the only real indication it’s ready. I’ve learned this the hard way—shipping incomplete documentation often leads to significant issues later, as these details are critical to the project’s success.

Next, I create a unit of work, or ‘context slice,’ by extracting details from each document—contract, endpoint specifications, front-end components—and incorporating the user flow. Then, I code that unit in a focused, intuitive way. While this builds on the spirit of vibe-coding, the extensive upfront documentation makes it a more structured process than Karpathy’s hands-off approach.

With all this context ready, implementing features feels seamless, even if you focus on perfecting the documentation. I’ve had tremendous success using these slices for Jira tickets that I can hand off to a coworker, encouraging them to adopt the same documentation-first approach to ensure thorough specs before coding.

While I’m still exploring how to optimize this approach for different scenarios, I’m excited to continue refining it as I tackle larger, collaborative projects. I’d love to hear how others are incorporating AI tools into their development workflows—feel free to share your experiences!

## Notes

I’m exploring adding data-flow descriptions to the contract document to define component input and output types and catch gaps. This could involve TypeScript function signatures, with an LLM verifying that each transformation step includes required fields, such as user IDs or timestamps, by checking for their presence and type compatibility. This idea is inspired by [The Hikikomori’s Guide to JavaScript](<https://web.archive.org/web/20231230183921/https://robotlolita.me/old-posts/2013-04-27-the-hikikomoris-guide-to-javascript.html>), which emphasizes designing an API first to guide development.
