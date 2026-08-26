# Learn help

Help you train your skills theoretically or practically

## Important!

This App using private library for interacting with data devices (such as Yandex or Google drivers).
So you need to get this library and install it locally with

```bash
pip install /path/to/device_lib.whl
```

Also, this app using private lib for interacting with AI

```bash
pip install /path/to/ai_lib.whl
```

And for the brave of optimization, this utility has some rust, to compile it, execute next commands:
```bash
maturin develop
```

## Question types:

1. Simple - just question and answer
2. Variants - questions, where you might choose between options
3. Timer - only limited time for solve
4. Writing - question with writing correct answer
5. AI_check - push AI to check your answer