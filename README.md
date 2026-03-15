Mr. Clarke's Office

It is a hackathon project that simulates an AI-powered defense system designed to detect threats and automatically generate intelligence briefings. The system combines document intelligence, computer vision surveillance, and voice-triggered emergency detection into one integrated platform.

The project consists of three main modules:

Mr. Clarke's Automated Briefing Generator

Demo Watch – Demogorgon Surveillance System

Code Red – Emergency Voice Detection System

1. Mr. Clarke's Automated Briefing Generator
Description

An AI-powered engine that ingests a folder containing PDF or text documents and automatically generates a structured and animated presentation.

Unlike simple chat-based systems, this module builds a full presentation pipeline including document processing, retrieval, slide outlining, and automated slide creation.

Key Features

PDF and text document ingestion

Intelligent document chunking

Vector embeddings and semantic search

Retrieval-Augmented Generation (RAG)

Automatic slide outline generation

Bullet point summarization

PPTX or Reveal.js presentation output

Workflow

Documents Folder

→ Document Loader

→ Text Chunking

→ Embedding Generation

→ Vector Database Storage

→ Semantic Retrieval

→ LLM Slide Outline Generation

→ Slide Deck Creation

Technologies

Python

LangChain / RAG pipeline

Vector database (FAISS / Chroma)

LLM (Mistral / Ollama)

python-pptx or Reveal.js

2. Demo Watch – Demogorgon Surveillance System
Description

A computer vision surveillance module that monitors camera feeds and detects potential threats in real time.

The system uses a lightweight vision-language model to analyze frames from video feeds and trigger alarms when a threat is detected.

Key Features

Real-time video monitoring

Frame-by-frame analysis

Vision-language model inference

Automatic alarm triggering

Workflow

Camera Feed

→ Frame Capture

→ smolvlm500m Vision Model

→ Object Detection

→ Threat Detected

→ Alarm Trigger

Technologies

Python

OpenCV

smolvlm500m Vision Model

Alarm module

3. Code Red – Emergency Voice Detection
Description

An always-listening audio monitoring system that detects emergency trigger phrases.

The system uses speech recognition to continuously process microphone input and activate alarms when specific keywords are detected.

Key Features

Real-time microphone monitoring

Speech-to-text transcription

Keyword detection

Emergency alert triggering

Workflow

Microphone Input

→ Audio Stream Processing

→ Whisper Speech-to-Text

→ Keyword Detection ("Code Red")

→ Alarm Trigger

Technologies

Python

OpenAI Whisper

PyAudio / sounddevice

System Architecture

The three modules operate independently but form a unified AI defense system:

Document Intelligence generates automated briefings

Vision Surveillance monitors threats

Voice Detection triggers emergency alerts


## 👥 Team

- Karan kumar Nayak
- @Mohi-ni 
