# TalkFlow

※ Still under development, so it might not work perfectly yet.

---

## Overview

TalkFlow visualizes the "topics" within conversations or text as a graph network, making the flow of discussion instantly clear.

### Possible Use Cases
- Joining a livestream midway and not understanding the conversation flow — use TalkFlow to catch up.
- Meetings where topics keep shifting — use TalkFlow to organize and track discussions.
- Reading a novel but forgot what happened earlier — use TalkFlow to recall previous topics.

---

## Example

![Textbox Example](textbox.png)
- You can input conversation text via the textbox and submit it.
- Voice input is planned for future support.

![Graph Example](graph.png)
- Submitting multiple messages will generate and update the graph.
- The example shown is based on the fairy tale *The Restaurant of Many Orders*.
- The upper section of the graph clearly shows the story flow:
  - Two young gentlemen follow various "etiquette" steps like washing their shoes and hair.
  - They gradually remove their gear, including their guns and clothing.

---

## Tech Stack

- Python  
- Docker  
- AWS  
  - (Amazon Transcribe)  
- Gemini API

---

## Getting Started

```shell
pip install -r requirements.txt
```
```shell
flask --app app run
```
