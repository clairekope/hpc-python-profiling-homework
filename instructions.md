# Week 01 Homework - Profiling Scripts

This week in class we learned how to time and profile code inside a Jupyter Notebook with the magic commands `%timeit`, `%prun` and `%lprun`. Notebooks are not the only way to run code, however; oftentimes larger projects will live in **Python scripts** ending with the `.py` extension. 

The magic commands aren't available in \scripts so we need alternative methods for timing and profiling. In class we learned about the `perf_counter()` function from the `time` module. In this homework, you'll get practice instrumenting timers into a script and profiling it both function-by-function and line-by-line.

## About the Problem - 2D Poisson Equation

The 2D Poisson equation is a standard example in computational science. In simple terms, it describes how a quantity spreads out in space, such as heat in a metal plate or electric potential in a region.

We write it as:

$$
-\nabla^2 u(x, y) = f(x, y)
$$

where `u` is the unknown value we want to compute, and `f` is the source term that drives the system.

In this assignment, we solve the equation on a grid. That turns the problem into a large system of equations, which we can write as:

$$
A u = b
$$

where `A` is a matrix that encodes the relationship between the grid points, `u` is the vector of unknown values we want to find, and `b` encodes the source term `f` (an sometimes any boundary conditions).

We're using this problem as a profiling because it is relatively easy to understand but a naive or "first draft" implementation can be very slow. As the grid gets larger, the matrix gets much bigger, and the time spent solving the system grows rapidly.

The Poisson problem is common in many scientific simulations, including:

- heat flow,
- diffusion,
- electrostatics,
- fluid flow,
- and other physical models that are solved on a grid, usually involving partial differential equations.

The goal of this homework is not to master the physics of the equation. Instead, it is to see how a simple scientific calculation can become slow in Python and how profiling helps us find the bottleneck.

## Files in this Directory

This directory contains a small example workflow that mirrors how scientific code is often organized:

- `poisson_solver.py`: the main numerical code. This file builds the problem, assembles the matrix, solves it, and returns the result.
- `poisson_demo.py`: a small script that runs the solver and visualizes the results.

Please put your answers to the assignment below in `answers.md`. Be sure to commit and push all changes to the files in this directory.

## Assignment

For this homework, you'll need a Linux command line with your `hpc-python` environment loaded.
**I strongly recommend using the OnDemand Interactive Desktop App**. The instructions for step 3 will open a new web browser window; this doesn't play well with the JupyterLab app. For VSCode users, your milleage may vary depending on your setup.

1. Using what we learned in class, how long does it take to solve the Poisson equation? Write your answer in `answers.md` and also submit your modified code so I can see *how* you timed it.
2. In a Jupyter Notebook we can use the `%prun` magic command, but for a script we use the `cProfile` module. Thankfully, we don't have to modify our code; we can just load the module along with whatever file we want to profile! This looks like `python -m cProfile <filename>`. Use `cProfile` to profile the Python file you feel is appropriate.
3. The step above should have dumped an awful lot of inscruitable information onto your screen. Thankfully there is a visualization tool called `snakeviz` that can help us. To use `snakeviz`,
we need to save the output of our profiling by adding the "output" option and specifying a filename: `python -m cProfile -o poisson.prof <filename>`. Then run `snakeviz poisson.prof`. **I suggest using the OnDemand Interactive Desktop for this.**
4. The `snakeviz` interface is quite nice because it let's you see which functions call other functions. This let's you filter extraneous information. If your results don't make sense, try profiling the other file. Which function (that isn't from an external library like NumPy) should we target for optimization? Which statistics tell us so?
5. In class, we worked with a line profiler using the `%lprun` magic command, but we can also use it in a script. Read the [line profiler documentation](https://kernprof.readthedocs.io/en/latest/) to see how to do this and profile the function we identified in step 4. When finished, some instructions for viewing the profiling results should print to the screen. Follow these instructions, and snakeviz won't work with line profiler's output. Which line takes the most overall time? Why does this make sense given what is happening with the code (e.g., the for-loops)?
6. Still looking at the line profiler results, which line takes the longest per-hit time? Why does it take so long, and why is this line necessary for the algorithm (i.e., for Gaussian elimination)?
7. Do you have a guess as to what we might do to improve the speed of our Poisson solver? It's ok if you don't right now; that's what this class is for!
8. Why do profilers provide so many different timing measurements (total, per-hit, etc.)? What can these metrics teach us?
9. Which profiling tool was the most useful for this exercise, `cProfile` + SnakeViz or `line_profiler`? Why? Is this different from the in-class assignment?

## Instructor's AI Disclosure

I used VSCode CoPilot to brainstorm and write the exercise for this assignment. I asked it for a number of computational science examples that would fit a lesson on profiling and then asked it to generate the suggestion I liked best following some desired structural features (e.g. have one file act as a module with many functions). It created `poisson_solver.py` and `poisson_demo.py`. I asked CoPilot to iterate on the former in order to make it a useful teaching demo, and edited the latter myself to make it look more like a researcher-produced script rather than a formal bit of software. Lastly, CoPilot brainstormed some summative questions for the assignment that inspired questions 8 and 9.

I also used CoPilot to write most of the introduction section to this homework, mostly because it's been a long time since I've had to think about these details. While it is something easily refreshed for me, it wasn't worth the effort of, say, translating a Wikipedia article into something approachable. :)
