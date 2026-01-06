Task Dependencies
=================

In many workflows, tasks depend on the results of other tasks.
**Pravaha** allows you to define task dependencies using the ``depends_on`` attribute.

Defining dependencies ensures that tasks are executed in the correct order and
prevents failures caused by missing prerequisites.

---

Defining Dependencies
---------------------

Pravaha supports two types of dependencies:

1. **OR-based dependencies**
2. **AND-based dependencies**

---

OR-based Dependencies
---------------------

An **OR-based dependency** means that a task will execute if **at least one**
of its dependent tasks completes successfully.

Example
^^^^^^^

.. code-block:: python

    from pravaha.core.task import Task
    from pravaha.core.executor import TaskExecutor
    from pravaha.dependency.dependency import Dependency

    # Dependency(type="OR | AND", dependencies=list[str])
    @Task("a", depends_on=Dependency("OR", dependencies=["b", "c"]))
    def a():
        print("a")

    @Task("b")
    def b():
        pass

    @Task("c")
    def c():
        pass

    TaskExecutor.execute()

---

AND-based Dependencies
----------------------

An **AND-based dependency** means that a task will execute **only if all**
of its dependent tasks complete successfully.

AND-based dependencies can be defined in two ways.

### 1. Implicit AND dependency using a list

By default, passing a list to ``depends_on`` is treated as an **AND dependency**.

.. code-block:: python

    from pravaha.core.task import Task
    from pravaha.core.executor import TaskExecutor

    @Task(name="task1", depends_on=["task2"])
    def task1():
        print("Task1 executed")

    @Task(name="task2")
    def task2():
        print("Task2 executed")

    if __name__ == "__main__":
        TaskExecutor.execute()

Expected Output
^^^^^^^^^^^^^^^

.. code-block:: text

    Task2 executed
    Task1 executed

---

### 2. Explicit AND dependency using ``Dependency``

You can also explicitly define an AND-based dependency using the ``Dependency`` object.

.. code-block:: python

    from pravaha.core.task import Task
    from pravaha.core.executor import TaskExecutor
    from pravaha.dependency.dependency import Dependency

    # Dependency(type="OR | AND", dependencies=list[str])
    @Task("a", depends_on=Dependency("AND", dependencies=["b", "c"]))
    def a():
        print("a")

    @Task("b")
    def b():
        pass

    @Task("c")
    def c():
        pass

    TaskExecutor.execute()

---

Notes
-----

- **Task registration order does not matter** when dependencies are defined.
- The executor automatically determines the **correct execution order**
  based on the dependency graph.
- Circular dependencies are not allowed. Ensure that your workflow graph
  is **acyclic (DAG)**.
