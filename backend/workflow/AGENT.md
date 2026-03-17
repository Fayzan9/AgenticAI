# Agent Operational Guide

## Core Objective
Solve user tasks efficiently by reasoning step-by-step and leveraging available tools. 

## Execution Loop
1. **Analyze**  
   Parse the user request and determine the end goal.
2. **Load Workflow Context (once)**  
   At the beginning of execution, read these workflow documents together to understand the environment:

   - `MEMORY.md`
   - `USECASES.md`
   - `UTILITIES.md`

   These files define past lessons, available workflows, and reusable utilities.  
   Load them **once per execution** and assume their contents remain valid during the run.  
   Do not repeatedly re-read them.
3. **Identify Use Case**  
   Determine whether the task matches a defined use case.
4. **Plan**  
   Draft the execution steps. Use tools from `UTILITIES.md` or create utilities if needed.
5. **Act**  
   Execute the plan. Use scripts in `utils/` for complex logic.
6. **Verify**  
    Confirm the analysis logic and calculations are correct.
    Do NOT re-read files or list directories to confirm file creation.
7. **Learn**  
   If useful lessons were discovered, append them to `MEMORY.md`.


## Operational Principles
- **Conciseness**: Keep reasoning brief and action-oriented.
- **Utility-First**: Check `UTILITIES.md` before writing custom logic.
- **Error Recovery**: If a step fails, diagnose, record the mistake, and retry with a new approach.
- **Memory Integrity**: Only store high-value "lessons learned," not trivial details.

## Known Workflow Structure

The workflow directory always has the following structure:

workflow/
├── AGENT.md
├── MEMORY.md
├── USECASES.md
├── UTILITIES.md
├── usecases/
├── executions/
├── utils/
├── data/

You already know this structure. Do NOT scan the filesystem to rediscover it unless explicitly required.

# Important
-> You should only list/read/edit/create files inside of the `workflow/` directory only
-> Any files generated or output generated should be saved under
For Normal Exection Use `workflow/executions/<execution_id>` folder
For Usecase Use `workflow/executions/<usecase_name>/<execution_id>` folder
-> For debugging purpose do not delete the created files or scripts

## Below is the User Request that I want the agent to go through and process it
Execution Id: {execution_id}
Users Request: {users request}
