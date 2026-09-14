# Week 01 Homework - Profiling Scripts

This week in class we learned how to time and profile code inside a Jupyter Notebook with the magic commands `%timeit`, `%prun` and `%lprun`. Notebooks are not the only way to run code, however; oftentimes larger projects will live in **Python scripts** ending with the `.py` extension. 

The magic commands aren't available in \scripts so we need alternative methods for timing and profiling. In class we learned about the `perf_counter()` function from the `time` module. In this homework, you'll get practice instrumenting timers into a script and profiling it both function-by-function and line-by-line.

## About the Problem - 2D Poisson Equation

One file is a module

## Instructions

For this homework, you'll need a Linux command line with your `hpc-python` environment loaded.
**I strongly recommend using the OnDemand Interactive Desktop App**. The instructions for step 3 will open a new web browser window; this doesn't play well with the JupyterLab app. For VSCode users, your milleage may vary depending on your setup.

1. Using what we learned in class, time how long it takes to solve the Poisson equation. Edit the Python file you feel is appropriate. Make sure to avoid timing any extraneous operations. _Where should they tell me how long it took?_
2. In a Jupyter Notebook we can use the `%prun` magic command, but for a script we use the `cProfile` module. Thankfully, we don't have to modify our code; we can just load the module along with whatever file we want to profile! This looks like `python -m cProfile <filename>`. Use `cProfile` to profile the Python file you feel is appropriate.
3. The step above should have dumped an awful lot of inscruitable information onto your screen. Thankfully there is a visualization tool called `snakeviz` that can help us. To use `snakeviz`,
we need to save the output of our profiling by adding the "output" option and specifying a filename: `python -m cProfile -o poisson.prof <filename>`. Then run `snakeviz poisson.prof`. **I suggest using the OnDemand Interactive Desktop for this.**
4. The `snakeviz` interface is quite nice because it let's you see which functions call other functions. This let's you filter extraneous information. If your results don't make sense, try profiling the other file. _Which function (that isn't from an external library like NumPy) should we target for optimization? Which statistics tell us so?_
4. _Have students instrument line profiler following [these](https://kernprof.readthedocs.io/en/latest/) docs_


## Instructor's AI Disclosure

I used VSCode CoPilot to brainstorm and write the exercise for this assignment. I asked it for a number of computational science examples that would fit a lesson on profiling and then asked it to generate the suggestion I liked best following some desired structural features (e.g. have one file act as a module with many functions). It created `poisson_solver.py` and `poisson_demo.py`, the latter of which I then edited to look more like a researcher-produced script rather than a formal bit of software.
