---
layout: post
title: "How to properly tell LLMs to nest code blocks?"
date: 2025-07-14 16:03:41 +0000
slug: lpt-how-to-properly-tell-llms-to-nest-code-blocks
lang: en
permalink: /lpt-how-to-properly-tell-llms-to-nest-code-blocks/
tags:
  - llm
  - ai
  - grok
excerpt: "How to properly render nested codblock in the chat box for easy copy pasting"
original_status: published
---

One of the things that I like to tell Grok when producing output is to wrap its output in code fences or code blocks.

This is incredibly convenient when producing markdown content that I'd like to copy independently from the whole response, because the chat interface provides a copy button in the top right corner as seen in the picture.

![]({{ '/assets/images/lpt-how-to-properly-tell-llms-to-nest-code-blocks/image-1.png' | relative_url }})

However, there is a small problem when the expected result is markdown that will, in turn, have nested code. The nested code fences close the outer fence early, and it breaks the way the whole message renders.

In some cases, this will not be an issue, because I could tell it to output in chat only the desired output without any meta-commentary, and use the copy chat response button.

However, this is not ideal. I have a prompt maker project that helps me improve existing prompts, and when I use it, I actually expect it to tell me how it improved the prompt and to provide the result in an easy-to-copy code box, as depicted above.

I tried this several times in all kinds of prompts, even instructing Grok to use `<code><pre></pre></code>`.

One of my most recent attempts included this:
    
    
    When generating code or markdown output, wrap the outermost code block in `<code><pre></pre></code>` HTML tags to clearly denote the start and end of the code section and ensure proper formatting. For markdown content within these tags, use standard triple backtick code fences (` ``` `) to encapsulate any nested code blocks, ensuring proper rendering of inner code snippets. Indent nested code blocks with 4 spaces to enhance readability and maintain consistent formatting. For example:
    
    <code><pre>
    ```markdown
    # Example Markdown
    Notice how the outer layer makes use of four backtick code fences. And that it starts with the HTML tags.
    This is a markdown section with a nested code block:
        ```python
        def example():
            print("Hello, World!")
        ```
    ```
    </pre></code>
    
    Ensure the number of backticks for nested code fences is sufficient to avoid conflicts, using three backticks (`) for inner blocks unless additional backticks are required for further nesting. Verify that all code fences are properly closed and that the output is valid markdown.
    

That produced this:

![]({{ '/assets/images/lpt-how-to-properly-tell-llms-to-nest-code-blocks/image.png' | relative_url }})

When copied, though, it will actually have the expected content:
    
    
    # Markdown with Nested Markdown and Python Code
    
    This is a markdown document with nested markdown and a Python code block.
    
    ## Nested Markdown Example
    
    Here is a nested markdown section:
        ```markdown
        ### Inner Markdown
        This is an *inner* markdown block with **formatting**.
    
        - Item 1
        - Item 2
    
        Below is a Python code block within the inner markdown:
            ```python
            def greet(name):
                return f"Hello, {name}!"
            
            print(greet("World"))
            ```
        ```
    
    ## Another Section
    
    This section demonstrates that the outer markdown continues correctly.
    

But for my purposes, this does not work. I want to be able to read in chat before copy-pasting.

### Here is what "kind of" works

I added a critical section to the project instructions, emphasizing the importance of these rules. That got Grok to use the correct number of backticks (`) to nest code blocks properly.
    
    
    ## CRITICAL 
    
    For nested code blocks, ensure the outer code block uses more backticks than the deepest inner code block. For example:
    
    - Use four backticks (````) for an outer block containing inner blocks with three backticks (```).
    - Use five backticks (`````) for an outer block containing inner blocks with four backticks (````), and so on. 
    - Check the prompt for multiple levels of nesting and adjust the number of backticks accordingly.
    
    This is important! If you don't do this, then your reply will be useless.
    

And that, kind of works, I can at least copy the outer block now

![]({{ '/assets/images/lpt-how-to-properly-tell-llms-to-nest-code-blocks/image-2.png' | relative_url }})
