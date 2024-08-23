# CrewAI for Generating Email Replies

<a href="https://www.youtube.com/watch?v=1D4YoAUpjlg">Tutorial followed.</a>

<br> Changes from the tutorial:

- Fixed usage of duckduckgo search tool
  - LLM was unable to provide correct inputs to the tool
    - it kept on providing a dictionary rather than a string
  - made a wrapper around this tool to provide a custom description to tell it to provide a string
- Fixed the error `Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value=2, input_type=int]`
  - needed to change `verbose=2` -> `verbose=True`
- Provided email contents as an input to `crew.kickoff()` rather than passing it to each method in `EmailAgents` and `EmailTasks`
- Organized it into different .py files
- Made an `EmailReply` Python module
  - run using `python -m EmailReply.main`
- Use LLM model and email from .env
- used `@staticmethod` for the methods in `EmailAgents` and `EmailTasks` classes
  - these methods don't need/work on instances of `EmailAgents` or `EmailTasks`
- Slightly changed the inputs provided to `Agent` and `Task` constructors
