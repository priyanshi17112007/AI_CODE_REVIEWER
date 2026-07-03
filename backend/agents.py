import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task,LLM

try:
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except Exception:
    pass

# Load environment variables
load_dotenv()

# Configure your Groq model instance
llm_instance = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)

async def analyze_code_with_crew(code_content: str):
    # 1. Define Specialized Cyber Security & QA Agents
    security_auditor = Agent(
        role="Senior Application Security Engineer",
        goal="Identify severe vulnerabilities, injection flaws, OWASP Top 10, and hardcoded secrets.",
        backstory="An elite ethical hacker with an eye for finding hidden security exploits and vulnerabilities in source code.",
        verbose=False,
        llm=llm_instance,
        temperature=0.1  # Keeps agent deterministic and strict
    )

    qa_engineer = Agent(
        role="Principal Quality Assurance & Syntax Auditor & Performance Engineer",
        goal="Detect syntax anomalies, faulty conditional logic, variable scope errors, and structural bugs & Uncover logical bugs, data loops, infinite loops, and heavy runtime complexities (O(n^2) issues).",
        backstory="A precise code linter and compiler design expert. You excel at spotting human errors "
            "such as missing colons, bracket mismatches, incorrect comparison operators, "
            "uninitialized variables, and flawed conditional logic paths."
             "A strict code optimizer specializing in structural runtime failures and logic breakages.",
        verbose=False,
        llm=llm_instance,
        temperature=0.1  # Prevents creative deviations from JSON formatting
    )

    # 2. Assign Tasks with strict formatting requirements
    security_task = Task(
        description=(
            f"Analyze this code block for security issues:\n\n{code_content}\n\n"
            "Provide the response strictly as a JSON list of objects containing: "
            "'severity' (High/Medium/Low), 'title', 'location', and 'description'. "
            "Do not include markdown code block syntax."
        ),
        expected_output="A raw valid JSON array representing security vulnerabilities.",
        agent=security_auditor
    )
    

    qa_task = Task(
        description=(f"Analyze this code block for logical bugs, infinite loops, or deep nesting bottlenecks:\n\n{code_content}\n\nProvide the response strictly as a JSON list of objects containing: 'bug_type', 'impact', and 'fix_suggestion'. Do not include markdown code block syntax."
                     "Specifically inspect for:\n"
            "- Syntax Errors: Missing punctuation, indentation flaws, unclosed strings.\n"
            "- Conditional Errors: Wrong operators (e.g., using '=' instead of '=='), flawed 'if/else' logic, or off-by-one loop limits.\n"
            "- Semantic Errors: Unused variables, undefined function calls, type mismatches.\n\n"
            "Provide the response strictly as a JSON list of objects containing: 'bug_type', 'impact', and 'fix_suggestion'. "
            "Do not include markdown code block syntax."),
        expected_output="A raw valid JSON array representing structural code bugs.",
        agent=qa_engineer
    )

    # 3. Assemble and Kick off the Swarm Sequential Pipeline
    crew = Crew(
        agents=[security_auditor, qa_engineer],
        tasks=[security_task, qa_task],
        process=Process.sequential
    )

    result = await crew.kickoff_async()
    return result