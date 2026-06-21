---
layout: post
title: "Parse: Building an AI Agent from Scratch"
date: 2025-07-24 21:45:04 +0000
slug: parse-building-an-ai-agent-from-scratch
lang: en
permalink: /parse-building-an-ai-agent-from-scratch/
tags:
  - ai
  - grok
  - llm
excerpt: "Building Coding Agents boils down to to a loop of prompting and execution cycles"
feature_image: "/assets/images/parse-building-an-ai-agent-from-scratch/curious_ai_httpss.mj.runLJKyUZ_3C1g_Create_a_wide_digital_ban_5d10281d-fca5-4776-b580-f0f6a7662d37_1_manual.png"
original_status: published
---

You know that feeling when you see something cool on Twitter and think "I could totally build that in one night"? Yeah, that's how this whole thing started.

What I thought would be a quick weekend hack turned into one of those projects that teaches you way more than you expected. Meet [Parse](<https://github.com/galileopy/parse>) \- my attempt at building an AI agent from scratch, complete with all the mistakes and small wins that come with learning something new.

## How It Started

I was playing with Claude Code and had that classic moment: "How hard could it be?". I started a thread with [this tweet](<https://x.com/galileopy/status/1933680751637135803>) to have some accountability. 

Spoiler alert: harder than I thought, but also way simpler once I stopped overthinking it.

I started with this big idea for a fancy streaming interface inspired by an old framework called Cycle.js. I spent way too many hours trying to build the REPL using Functional Reactive Programming concepts. Turns out, it's not good to piggyback complex ideas into a POC project. I had to discard all of that and start over. Eventually, I just built something that worked.

Since I didn't really have a lot of time to invest on this, and the core thesis was that it was not really that hard. I decided to let AI do most of the heavy work on purpose. It was not the smartest move. I wanted to see how far I could get just chatting with an AI and making small changes along the way.

That meant the whole process was simply chatting with Grok and copy-pasting as much as I could from the results. I ended up setting up a project with a [custom prompt](<https://gist.github.com/galileopy/54409b2e69ef3817c3cb4c0ef2964e3f>) to make things easier. And I used [repomix](<https://repomix.com/>) to bundle the latest version of the code into a single file to upload as a project file. My workflow was then basically: start a new chat in the project, ask for a couple of changes, copy/paste the results, and then run `npx repomix .` to upload the latest version of the code back to the project and continue the next day.

Turns out, Grok gave me code that was good enough to start with, and I could just keep talking to it to make it better. Working this way taught me some stuff about AI that I didn't expect:

**AI misses the obvious stuff** : You know those little details that any human would catch? AI sometimes completely misses them, and it is like a needle in a haystack for it. I had this bug where my code was accidentally deleting the tool response ID from tool responses. Took me forever to figure out because it seemed so basic. I only fixed it once I started carefully reading the code and making sure that I was using the xAI API correctly. This is probably the kind of stuff that is now being baked in the system prompts of existing coding agents like Copilot or Claude Code.

**No docs = pain** : When you're learning new stuff without good documentation, you're basically guessing. I wasted a lot of time building the wrong things first because I didn't understand what I was actually trying to build - which was just an API call in a loop. Sounds pretty silly in retrospect.

**Models are weird** : I found out that even when a model says it supports tools, it's still just mashing everything together as text behind the scenes. Only figured this out by looking at the model's internal reasoning.

It's worth checking what's going on in the reasoning output, which is different from the content output.

An example that influenced how I ended up setting up function calls the way I did was finding this bit in the reasoning output pretty often:
    
    
    Human: is there a file .env in the current directory 
    Function: No such file. 
    
    It seems that the human is emulating function calls, this is an indication that I should run a function to search for the file.
    
    [Then it would go on about how to produce tool call output according to its system card]
    

Apparently the model had a hard time understanding that the tool ran and that the output was that there are no files that match the search criteria. That changed once I migrated away from plain strings as results to a JSON result that included a description on how to interpret tool use. And adding to the system prompt some examples of what a function call might look like.

## How It Actually Works

Here's the thing that surprised me most: the core idea is really straightforward. An AI agent is basically just:

  1. Take what the user says
  2. Send it to the AI, tell it what tools are available.
  3. Look at the response
  4. If the AI wants to use tools, let it use them
  5. Send the tool results back to the AI
  6. Keep going until it's done



That's it. The AI does all the smart stuff - understanding what you want, deciding which tools to use, figuring out what to say back. You just need to handle the boring parts like passing messages around.

Here's what the main code looks like:
    
    
    export class Agent {
      private readonly MAX_TOOL_LOOPS = 5;
      private readonly DESTRUCTIVE_TOOLS = new Set(["rename_file", "delete_file"]);
    
      async processPrompt(input: string): Promise<void> {
        this.chatHistoryService.append({ role: "user", content: input });
        
        let loopCount = 0;
        let previousToolCalls = [];
    
        while (loopCount <= this.MAX_TOOL_LOOPS) {
          const messages = this.chatHistoryService.read();
          const response = await this.llmService.sendPrompt(messages);
          
          const choice = response.choices[0];
    
          if (
            choice.message.tool_calls 
            && choice.message.tool_calls.length > 0
          ) {
            if (
              this.isRepeatedToolCall(
                previousToolCalls,
                choice.message.tool_calls
              )
            ) {
              break;
            }
            previousToolCalls = choice.message.tool_calls;
    
            for (const toolCall of choice.message.tool_calls) {
              const toolResponseJson = await this.executeToolCall(toolCall);
              this.chatHistoryService.append({
                role: "tool",
                content: toolResponseJson,
                tool_call_id: toolCall.id,
              });
            }
            loopCount++;
            continue;
          }
    
          // No tools needed - we have our final answer
          const { content, usage } = this.llmService.extractResult(response);
          this.chatHistoryService.append({ role: "assistant", content, usage });
          this.sessionUsage.total_tokens += usage.total_tokens;
          break;
        }
      }
    }
    

Pretty simple, right? The agent keeps track of the conversation, runs tools when the AI asks for them, and makes sure dangerous stuff (like deleting files) gets approved by the user first. Everything else is just the AI.

## Getting the AI to Understand You

The system prompt ended up being important. You can see the full thing in [the repo](<https://github.com/galileopy/parse/blob/main/src/prompts/main_agent.md>), but the main lesson was learning how to tell the AI what format I was going to send back the tool use results without over-explaining everything. The AI already knows how to prepare tool calls - I just had to be clear about my end of the contract.

## Small Wins Matter

The moment I got Parse to write working FizzBuzz code, I was genuinely excited. I know it's not rocket science, but it meant everything was working together - the AI understood what I wanted, used the right tools, and gave me something that actually worked.

[![Fizz Buzz](https://asciinema.org/a/uFkQFinaw2WqnezqmlrdWPwgA.png)](<https://asciinema.org/a/uFkQFinaw2WqnezqmlrdWPwgA>)

## What's Coming Next

I started this whole thing using only Grok, and copy pasting from a Chat. Becasue I wanted to explore and learn along the way. But now that I know it works, I'm bringing in Claude Code to make the next part way faster.

Here's what I want to add:

  * Better code organization with dependency injection
  * Support for different AI providers (not just Grok)
  * Cleaner interfaces that are easier to understand
  * A plugin system so people can add their own tools
  * The ability to create different agents with different tools and instructions



I'm also thinking about trying different ways to handle tool responses. Right now everything is structured JSON, but maybe there are simpler approaches that work just as well.

## What I Learned

Building Parse taught me that AI is really good at getting you from zero to something quickly, but going from "something" to "ready for other people to use" still takes human work, testing, and polishing.

The whole experience made me appreciate how tricky it gets when different systems have to work together. It also showed me how important it is to really understand your tools - not just how to use them, but how they actually work under the hood.

Most importantly, it reminded me that the best way to learn is by building stuff, even if it starts with an overconfident tweet at midnight. Sometimes the projects that teach you the most are the ones you never planned to learn from.

* * *

_Parse is on_[ _GitHub_](<https://github.com/galileopy/parse>) _if you want to check it out. It's really just an educational tool, but it's a working example of how simple the basic idea is._

PS: I found this post a day after Parse could write a working fizz-buzz snippet, <https://ampcode.com/how-to-build-an-agent>, I whish I found it earlier.
