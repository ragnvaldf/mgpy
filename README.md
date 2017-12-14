# Dependency oriented programming through marked graph building

## Idea
A function's sole reason to exist in a software project is to do *something* based on it's input parameters. Once the function has done it's work, it returns *something else*. In many cases this output is used as input to several other functions. A function is not concerned with how or when the input parameter/state  was created, or if it is used by other functions. Functions which do not depend on eachother can be executed in any order or in parallell, without affecting the rest of the program. In conventional programming however the developer must define the order explicitly and implement measures on top of this to enable concurrent execution. The idea behind this project is that function invocation and multithreading can be pushed into the background through use of a library (this) that creates a Petri net based on function signatures. Once created, the scheduler will handle all function invocations, such that a function can only be run if all requirements are satisfied. Requirement in this setting being the function's input parameters, which were created by another function. Once function X completes it satisfies the requirement for each of it's dependent functions Yi.

A Petri net is a discrete event dynamic system which can describe distributed systems. A Petri net contains transitions representing events that occurs, and places represening conditions. Arcs between transitions and places describe pre and post conditions for transitions. The state(marking) of the system is defined by the the number of tokens in each place. When a transition fires, it consumes tokens from it's input places, and deposits new tokens in it's output places. A function which return y = f(x1, x2) can thus be reresented as a Petri Net with transition f and places y, x1 and x2. Assuming x1 and x2 was created by functions y1 and y2, y = f(y1(), y2()) could be represented by a Petri Net with transitions f, y1, y2 and places y, x1, x2, such that xi is output place of yi, and input place of f. This Petri Net satisfies the requirement of being a Marked Graph.

A Marked Graph in a subclass of Petri net where every place is restricted to having exactly 1 input and 1 output arc. This means there can not be conflict, but there can be concurrency. By writing code in such a way that a marked graph can be built, the order of execution need not be defined by the developer, since it is conflict free. The burden of allowing concurrency and parallellism can be pushed to the background through use of a multithreaded scheduler controlling the Petri Net.

## Project goals
1. Develop a python library to automate marked graph building from function requirement-provide definitions, as well as a multithreaded scheduler
2. Determine if developing programs in this manner is feasible, by developing a proof of concept program for visualization of the built graph
3. Implement a high level abstraction to simplify fork-join based parallellism on iterable types where operations can be applied to items independently
4. Examine feasibility of including support for GPGPU and grid computing through abstractions
5. Examine the following potential advantages and consequences of this style of programming
  * Concurrency handled in the background without programmer having to deal with threads
  * Model of program is built while programming, thus the architecture of the full program can easily be visualized
  * The model can be analyzed with established Petri net theory to discover potential defects
  * Profiling the full program can easily be done by toggling a flag in the scheduler, and the timing information can be represented visually in the model
  * Debugging a faulty program can be simplified, by keeping a backlog of the states of the Petri Net, which can be analyzed after a crash
  * Parts of program can easily be mocked, thus encouraging test driven development
  * Modular design and separation of concerns
  * Program flow can be changed by replacing a transition's assigned function, thus allowing both offline and online changes to be easily applied
