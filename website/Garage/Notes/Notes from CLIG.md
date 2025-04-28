many modern computers don’t have command-line at all

## Philosophy

- Corporations force people to use prepared marketplaces app stores
- new no-code approach replaces programmers (side note - also AI)
- cli allows you to see how things really work
- You can interact with computer at level much more deeper than any GUI offer
- Some time ago editor was in terminal
- Now terminal is a feature in editor
- Fundamental principles of good CLI design:
  - human-first
  - simple programs with clean interfaces can be combined into larger systems
  - Programs must be modular enough to be combined
  - Making programs composable is just as important as ever
  - people will use your software in a way you can’t even imagine
  - Where possible, a CLI should follow patterns that already exist.
  - Command should say not too much but at least something that user believes it’s working
  - Programs must be easy to discover for users, intuitive
  - In terminal user has a conversation with the program
  - robustness
    - handle unexpected input
    - idempotent operations when possible
    - can also come from keeping it simple
  - enjoyable to use
    - feeling that soft is on the user side
    - help programmers solkve their problems

## Guidelines

What I can do to make my CLI better.

Basics are essential and I must follow them. If not, my CLI will be hard to use.

Next section are nice to have. If I follow them, my CLi could be better than average CLI

### Basics

1. **Use a command-line argument parsing library where you can.**
   1. I will use Click in my Python project
2. **Return zero exit code on success, non-zero on failure.**
3. **Send output to `stdout`.**
4. **Send messaging to `stderr`.**
   1. logs
   2. errors

### Help

1. **Display help text when passed no options, the `-h` flag, or the `--help` flag.**
2. **Display a concise help text by default.**
   1. Click will handle this rule for me
3. **Show full help when `-h` and `--help` is passed.**'
4. **Provide a support path for feedback and issues.**
   1. for example: add link to github in the help text
5. **In help text, link to the web version of the documentation.**
6. **Lead with examples.**
7. **If you’ve got loads of examples, put them somewhere else**
8. **Display the most common flags and commands at the start of the help text.**
9. **Use formatting in your help text.**
10. **If the user did something wrong and you can guess what they meant, suggest it.**
11. **If your command is expecting to have something piped to it and `stdin` is an interactive terminal, display help immediately and quit.**

### Documentation

1. documentation should expand information that are toi long to keep show them in terminal
   1. It’s where people go to understand what your tool is for
   2. what it *isn’t* for
   3. how it works
   4. how to do everything they might need to do
2. **Provide web-based documentation.**
3. **Provide terminal-based documentation.**
4. **Consider providing man pages.**
   1. I can use [ronn](https://rtomayko.github.io/ronn/ronn.1.html)
   2. but [click-man](https://github.com/click-contrib/click-man) will be better for me because I sue Click

### Output

1. **Human-readable output is paramount.**
   1. Further reading: <https://unix.stackexchange.com/questions/4126/what-is-the-exact-difference-between-a-terminal-a-shell-a-tty-and-a-con/4132#4132>
2. **Have machine-readable output where it does not impact usability.**
3. **If human-readable output breaks machine-readable output, use `--plain` to display output in plain, tabular text format for integration with tools like `grep` or `awk`.**
4. **Display output as formatted JSON if `--json` is passed.**
5. **Display output on success, but keep it brief.**
6. **If you change state, tell the user.**
   1. example: git push
7. **Make it easy to see the current state of the system.**
8. **Suggest commands the user should run.**
9. **Actions crossing the boundary of the program’s internal world should usually be explicit.**
   1. reading or weriting files that user do not pass as argument
   2. talking to a remote server
10. **Increase information density—with ASCII art!**
11. **Use color with intention.**
12. **Disable color if your program is not in a terminal or the user requested it**
    1. `stdout` or `stderr` is not an interactive terminal (a TTY).
    2. The `NO_COLOR` environment variable is set
    3. The `TERM` environment variable has the value `dumb`.
    4. The user passes the option `--no-color`.
    5. add a `MYAPP_NO_COLOR` environment variable in case users want to disable color specifically for your program.
    6. _Further reading: [no-color.org](https://no-color.org/), [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46)_
    7. **If `stdout` is not an interactive terminal, don’t display any animations.**
    8. **Use symbols and emoji where it makes things clearer.**
    9. **By default, don’t output information that’s only understandable by the creators of the software.**
    10. **Don’t treat `stderr` like a log file, at least not by default.**
    11. **Use a pager (e.g. `less`) if you are outputting a lot of text.**

### Errors

1. **Catch errors and rewrite them for humans.**
2. **Signal-to-noise ratio is crucial.**
3. **Consider where the user will look first.**
4. **If there is an unexpected or unexplainable error, provide debug and traceback information, and instructions on how to submit a bug.**
   1. Consider writing the debug log to a file instead of printing it to the terminal.
5. **Make it effortless to submit bug reports.**
6. _Further reading: [Google: Writing Helpful Error Messages](https://developers.google.com/tech-writing/error-messages), [Nielsen Norman Group: Error-Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines)_

### Arguments and flags

1. **Prefer flags to args.**
2. **Have full-length versions of all flags.**
3. **Only use one-letter flags for commonly used flag**
4. **Multiple arguments are fine for simple actions against multiple files**
5. **If you’ve got two or more arguments for different things, you’re probably doing something wrong.**
6. **Use standard names for flags, if there is a standard.**
7. **Make the default the right thing for most users.**
8. **Prompt for user input.**
9. **Never *require* a prompt.**
10. **Confirm before doing anything dangerous.**
11. **If input or output is a file, support `-` to read from `stdin` or write to `stdout`**
12. **If a flag can accept an optional value, allow a special word like “none.”**
13. **If possible, make arguments, flags and subcommands order-independent.**
14. **Do not read secrets directly from flags.**

### Interactivity

1. **Only use prompts or interactive elements if `stdin` is an interactive terminal (a TTY)**
2. **If `--no-input` is passed, don’t prompt or do anything interactive.**
3. **If you’re prompting for a password, don’t print it as the user types.**
4. **Let the user escape.**

### Subcommands

1. **Be consistent across subcommands.**
2. **Use consistent names for multiple levels of subcommand.**
   1. for complex software, it is a common pattern to use two levels of subcommand, where one is a noun and one is a verb. For example, `docker container create`
   2. _Further reading: [User experience, CLIs, and breaking the world, by John Starich](https://uxdesign.cc/user-experience-clis-and-breaking-the-world-baed8709244f)_
3. **Don’t have ambiguous or similarly-named commands.**

### Robustness

1. **Validate user input.**
2. **Responsive is more important than fast.**
3. **Show progress if something takes a long time.**
   1. I can use this in Python <https://github.com/tqdm/tqdm>
4. **Do stuff in parallel where you can, but be thoughtful about it.**
5. **Make things time out.**
6. **Make it recoverable.**
7. **Make it crash-only.**
8. **People are going to misuse your program.**

### Future-proofing

1. **Keep changes additive where you can.**
2. **Warn before you make a non-additive change.**
3. **Changing output for humans is usually OK.**
4. **Don’t have a catch-all subcommand.**
5. **Don’t allow arbitrary abbreviations of subcommands.**
6. **Don’t create a “time bomb.”**

### Signals and control characters

1. **If a user hits Ctrl-C (the INT signal), exit as soon as possible.**
2. **If a user hits Ctrl-C during clean-up operations that might take a long time, skip them.**

### Configuration

1. configuration categories:

   1. Likely to vary from one invocation of the command to the next like - Setting the level of debugging output
      1. use flags for this
   2. Generally stable from one invocation to the next, but not always. This type of configuration is often specific to an individual computer.

      1. Examples:

      - Providing a non-default path to items needed for a program to start
      - Specifying how or whether color should appear in output
      - Specifying an HTTP proxy server to route all requests through
      - use flags and probbably environment variables

   3. Stable within a project, for all users.
      1. **Use a command-specific, version-controlled file.**

2. **Follow the XDG-spec.**
3. **If you automatically modify configuration that is not your program’s, ask the user for consent and tell them exactly what you’re doing.**
4. **Apply configuration parameters in order of precedence.**
   - Flags
   - The running shell’s environment variables
   - Project-level configuration (e.g. `.env`)
   - User-level configuration
   - System wide configuration

### Environment variables

1. **Environment variables are for behavior that *varies with the context* in which a command is run.**
2. **For maximum portability, environment variable names must only contain uppercase letters, numbers, and underscores (and mustn’t start with a number).**
3. **Aim for single-line environment variable values.**
4. **Avoid commandeering widely used names.**
5. **Check general-purpose environment variables for configuration values when possibl**
6. **Read environment variables from `.env` where appropriate.**
7. **Don’t use `.env` as a substitute for a proper [configuration file](https://clig.dev/#configuration).**
8. **Do not read secrets from environment variables.**

### Naming

1. **Make it a simple, memorable word.**
2. **Use only lowercase letters, and dashes if you really need to.**
3. **Keep it short.**
4. **Make it easy to type.**

### Distribution

1. **If possible, distribute as a single binary.**
2. **Make it easy to uninstall.**

### Analytics

1. **Do not phone home usage or crash data without consent.**
2. alternative analytycs
   1. Instrument your web docs
   2. Instrument your downloads.
   3. Talk to your users.

---

## Further reading

- [What is TTY](https://unix.stackexchange.com/questions/4126/what-is-the-exact-difference-between-a-terminal-a-shell-a-tty-and-a-con/4132#4132)
- [no-color.org](https://no-color.org/)
- [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46)
- [Google: Writing Helpful Error Messages](https://developers.google.com/tech-writing/error-messages)
- [Nielsen Norman Group: Error-Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines)
- [GNU Coding Standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)
- [User experience, CLIs, and breaking the world, by John Starich](https://uxdesign.cc/user-experience-clis-and-breaking-the-world-baed8709244f)
- [Crash-only software: More than meets the eye](https://lwn.net/Articles/191059/)
- [The Poetics of CLI Command Names](https://smallstep.com/blog/the-poetics-of-cli-command-names/)
- [Open Source Metrics](https://opensource.guide/metrics/)
- [The Unix Programming Environment](https://en.wikipedia.org/wiki/The_Unix_Programming_Environment), Brian W. Kernighan and Rob Pike
- [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
- [Program Behavior for All Programs](https://www.gnu.org/prep/standards/html_node/Program-Behavior.html), GNU Coding Standards
- [CLI Style Guide](https://devcenter.heroku.com/articles/cli-style-guide), Heroku

---

**Attribution & License Information:**

These notes are based on **Command Line Interface Guidelines** available at [clig.dev](https://clig.dev), licensed under [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

This document is also licensed under [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
