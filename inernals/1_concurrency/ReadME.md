Concurrency

Concurrency is about managing multiple tasks at the same time.2 It deals with the structure of a program that has multiple independent units of work.3 A single-core CPU can handle concurrency by rapidly switching between different tasks.4 It's the illusion of simultaneous execution.

Key Characteristics:
* Single-core CPU: Can be achieved on a machine with a single processing core.5
* Context Switching: The operating system switches between tasks, giving each one a small slice of CPU time.6
* Focus: It's about structuring the program to handle multiple tasks gracefully. It's a design concern.





Parallelism

Parallelism is about executing multiple tasks simultaneously. This requires hardware with multiple processing units (like a multi-core CPU) that can perform work at the exact same time.

Key Characteristics:
* Multi-core CPU: Requires hardware with at least two processing cores.
* Simultaneous Execution: Tasks are physically running at the same moment.9
* Focus: It's a performance concern, aiming to speed up computation by leveraging multiple cores.10


Difference between concurrency and parallelism

Feature	Concurrency	Parallelism
Execution	Tasks are interleaved (not necessarily simultaneous)	Tasks are executed simultaneously
Hardware	Can be on a single-core CPU	Requires a multi-core CPU
Goal	To handle many things at once (structure)	To do many things at once (performance)
Example	A single CPU switching between a browser and a text editor	A multi-core CPU running different parts of a video rendering task on each core
Analogy	One chef juggling multiple dishes	Multiple chefs each working on their own dish
