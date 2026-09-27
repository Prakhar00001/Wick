<div align="center">

# <span style="color:red">WICK</span>
**A LLM Evaluation Harness**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Type Checking](https://img.shields.io/badge/type__checking-strict-green.svg)](https://microsoft.github.io/pyright/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*“Evaluating LLMs shouldn't feel like a science fair project. Wick brings CI/CD rigor, bounded concurrency, and statistical confidence to AI evaluation.”*

</div>

---

## "Why":

Current LLM evaluation tools often fall into two traps: they are either notebook-centric toy scripts that fail under rate limits, or they are heavy, opinionated SaaS platforms that force you to rewrite your entire agent architecture to use them.

It is an infrastructure-first CLI evaluation harness designed to operate at scale. It acts as an uncompromising quality gate for single-prompt models, RAG pipelines, and multi-turn autonomous agents.

### Core Tenets
1. **Zero False Confidence:** Rigorous LLM-as-a-judge criteria, exact-match grounding, and statistical diffing.
2. **Bring Your Own Architecture:** Unopinionated `Protocol`-based abstractions. We evaluate the output; we don't dictate your execution graph.
3. **Production Telemetry:** First-class support for token-counting, per-step latency, cost attribution, and OpenTelemetry trace extraction.
4. **Resilience:** Built on `asyncio` and `tenacity` with semaphore-bounded concurrency, circuit breakers, and exponential backoff to handle provider rate-limits gracefully.

---

##  Architecture at a Glance

Wick is structured around cleanly segregated boundaries using Pydantic v2 and Python runtime Protocols.

<details>
<summary><b>Click to expand the Architecture Diagram & Folder Structure</b></summary>

```text
Wick/
├── wick/
│   ├── core/          
│   ├── runners/       
│   ├── scorers/       
│   ├── targets/        
│   ├── regression/    
│   ├── reporters/      
│   └── cli/            
├── tests/              
├── examples/           
└── pyproject.toml      


🚀 Quick Start

Installation
Requires Python 3.11+. We recommend using a virtual environment.

git clone [https://github.com/Prakhar00001/Wick.git](https://github.com/Prakhar00001/Wick.git)
cd Wick
pip install -e ".[dev]"

* Running Your First Suite
Verify the CLI is installed correctly. You should be greeted by the Wick banner.

wick --help

* Run a sample evaluation suite:

wick run examples/rag_suite.yaml

__      __  _          __    
 \ \    / / (_)  __    |  |__ 
  \ \/\/ /  | | / _|   |  |/ /
   \_/\_/   |_| \__|   |    < 
                       |__|\_\

WICK - Evaluation Harness

Comparing pr-1234 against main-baseline...

Metrics Delta:
• Groundedness: 0.92 ➔ 0.95 (+0.03) ✅
• Latency (P95): 850ms ➔ 710ms (-140ms) ✅
• Exact Match: 0.88 ➔ 0.81 (-0.07) ❌ (FAILED GATE)

Newly Failing Examples:
- EX-045: "Model hallucinated internal IP address."
- EX-099: "Failed to parse standard date format."

Exiting with code 1. CI pipeline blocked.


 * LICENSE
Distributed under the MIT License. See LICENSE for more information.
