# **Question & Answer Interview ** for **Python**, split into **Beginner (~50 Q&A)**, **Intermediate (~50 Q&A)**, and **Advanced (~50 Q&A)** levels.

---

## Beginner Level

These questions test basic Python concepts: syntax, data types, control-flow, built-ins.

### 1. **Q:** What is Python? Name a few key features.
   
**Answer:**

* Python is a high-level, interpreted, general-purpose programming language. 
* Key features include: readable & clear syntax; dynamic typing; automatic memory management; large standard library; cross-platform. 
* Example:

     ```python
     print("Hello, world!")
     ```

     runs without needing explicit compilation.

### 2. **Q:** What is the difference between a list and a tuple in Python?
   
**Answer:**

* A **list** is mutable (you can change, add, remove items) and defined with square brackets `[]`.
* A **tuple** is immutable (once created you cannot change its items) and defined with parentheses `()`. 
* Example:

     ```python
     my_list = [1, 2, 3]
     my_list[0] = 10  # OK
     my_tuple = (1, 2, 3)
     # my_tuple[0] = 10  # Error
     ```

### 3. **Q:** Explain what the `__init__` method is in Python classes.
   
**Answer:**

* `__init__` is the constructor method in Python classes: it’s automatically called when a new instance is created. 
* It’s used to initialize instance attributes.
* Example:

     ```python
     class Person:
         def __init__(self, name, age):
             self.name = name
             self.age = age

     p = Person("Alice", 30)
     print(p.name, p.age)  # “Alice 30”
     ```

### 4. **Q:** Is Python a compiled language or an interpreted language?
   
**Answer:**

* Python is generally considered an interpreted language, since its code is executed by the Python Virtual Machine (PVM) after it is compiled into bytecode. 
* Under the hood: source code → compiled to `.pyc` bytecode → interpreted/executed.
* Example: When you run `python script.py`, the interpreter handles execution.

### 5. **Q:** What is indentation in Python & why is it important?
   
**Answer:**

* Indentation in Python defines the blocks of code (for loops, if statements, function definitions). It is **required**; Python uses indentation instead of braces. 
* Wrong indentation leads to `IndentationError`.
* Example:

     ```python
     if x > 0:
         print("Positive")
         # this line must be indented
     ```

### 6. **Q:** What is the difference between the `/` and `//` operators in Python?
   
**Answer:**

* `/` is “true division” (floating-point) even if operands are integers in Python 3.
* `//` is floor (or integer) division: it returns the quotient truncated toward negative infinity (for positive numbers, simply integer part). Example: `5//2 == 2`, `5/2 == 2.5`. 
* Example:

     ```python
     print(5 / 2)   # 2.5
     print(5 // 2)  # 2
     ```

### 7. **Q:** What is dynamic typing?
   
**Answer:**

* Dynamic typing means that you don’t have to declare the type of a variable; the type is determined at runtime. 
* Example:

     ```python
     a = 5        # a is int
     a = "hello"  # now a is str
     ```

### 8. **Q:** How can you concatenate two lists in Python?
   
**Answer:**

* Use the `+` operator: `a + b` gives a new list combining `a` and `b`. 
* Or use `list.extend()`: modifies the first list in-place.
* Example:

     ```python
     a = [1,2,3]
     b = [4,5]
     c = a + b      # [1,2,3,4,5]
     a.extend(b)    # a becomes [1,2,3,4,5]
     ```

### 9. **Q:** What is slicing in Python?
   
**Answer:**

* Slicing is a way to extract subsets of sequences (strings, lists, tuples) using `[start:stop:step]` notation. 
* Example:

     ```python
     numbers = [0,1,2,3,4,5,6]
     print(numbers[1:5])     # [1,2,3,4]
     print(numbers[::2])     # [0,2,4,6]
     print(numbers[::-1])    # reversed list [6,5,4,3,2,1,0]
     ```

### 10. **Q:** What is the difference between mutable and immutable data types?
    
**Answer:**

* Mutable types: their contents can be changed after creation (lists, dictionaries, sets).
* Immutable types: their contents cannot be changed (strings, tuples, integers). 
* Example:

    ```python

        s = "hello"
        # s[0] = "H"   # Error
        lst = [1,2,3]
        lst[0] = 9     # OK
    ```

### 11. **Q:** What is a module and what is a package in Python?
    
**Answer:**

* A **module** is a single `.py` file containing Python definitions (functions, classes, variables) that you can import.
* A **package** is a directory containing modules, and must include an `__init__.py` file (in older Python versions) to be recognized as a package. 
* Example:

    ```
      mypackage/
         __init__.py
         module1.py
         module2.py
    ```

Then you can `import mypackage.module1` etc.

### 12. **Q:** What does the `pass` statement do?
    
**Answer:**

* `pass` is a no-operation placeholder: it does nothing when executed. It’s useful when you need a syntactically valid block but haven’t implemented it yet. 
* Example:

      ```python
      def not_implemented_yet():
          pass
      ```

### 13. **Q:** What is the difference between “pass by value” and “pass by reference” in Python?
    
**Answer:**

* Python uses a model often called “pass by object reference” (or “pass by assignment”). 
* If you pass a mutable object to a function, modifications inside can affect the caller’s object. If you pass an immutable object, you cannot modify it in place.
* Example:

    ```python
      def f(x):
          x += [3]

      lst = [1,2]
      f(lst)
      print(lst)  # [1,2,3] because list is mutable

      def g(x):
          x += 5

      n = 2
      g(n)
      print(n)    # 2 – ints immutable
    ```

### 14. **Q:** How do you floor a number in Python (i.e., get the largest integer ≤ x)?
    
**Answer:**

* Use `math.floor()` from the `math` module. 
* Example:

    ```python
      import math
      print(math.floor(3.7))   # 3
     ```

### 15. **Q:** What is the difference between `for` and `while` loops in Python?
    
**Answer:**

* `for` loop: iterates over a known sequence (list, tuple, range).
* `while` loop: runs until a given condition becomes false — useful when number of iterations isn’t known ahead of time. 
* Example:

    ```python
      for i in range(5):
          print(i)

      c = 0
      while c < 5:
          print(c)
          c += 1
    ```

### 16. **Q:** What is a dictionary in Python?
    
**Answer:**

* A dictionary (`dict`) is a built-in mutable mapping type: key → value pairs, with unique keys.
* Example:

    ```python
      d = {"name": "Alice", "age": 30}
      print(d["name"])  # “Alice”
      d["city"] = "Bangalore"
    ```

### 17. **Q:** How do you iterate through a dictionary’s keys and values?
    
**Answer:**

* Use `dict.items()` to get `(key, value)` pairs; `dict.keys()` for keys; `dict.values()` for values.
* Example:

    ```python
      for key, value in d.items():
          print(f"{key} -> {value}")
    ```

### 18. **Q:** What is a list comprehension? Give an example.
    
**Answer:**

* A concise way to create lists using a single expression, often replacing loops.
* Example:

    ```python
      squares = [x*x for x in range(1, 6)]  # [1,4,9,16,25]
      even = [x for x in range(10) if x % 2 == 0]  # [0,2,4,6,8]
    ```

### 19. **Q:** What is the difference between `==` and `is` in Python?
    
**Answer:**

* `==` tests value equality (are the objects’ values equal?).
* `is` tests identity (are the two references pointing to the **same** object?).
* Example:

    ```python
      a = [1,2,3]
      b = [1,2,3]
      print(a == b)  # True
      print(a is b) # False
    ```

### 20. **Q:** What happens if you modify a list while iterating it?
    
**Answer:**

* It can lead to unexpected behavior (skip elements or run indefinitely). It’s safer either to iterate over a copy or build a new list.
* Example:

    ```python
      lst = [1,2,3,4]
      for x in lst:
          if x % 2 == 0:
              lst.remove(x)
      print(lst)  # might result in [1,3] or skip one.
    ```

### 21. **Q:** Explain what the `__name__ == "__main__"` idiom does.
    
**Answer:**

* When a Python file is run directly (not imported), `__name__` is set to `"__main__"`.
* So we use:

    ```python
      if __name__ == "__main__":
          main()
    ```

to ensure `main()` runs only when script is executed, not when imported.

### 22. **Q:** What is the difference between `append()` and `extend()` methods on lists?
    
**Answer:**

* `append(x)`: adds a single item `x` at end of list.
* `extend(iterable)`: iterates over `iterable`, adding each element to the list.
* Example:

    ```python
      lst = [1,2]
      lst.append([3,4])
      print(lst)  # [1,2,[3,4]]

      lst2 = [1,2]
      lst2.extend([3,4])
      print(lst2) # [1,2,3,4]
    ```

### 23. **Q:** What is a set in Python? What are its basic properties?
    
**Answer:**

* A set is an unordered collection of unique elements (mutable).
* Useful for membership testing, eliminating duplicates.
* Example:

    ```python
      s = {1,2,3,2,1}
      print(s)  # {1,2,3}
      s.add(4)
    ```

### 24. **Q:** What is a generator in Python?
    
**Answer:**

* A generator is a special kind of iterator, defined using a function with `yield`, or by using generator expression `( … for … )`.
* It produces values lazily (on demand) and is memory‐efficient for large data sets.
* Example:

    ```python
      def my_gen(n):
          for i in range(n):
              yield i*i

      for x in my_gen(5):
          print(x)  # 0,1,4,9,16
    ```

### 25. **Q:** What is the difference between `=` and `==` in Python?
    
**Answer:**

* `=` is the assignment operator: `a = 10` assigns value `10` to variable `a`.
* `==` is the equality comparison operator: `a == 10` returns `True` if `a` equals `10`.

### 26. **Q:** How do you swap two variables in Python without a temporary variable?
    
**Answer:**

* Python allows tuple unpacking:

    ```python
      a = 5
      b = 10
      a, b = b, a
      print(a, b)  # 10 5
    ```

### 27. **Q:** What is the difference between `deepcopy` and `copy` (shallow copy) in Python?
    
**Answer:**

* Shallow copy (`copy.copy()`): creates a new object, but nested elements still refer to original objects.
* Deep copy (`copy.deepcopy()`): creates new object **and** recursively copies nested objects so that no references to the original nested objects remain.
* Example:

    ```python
      import copy
      original = [[1,2],[3,4]]
      shallow = copy.copy(original)
      deep = copy.deepcopy(original)
      original[0][0] = 999
      print(shallow)  # [[999,2],[3,4]]
      print(deep)     # [[1,2],[3,4]]
    ```

### 28. **Q:** What does the `@staticmethod` decorator do?
    
**Answer:**

* In a class, `@staticmethod` defines a method that does **not** receive `self` or `cls` parameter; it's just a function within a class’s namespace.
* Example:

    ```python
      class MyClass:
          @staticmethod
          def greet(name):
              print(f"Hello {name}")

      MyClass.greet("Alice")
     ```

### 29. **Q:** What does the `@classmethod` decorator do?
    
**Answer:**

* In a class, `@classmethod` defines a method that receives the class itself (`cls`) as the first parameter instead of `self`.
* Useful for factory methods.
* Example:

    ```python
      class MyClass:
          count = 0

          def __init__(self):
              MyClass.count += 1

          @classmethod
          def how_many(cls):
              print(f"{cls.count} instances so far")

      m1 = MyClass()
      m2 = MyClass()
      MyClass.how_many()  # “2 instances so far”
    ```

### 30. **Q:** How can you install external packages in Python?
    
**Answer:**

    * Using `pip`, e.g.:

      ```bash
      pip install requests
      ```
* You can also use `venv` to create virtual environments to isolate dependencies.
* Note: For best practice, use `requirements.txt` to freeze versions.

### 31. **Q:** What is PEP 8?
    
**Answer:**

* PEP 8 is the Python Enhancement Proposal that describes the coding style guidelines for Python code — naming conventions, formatting, whitespace, etc.
* Adhering to PEP 8 helps maintain readable and consistent code across teams.

### 32. **Q:** What is a lambda function in Python? Provide an example.
    
**Answer:**

* A lambda function is an anonymous (no name) small function defined with the `lambda` keyword.
* Example:

    ```python
      square = lambda x: x*x
      print(square(5))  # 25
  ```

### 33. **Q:** What is the usage of the `map()` and `filter()` functions?
    
**Answer:**

* `map(func, iterable)`: applies `func` to each item in `iterable`, returns an iterator.
* `filter(func, iterable)`: returns items for which `func(item)` is `True`.
* Example:

    ```python
      nums = [1,2,3,4]
      squares = list(map(lambda x: x*x, nums))  # [1,4,9,16]
      evens = list(filter(lambda x: x%2==0, nums)) # [2,4]
    ```

### 34. **Q:** What is string formatting in Python? Provide an example using f-strings.
    
**Answer:**

* f-strings (Python 3.6+): embed expressions inside string literals using `{}` and prefix `f` before string.
* Example:

    ```python
      name = "Alice"
      age = 30
      print(f"{name} is {age} years old.")  # “Alice is 30 years old.”
    ```

### 35. **Q:** Explain how to handle exceptions in Python.
    
**Answer:**

* Use `try‐except` blocks to catch exceptions, optionally `finally`, optionally `else`.
* Example:

    ```python
      try:
          x = int(input("Enter a number: "))
          y = 10/x
      except ValueError:
          print("Invalid input, not an integer.")
      except ZeroDivisionError:
          print("Cannot divide by zero.")
      else:
          print("Result:", y)
      finally:
          print("Done.")
    ```

### 36. **Q:** What is the `with` statement (context manager) used for?
    
**Answer:**

* The `with` statement simplifies resource management (opening/closing files, locks) by guaranteeing the correct acquisition and release of resources.
* Example:

    ```python
      with open("file.txt", "r") as f:
          data = f.read()
      # file is automatically closed when leaving block
    ```

### 37. **Q:** What is slicing a string in Python? Provide an example.
    
**Answer:**

* Similar to lists: you can slice strings. Example:

    ```python
      s = "Hello, world!"
      print(s[0:5])     # “Hello”
      print(s[::-1])    # “!dlrow ,olleH”
    ```

### 38. **Q:** How do you convert a string to an integer in Python?
    
**Answer:**

* Use the built-in `int()` function. Example:

    ```python
      s = "123"
      n = int(s)
      print(n + 10)  # 133
    ```

### 39. **Q:** What is `enumerate()` used for?
    
**Answer:**

* `enumerate(iterable, start=0)` returns pairs of (index, item) for items in `iterable`. Useful when you need item index and value.
* Example:

    ```python
      for idx, val in enumerate(["a","b","c"], start=1):
          print(idx, val)
      # 1 a
      # 2 b
      # 3 c
    ```

### 40. **Q:** What is the difference between `==` and `<`, `>`, etc., for strings in Python?
    
**Answer:**

    * `==` checks equality of two strings.
    * `<`, `>` compare lexicographically (based on character codes).
    * Example:

    ```python
      print("apple" < "banana")   # True
      print("Apple" < "apple")    # True (uppercase has lower ASCII)
    ```

### 41. **Q:** How do you open a file for writing and read from it in Python?
    
**Answer:**

    * Example:

    ```python
      # Writing
      with open("out.txt", "w") as f:
          f.write("Hello\n")

      # Reading
      with open("out.txt", "r") as f:
          contents = f.read()
          print(contents)
    ```

### 42. **Q:** What does `__repr__` vs `__str__` in a class mean?
    
**Answer:**

* `__str__(self)`: human-readable string representation of object (for `print(obj)`).
* `__repr__(self)`: unambiguous representation, ideally one that could recreate the object, used by `repr(obj)` or in interactive prompt.
* Example:

    ```python
      class Person:
          def __init__(self, name):
              self.name = name
          def __str__(self):
              return f"Person: {self.name}"
          def __repr__(self):
              return f"Person({self.name!r})"
      p = Person("Alice")
      print(p)         # Person: Alice
      print(repr(p))   # Person('Alice')
    ```

### 43. **Q:** What is docstring?
    
**Answer:**

* A docstring is a string literal placed at the beginning of a module, class, or function to describe what it does. It becomes the `__doc__` attribute.
* Example:

    ```python
      def add(a, b):
          """Return sum of a and b."""
          return a + b

      print(add.__doc__)  # “Return sum of a and b.”
    ```

### 44. **Q:** How do you check whether a key exists in a dictionary?
    
**Answer:**

* Use the `in` operator:

    ```python
      d = {"a":1, "b":2}
      if "a" in d:
          print("exists")
    ```

### 45. **Q:** What is the ‘slice’ step parameter? Example usage.
        
**Answer:**

* In `[start:stop:step]`, `step` is how many positions to jump. Example:

    ```python
      numbers = [0,1,2,3,4,5,6,7]
      print(numbers[1:7:2])   # [1,3,5]
      print(numbers[::-1])    # reversed list
    ```

### 46. **Q:** What is the `zip()` function used for?
    
**Answer:**

* `zip(*iterables)` combines elements from each iterable into tuples, stopping at the shortest. Example:

    ```python
      names = ["Alice","Bob","Carol"]
      ages  = [30, 25, 27]
      for name, age in zip(names, ages):
          print(name, age)
      # Alice 30
      # Bob 25
      # Carol 27
    ```

### 47. **Q:** How do you remove duplicates from a list while preserving order?
    
**Answer:**

* One approach:

    ```python
      seen = set()
      result = []
      for x in lst:
          if x not in seen:
              seen.add(x)
              result.append(x)
      # result is deduplicated list preserving order
    ```

### 48. **Q:** What does the `*args` and `**kwargs` syntax mean in function definitions?
    
**Answer:**

* `*args`: collects extra positional arguments into a tuple.
* `**kwargs`: collects extra keyword arguments into a dict.
* Example:

    ```python
      def func(a, b, *args, **kwargs):
          print(a, b)
          print(args)
          print(kwargs)

      func(1,2,3,4, x=5, y=6)
      # prints:
      # 1 2
      # (3,4)
      # {'x':5, 'y':6}
    ```

### 49. **Q:** How do you pick a random element from a list?
    
**Answer:**

* Use the `random` module:

    ```python
      import random
      lst = [1,2,3,4]
      print(random.choice(lst))
    ```

### 50. **Q:** What is list slicing vs indexing?
    
**Answer:**

* Indexing (`lst[i]`): returns single element at position i.
* Slicing (`lst[i:j]`): returns a new list with elements from i up to (but not including) j.
* Example:

    ```python
      lst = [10,20,30,40]
      print(lst[2])     # 30
      print(lst[1:3])   # [20,30]
    ```

---

## Intermediate Level

Here we dig a bit deeper: OOP, advanced built-ins, decorators, iterators, some algorithms, memory/ performance concerns.

### 51. **Q:** Explain multiple inheritance in Python and how method resolution order (MRO) works.
    
**Answer:**

    * Python supports multiple inheritance: a class can inherit from multiple base classes.
    * The Method Resolution Order (MRO) defines the order in which base classes are searched when looking up a method. In new-style classes (Python 3) it uses C3 linearization.
    * Example:

      ```python
      class A:
          def greet(self): print("A")

      class B(A):
          def greet(self): print("B")

      class C(A):
          def greet(self): print("C")

      class D(B, C):
          pass

      d = D()
      d.greet()  # prints "B", because B is searched before C
      print(D.mro())  # [D, B, C, A, object]
      ```
    * Key takeaway: MRO ensures a consistent and deterministic lookup order.

### 52. **Q:** What is the difference between shallow copy and deep copy? (again but in context)
    
**Answer:**

    * As answered previously: shallow copy copies the outer object, inner references still point to original. Deep copy copies the entire structure recursively.
    * Use when you want independent nested objects.
    * Example shown in beginner section.

### 53. **Q:** What is a decorator in Python? Provide an example.
    
**Answer:**

    * A decorator is a function that takes another function (or class) as input and returns a new function (or class) with added/modified behavior.
    * Example:

      ```python
      def my_decorator(func):
          def wrapper(*args, **kwargs):
              print("Before function call")
              result = func(*args, **kwargs)
              print("After function call")
              return result
          return wrapper

      @my_decorator
      def say_hello():
          print("Hello!")

      say_hello()
      # Output:
      # Before function call
      # Hello!
      # After function call
      ```

### 54. **Q:** What are iterators and iterable in Python?
    
**Answer:**

    * An **iterable** is an object you can obtain an iterator from (e.g., lists, tuples, sets, dicts).
    * An **iterator** is an object that implements `__next__()` and `__iter__()`; calling `next()` yields successive values, raises `StopIteration` when done.
    * Example:

      ```python
      lst = [1,2,3]
      it = iter(lst)
      print(next(it))  # 1
      print(next(it))  # 2
      print(next(it))  # 3
      # next(it) now raises StopIteration
      ```

### 55. **Q:** What is `yield` and how does it differ from `return`?
    
**Answer:**

    * `return` ends function execution and optionally sends back a value.
    * `yield` makes the function a generator: each time it yields, it suspends state and returns a value; next time it resumes after yield.
    * Example:

      ```python
      def count_up_to(n):
          i = 1
          while i <= n:
              yield i
              i += 1

      for num in count_up_to(3):
          print(num)  # 1,2,3
      ```

### 56. **Q:** Explain list vs generator comprehensions; differences in memory.
    
**Answer:**

    * List comprehension (`[x*x for x in range(n)]`) builds the entire list in memory.
    * Generator expression (`(x*x for x in range(n))`) returns a generator that yields items one at a time; uses less memory.
    * Example:

      ```python
      squares_list = [x*x for x in range(1000000)]
      # uses memory for all million squares

      squares_gen = (x*x for x in range(1000000))
      # memory footprint is small; yields one at a time
      ```

### 57. **Q:** What is an abstract base class (ABC) in Python?
    
**Answer:**

    * In module `abc`, you can define classes with `@abstractmethod` that cannot be instantiated unless abstract methods are overridden. Useful for interface‐like behavior.
    * Example:

      ```python
      from abc import ABC, abstractmethod

      class Shape(ABC):
          @abstractmethod
          def area(self):
              pass

      class Circle(Shape):
          def __init__(self, r):
              self.r = r
          def area(self):
              return 3.14 * self.r * self.r

      # s = Shape()  # Error
      c = Circle(5)
      print(c.area())  # 78.5
      ```

### 58. **Q:** How does Python’s memory management work? (heap, garbage collection)
    
**Answer:**

    * Python uses a private heap for all objects & data structures. The memory manager handles allocation. ([BrainStation][4])
    * There’s built-in garbage collection (GC) and reference counting: when an object’s reference count drops to zero, it can be reclaimed.
    * Example: cyclic references may require GC to clean up.

### 59. **Q:** What are `__slots__` in Python classes and when might you use them?
    
**Answer:**

    * `__slots__` is a class variable you define to restrict attribute creation to a fixed list and avoid per‐instance `__dict__`, reducing memory overhead when many instances exist.
    * Example:

      ```python
      class Point:
          __slots__ = ('x', 'y')
          def __init__(self, x, y):
              self.x = x
              self.y = y

      p = Point(1,2)
      # p.z = 10  # AttributeError
      ```

### 60. **Q:** Explain context managers and how you can create your own using `__enter__`, `__exit__`.
    
**Answer:**

    * A context manager defines `__enter__()` (called at block start) and `__exit__(exc_type, exc_val, exc_tb)` (called on exit). It can be used with `with` statement to manage resources.
    * Example:

      ```python
      class MyContext:
          def __enter__(self):
              print("Enter")
              return self
          def __exit__(self, exc_type, exc_val, exc_tb):
              print("Exit")

      with MyContext() as ctx:
          print("Inside")
      # Output:
      # Enter
      # Inside
      # Exit
      ```

### 61. **Q:** What is monkey-patching?
    
**Answer:**

    * Monkey‐patching refers to dynamically modifying classes or modules at runtime (adding methods, changing behavior). While powerful, it can be risky for maintainability. 
    * Example:

      ```python
      import math
      original_sqrt = math.sqrt
      math.sqrt = lambda x: 42
      print(math.sqrt(16))  # 42
      math.sqrt = original_sqrt  # restore
      ```

### 62. **Q:** Explain how you would implement a stack data structure in Python.
    
**Answer:**

    * Use a list (or `collections.deque`) to implement stack: `push` = `append`, `pop` = `pop()`.
    * Example:

      ```python
      class Stack:
          def __init__(self):
              self._items = []
          def push(self, item):
              self._items.append(item)
          def pop(self):
              if self._items:
                  return self._items.pop()
              raise IndexError("pop from empty stack")
          def peek(self):
              if self._items:
                  return self._items[-1]
              return None
          def is_empty(self):
              return not self._items
      ```

### 63. **Q:** Explain shallow vs deep copy again but in context of lists of dictionaries.
    
**Answer:**

    * Suppose you have `lst = [ {'a':1}, {'b':2} ]`.

      * A shallow copy `lst2 = lst.copy()` creates a new top‐level list but the dictionaries inside are the same objects. Modifying a dictionary in `lst2` modifies `lst`.
      * A deep copy (`import copy; lst3 = copy.deepcopy(lst)`) duplicates the dictionaries too, so modifications are independent.

### 64. **Q:** How do you sort a list of dictionaries by a given key?
    
**Answer:**

    * Use `sorted()` with `key=` parameter or list’s `sort()` method.
    * Example:

      ```python
      people = [
        {"name":"Alice","age":30},
        {"name":"Bob","age":25},
        {"name":"Carol","age":27}
      ]
      sorted_by_age = sorted(people, key=lambda x: x["age"])
      # [{'name':'Bob',...}, {'name':'Carol',...}, {'name':'Alice',...}]
      ```

### 65. **Q:** Explain the difference between `__new__` and `__init__` in class instantiation.
    
**Answer:**

    * `__new__(cls, ...)` is called to create (allocate) a new instance (before initialization). It returns the new instance (or subclass).
    * `__init__(self, ...)` initializes the instance after it’s created.
    * Usually you override `__new__` when subclassing immutable types (like `tuple`, `str`) or customizing instantiation.

### 66. **Q:** What is list slicing performance — is it O(n)?
    
**Answer:**

    * Yes, slicing a list (e.g., `lst[1:1000]`) creates a new list and copies elements, so it’s O(k) where k = size of slice.
    * Important for performance when doing many or large slices.

### 67. **Q:** How do Python’s built-in `sort()` and `sorted()` functions work internally (algorithm)?
    
**Answer:**

    * Python (CPython) uses Timsort (a hybrid stable sorting algorithm derived from merge sort and insertion sort) for list sorting since Python 2.3. ([Wikipedia][5])
    * It is O(n log n) worst-case, and takes advantage of existing runs (already sorted subsequences) to accelerate for nearly‐sorted input.

### 68. **Q:** What is the Global Interpreter Lock (GIL) in Python?
    
**Answer:**

    * The GIL is a mutex that allows only one native thread to execute Python bytecode at a time in CPython.
    * It means multi-threading may not scale CPU‐bound workloads; you may use multiprocessing or external libraries releasing the GIL for concurrency. 

### 69. **Q:** How do you implement caching in Python (memoization) for a recursive function?
    
**Answer:**

    * Use dictionary to store previously computed results (manual) or use `functools.lru_cache`.
    * Example:

      ```python
      from functools import lru_cache

      @lru_cache(maxsize=None)
      def fib(n):
          if n < 2:
              return n
          return fib(n-1) + fib(n-2)

      print(fib(50))  # fast, thanks to caching
      ```

### 70. **Q:** What is the difference between `__call__()` and normal methods?
    
**Answer:**

    * If a class defines `__call__(self, *args, **kwargs)`, its instances become callable like functions.
    * Example:

      ```python
      class Adder:
          def __init__(self, n):
              self.n = n
          def __call__(self, x):
              return self.n + x

      add5 = Adder(5)
      print(add5(10))  # 15
      ```

### 71. **Q:** Explain how to merge two sorted lists into one sorted list (algorithmically).
    
**Answer:**

    * Use two pointers i, j starting at list1[0], list2[0], compare and copy smaller into result, advance pointer; when one list ends, copy remainder.
    * Example:

      ```python
      def merge(a, b):
          i = j = 0
          result = []
          while i < len(a) and j < len(b):
              if a[i] <= b[j]:
                  result.append(a[i]); i+=1
              else:
                  result.append(b[j]); j+=1
          # copy leftovers
          result.extend(a[i:])
          result.extend(b[j:])
          return result
      ```

### 72. **Q:** What is the difference between `__getitem__`, `__iter__`, `__next__` in custom classes?
    
**Answer:**

    * `__getitem__(self, key)`: allows indexing `obj[key]`.
    * `__iter__(self)`: returns an iterator (typically `self`).
    * `__next__(self)`: defines next item in iterator; raises `StopIteration`.
    * Example:

      ```python
      class CountTo:
          def __init__(self, n):
              self.n = n
              self.i = 0
          def __iter__(self):
              return self
          def __next__(self):
              if self.i >= self.n:
                  raise StopIteration
              self.i += 1
              return self.i

      for num in CountTo(3):
          print(num)  # 1,2,3
      ```

### 73. **Q:** How does Python’s garbage collector handle cyclic references?
    
**Answer:**

    * Python uses reference counting for immediate deallocation of objects when count drops to zero. However, reference counting cannot clean up objects involved in cycles (A→B→A).
    * Therefore, the garbage collector periodically examines object generations to find cycles and free them.
    * Important for memory management when objects reference each other.

### 74. **Q:** What is the `__eq__` method in a class? How do you define it?
    
**Answer:**

    * `__eq__(self, other)` defines behavior for `self == other`. You can override it to compare objects meaningfully.
    * Example:

      ```python
      class Point:
          def __init__(self, x, y):
              self.x = x
              self.y = y
          def __eq__(self, other):
              if isinstance(other, Point):
                  return self.x == other.x and self.y == other.y
              return False

      p1 = Point(1,2)
      p2 = Point(1,2)
      print(p1 == p2)  # True
      ```

### 75. **Q:** Explain difference between `@property` decorator vs normal method getter.
    
**Answer:**

    * `@property` allows you to access method as attribute (for read-only or computed attributes) instead of calling it.
    * Example:

      ```python
      class Rectangle:
          def __init__(self, width, height):
              self.width = width
              self.height = height

          @property
          def area(self):
              return self.width * self.height

      r = Rectangle(3,4)
      print(r.area)   # 12  (no parentheses)
      ```

### 76. **Q:** How would you profile a Python program’s performance (time/memory)?
    
**Answer:**

    * Use modules like `cProfile` (for time), `timeit` (small code snippets), `memory_profiler` or `tracemalloc` (for memory).
    * Example:

      ```bash
      python -m cProfile myscript.py
      ```

### 77. **Q:** What are metaclasses in Python, and when might you use them?
    
**Answer:**

    * A metaclass is a “class of a class”; it defines how classes behave (how they are constructed).
    * You specify `metaclass=MyMeta` in class definition.
    * Use cases: logging class creation, enforcing coding rules, automatically registering subclasses.
    * Example:

      ```python
      class Meta(type):
          def __new__(cls, name, bases, attrs):
              print(f"Creating class {name}")
              return super().__new__(cls, name, bases, attrs)

      class MyClass(metaclass=Meta):
          pass

      # Output: “Creating class MyClass”
      ```

### 78. **Q:** Explain coroutine vs generator in Python.
    
**Answer:**

    * Generators yield values and can be iterated.
    * Coroutines (with `async def` / `await`) are for asynchronous execution; they don’t just produce a sequence—they await events, perform non-blocking I/O, etc.
    * Example:

      ```python
      async def fetch(url):
          data = await some_async_io(url)
          return data
      ```

### 79. **Q:** What is the difference between `__init__.py` and namespace packages?
    
**Answer:**

    * Historically, a folder with `__init__.py` is treated as a Python package.
    * Since Python 3.3+, you can have namespace packages (folders without `__init__.py`) where the directories are still packages.
    * Useful for large modular codebases spanning multiple directories.

### 80. **Q:** How would you implement LRU (Least Recently Used) cache in Python?
    
**Answer:**

    * Use `collections.OrderedDict` (Python 3.7+ dict preserves insertion order) or `functools.lru_cache`.
    * Example custom:

      ```python
      from collections import OrderedDict

      class LRUCache:
          def __init__(self, capacity):
              self.cache = OrderedDict()
              self.capacity = capacity
          def get(self, key):
              if key not in self.cache:
                  return -1
              value = self.cache.pop(key)
              self.cache[key] = value  # mark as recently used
              return value
          def put(self, key, value):
              if key in self.cache:
                  self.cache.pop(key)
              elif len(self.cache) >= self.capacity:
                  self.cache.popitem(last=False)  # least recently used
              self.cache[key] = value
      ```

### 81. **Q:** What is the `__slots__` property and when is it used? (covered earlier)
    
**Answer:**

    * Already explained in Q59.

### 82. **Q:** Explain the difference between `==` and `is` again but with immutable caching (e.g., small integers).
    
**Answer:**

    * For small immutable integers (-5 to 256 in CPython by default), Python caches objects, so `a is b` may be `True`.
    * Example:

      ```python
      a = 100
      b = 100
      print(a is b)  # True (because cached)

      a = 1000
      b = 1000
      print(a is b)  # Often False (not guaranteed)
      ```

### 83. **Q:** How do you handle file not found error gracefully?
    
**Answer:**

    * Use `try-except FileNotFoundError:`.
    * Example:

      ```python
      try:
          with open("nonexistent.txt","r") as f:
              data = f.read()
      except FileNotFoundError:
          print("File not found.")
      ```

### 84. **Q:** What does `__dict__` attribute of an object represent?
    
**Answer:**

    * It’s a dictionary (if available) storing an object’s (writable) attributes.
    * Example:

      ```python
      class A:
          def __init__(self):
              self.x = 10
              self.y = 20

      a = A()
      print(a.__dict__)  # {'x':10,'y':20}
      ```

### 85. **Q:** What is monkey patching again? (covered earlier)
    
**Answer:**

    * Already explained in Q61.

### 86. **Q:** Describe how you would traverse a directory and its subdirectories in Python.
    
**Answer:**

    * Use the `os.walk()` function.
    * Example:

      ```python
      import os
      for dirpath, dirnames, filenames in os.walk("/path/to/dir"):
          for fname in filenames:
              fullpath = os.path.join(dirpath, fname)
              print(fullpath)
      ```

### 87. **Q:** Explain the difference between `__repr__` and `__str__` (covered already).
    
**Answer:**

    * Already answered in Q42.

### 88. **Q:** What is the use of the `bisect` module?
    
**Answer:**

    * The `bisect` module supports binary search and insertion in sorted lists. Good for keeping a list sorted with minimal overhead.
    * Example:

      ```python
      import bisect
      lst = [1,3,4,7]
      bisect.insort(lst,5)
      print(lst)  # [1,3,4,5,7]
      idx = bisect.bisect(lst, 4)
      print(idx)  # position to insert 4 to keep sorted
      ```

### 89. **Q:** How do you handle command-line arguments in Python?
    
**Answer:**

    * Use `sys.argv` for low-level; or `argparse` module for structured argument parsing.
    * Example:

      ```python
      import argparse
      parser = argparse.ArgumentParser(description="My program")
      parser.add_argument("--verbose", action="store_true")
      parser.add_argument("filename")
      args = parser.parse_args()
      print(args.verbose, args.filename)
      ```

### 90. **Q:** Explain how list growth works in Python (memory amortisation).
    
**Answer:**

    * Python lists over-allocate space to amortise append operations. When capacity is exceeded, they allocate more space than immediately needed (often ~50% more) to reduce frequent reallocations.
    * So `append()` is amortised O(1), though occasional O(n) when resizing. This is important for performance.

### 91. **Q:** What’s the difference between `__init__` and `__del__` in a class?
    
**Answer:**

    * `__init__(self,…)`: initializer called after object creation.
    * `__del__(self)`: destructor method, called when object is about to be destroyed (via GC). But reliance on it is discouraged because destruction timing is not guaranteed.
    * Example:

      ```python
      class A:
          def __init__(self):
              print("init")
          def __del__(self):
              print("del")

      a = A()
      del a
      # “init” printed, maybe “del” printed immediately or later when GC collects
      ```

### 92. **Q:** How do you implement a priority queue in Python?
    
**Answer:**

    * Use `heapq` module which implements a binary heap.
    * Example:

      ```python
      import heapq
      heap = []
      heapq.heappush(heap, (2, "low priority"))
      heapq.heappush(heap, (1, "high priority"))
      priority, task = heapq.heappop(heap)
      print(task)  # "high priority"
      ```

### 93. **Q:** What is “duck typing” in Python?
    
**Answer:**

    * Duck typing: “If it quacks like a duck, it is a duck”. Instead of checking type, you check for presence of methods/attributes.
    * Example:

      ```python
      class Duck:
          def quack(self): print("Quack!")

      class Person:
          def quack(self): print("Person pretending to quack")

      def make_it_quack(thing):
          thing.quack()

      make_it_quack(Duck())
      make_it_quack(Person())
      ```
    
### 94. **Q:** What is `__call__` method use case? (covered in Q70)
    
**Answer:**

    * See Q70.

### 95. **Q:** How would you implement a simple linked list in Python?
    
**Answer:**

    ```python
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    class LinkedList:
        def __init__(self):
            self.head = None

        def append(self, value):
            node = Node(value)
            if not self.head:
                self.head = node
                return
            current = self.head
            while current.next:
                current = current.next
            current.next = node

        def __iter__(self):
            current = self.head
            while current:
                yield current.value
                current = current.next

    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    for val in ll:
        print(val)  # 10, 20
    ```

### 96. **Q:** What is the difference between `__init__` and `__new__`? (covered earlier)
    
**Answer:**

    * See Q65.

### 97. **Q:** Explain how a Python dictionary is implemented under the hood (at a high level).
    
**Answer:**

    * Python dictionaries are hash tables: each key is hashed; buckets store key,value pairs; on lookup the hash is computed, bucket found, then equality test. They are dynamically resized as load factor increases.
    * This gives average O(1) lookup, insertion. Knowing hashing helps understand collisions, performance issues.

### 98. **Q:** How do you reverse a string in Python?
    
**Answer:**

    * Easiest way: slicing with step -1: `s[::-1]`. Example:

      ```python
      s = "hello"
      rev = s[::-1]
      print(rev)  # “olleh”
      ```

### 99. **Q:** What is the difference between `__repr__` and `__str__`? (covered earlier)
    
**Answer:**

    * See Q42.

### 100. **Q:** How do you merge dictionaries in Python 3.9+?
     
**Answer:**

     * Use the `|` (pipe) operator:

       ```python
       d1 = {"a":1, "b":2}
       d2 = {"b":3, "c":4}
       merged = d1 | d2    # {"a":1, "b":3, "c":4}
       ```
     * Or use `dict1.update(dict2)` to update in-place.

---

## Advanced Level

Topics include concurrency, async, metaprogramming, memory/patterns, algorithms, design, performance tuning.

### 101. **Q:** What is the difference between threading and multiprocessing in Python?
     
**Answer:**

     * **Threading**: uses threads within the same process; due to the GIL in CPython, only one thread executes Python bytecode at a time; good for I/O-bound tasks.
     * **Multiprocessing**: uses separate processes each with its own memory space; bypasses GIL; better for CPU-bound tasks.
     * Example:

       ```python
       import threading, multiprocessing

       def io_task():
           # simulate I/O
           pass

       def cpu_task():
           # heavy computation
           pass

       # Use threading for io_task; multiprocessing for cpu_task
       ```

### 102. **Q:** Explain async/await in Python; what does `asyncio` provide?
     
**Answer:**

     * `async def` defines coroutine functions. Calling them returns coroutine objects which must be awaited with `await` inside another coroutine, or run via event loop.
     * `asyncio` module provides event loop, tasks, futures, asynchronous I/O abstractions.
     * Example:

       ```python
       import asyncio

       async def say_hello():
           await asyncio.sleep(1)
           print("Hello after 1 second")

       asyncio.run(say_hello())
       ```

### 103. **Q:** What is the `multiprocessing.Pool` and how does it differ from `concurrent.futures.ProcessPoolExecutor`?
     
**Answer:**

     * `multiprocessing.Pool`: map, apply, etc for processes.
     * `concurrent.futures.ProcessPoolExecutor`: high‐level interface with futures (submit(), map()). Choice depends on API familiarity, features such as callback.
     * Example:

       ```python
       from concurrent.futures import ProcessPoolExecutor

       def f(x):
           return x*x

       with ProcessPoolExecutor() as exe:
           results = list(exe.map(f, [1,2,3,4]))
       ```

### 104. **Q:** How would you implement a thread-safe singleton in Python?
     
**Answer:**

     ```python
     import threading

     class Singleton:
         _instance = None
         _lock = threading.Lock()

         def __new__(cls, *args, **kwargs):
             if not cls._instance:
                 with cls._lock:
                     if not cls._instance:
                         cls._instance = super().__new__(cls)
             return cls._instance

     s1 = Singleton()
     s2 = Singleton()
     print(s1 is s2)  # True
     ```

### 105. **Q:** What is the `async def __aenter__` / `__aexit__` pair used for?
     
**Answer:**

     * In asynchronous context managers, you define `__aenter__(self)` and `__aexit__(self, exc_type, exc, tb)` to be used with `async with`.
     * Example:

       ```python
       class AsyncContext:
           async def __aenter__(self):
               print("Async enter")
               return self
           async def __aexit__(self, exc_type, exc, tb):
               print("Async exit")

       async def main():
           async with AsyncContext() as ctx:
               print("Inside")

       import asyncio
       asyncio.run(main())
       ```

### 106. **Q:** What is a memory leak in Python? How can it happen?
     
**Answer:**

     * Although Python has GC, memory leaks can occur if references are held inadvertently (cached objects, global lists, closures capturing large objects, circular references with `__del__`, etc.).
     * Example:

       ```python
       cache = {}
       def process(item):
           cache[item.id] = item   # never freed -> leak
       ```

### 107. **Q:** Explain the concept of “weak references” (`weakref`) and when you might use them.
     
**Answer:**

     * The `weakref` module allows creation of references to objects that do not increase their reference count—so object can be garbage-collected when only weak references remain.
     * Use case: caching objects but don't want to prevent their garbage collection when unused.
     * Example:

       ```python
       import weakref

       class MyObj:
           pass

       obj = MyObj()
       r = weakref.ref(obj)
       print(r())  # <MyObj>
       del obj
       print(r())  # None (object collected)
       ```

### 108. **Q:** How do you use the `multiprocessing.Manager` in Python?
     
**Answer:**

     * `Manager()` returns a server process that can hold Python objects shared between processes (dicts, lists) safely.
     * Example:

       ```python
       from multiprocessing import Process, Manager

       def worker(d, key, value):
           d[key] = value

       if __name__ == "__main__":
           manager = Manager()
           shared_dict = manager.dict()
           p = Process(target=worker, args=(shared_dict, "x", 100))
           p.start()
           p.join()
           print(shared_dict["x"])  # 100
       ```

### 109. **Q:** How would you detect and handle deadlocks in Python multi­threaded code?
     
**Answer:**

     * Use tools: ensure acquiring locks in consistent order; use `threading.Lock.acquire(timeout=…)`; use higher level concurrency primitives (`Queue`, `Condition`, `Semaphore`); analysis tools for detecting blocking; avoid holding locks across I/O.
     * Example: two threads each holding one lock and waiting for the other → deadlock.

### 110. **Q:** Explain how you would profile memory usage of a Python object over time.
     
**Answer:**

     * Use `tracemalloc` (Python 3.4+) to track memory allocations; use `objgraph` to visualize object graphs; periodically snapshot memory and compare.
     * Example:

       ```python
       import tracemalloc
       tracemalloc.start()
       # run code
       snapshot = tracemalloc.take_snapshot()
       top_stats = snapshot.statistics('lineno')
       for stat in top_stats[:10]:
           print(stat)
       ```

### 111. **Q:** What is `metaclass` usage in dynamic class creation? (similar to earlier)
     
**Answer:**

     * See Q77.

112. **Q:** What are descriptors in Python (i.e., `__get__`, `__set__`, `__delete__`)?
     
**Answer:**

     * A descriptor is an object attribute with “binding behavior”: when attribute access occurs, its descriptor methods are invoked. Descriptors are used to implement e.g. properties, methods, static methods.
     * Example:

       ```python
       class Descriptor:
           def __get__(self, instance, owner):
               print("Getting value")
               return instance._value
           def __set__(self, instance, value):
               print("Setting value")
               instance._value = value

       class MyClass:
           attr = Descriptor()
           def __init__(self, value):
               self._value = value

       m = MyClass(10)
       print(m.attr)   # Getting value -> 10
       m.attr = 20     # Setting value
       print(m.attr)   # Getting value -> 20
       ```

### 113. **Q:** Explain how you would implement your own iterator class (with `__iter__`, `__next__`). (covered in Q72)
     
**Answer:**

     * See Q72.

114. **Q:** What is a closure in Python? Provide an example.
     
**Answer:**

     * A closure is when a nested function remembers values from its enclosing lexical scope even after the outer function has finished execution.
     * Example:

       ```python
       def make_multiplier(n):
           def multiplier(x):
               return x * n
           return multiplier

       times3 = make_multiplier(3)
       print(times3(10))  # 30
       ```

115. **Q:** What is the difference between synchronous and asynchronous code in Python?
     
**Answer:**

     * Synchronous: tasks execute one after the other; each task may block.
     * Asynchronous: tasks may yield control (via `await`, `asyncio`) allowing other tasks to run while waiting (for I/O etc).
     * Example: reading multiple network endpoints concurrently via `asyncio.gather`.

### 116. **Q:** How would you implement a trie (prefix tree) in Python?
     
**Answer:**

     ```python
     class TrieNode:
         def __init__(self):
             self.children = {}
             self.is_end = False

     class Trie:
         def __init__(self):
             self.root = TrieNode()

         def insert(self, word):
             node = self.root
             for ch in word:
                 node = node.children.setdefault(ch, TrieNode())
             node.is_end = True

         def search(self, word):
             node = self.root
             for ch in word:
                 if ch not in node.children:
                     return False
                 node = node.children[ch]
             return node.is_end

     trie = Trie()
     trie.insert("hello")
     print(trie.search("hell"))  # False
     print(trie.search("hello")) # True
     ```

### 117. **Q:** Explain context switching overhead in Python threads; why might you choose processes instead?
     
**Answer:**

     * Thread context switching still consumes CPU and suffers from GIL contention in CPython; many threads still blocked waiting; for CPU-bound tasks threads don’t gain much due to GIL.
     * Processes each have separate GIL and memory space; true parallelism on multi-core; overhead higher (IPCs), but for heavy tasks beneficial.

### 118. **Q:** What is the `subprocess` module for, and how does it compare to `os.system`?
     
**Answer:**

     * `subprocess` gives fine‐grained control over spawning new processes, reading/writing their input/output/error streams, capturing return codes, avoiding shell injection.
     * `os.system` is simpler but less flexible and may be vulnerable to shell injection.
     * Example:

       ```python
       import subprocess
       result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
       print(result.stdout)
       ```

### 119. **Q:** How do you implement a thread pool (or process pool) in Python and when would you use one?
     
**Answer:**

     * Use `concurrent.futures.ThreadPoolExecutor` or `ProcessPoolExecutor`.
     * Use thread pool for I/O‐bound tasks; process pool for CPU-bound.
     * Example:

       ```python
       from concurrent.futures import ThreadPoolExecutor

       def task(x):
           return x*x

       with ThreadPoolExecutor(max_workers=5) as executor:
           results = list(executor.map(task, [1,2,3,4,5]))
       print(results)  # [1,4,9,16,25]
       ```

### 120. **Q:** What is the difference between “weakref” and normal references? (covered in Q107)
     
**Answer:**

     * See Q107.

### 121. **Q:** Explain how you would build a REST API in Python (frameworks, best practices).
     
**Answer:**

     * Use frameworks like `Flask` or `FastAPI`, define endpoints, use request/response, JSON serialization, proper HTTP status codes, use dependency injection (FastAPI), input validation, authentication.
     * Example (Flask):

       ```python
       from flask import Flask, request, jsonify

       app = Flask(__name__)

       @app.route("/items/<int:item_id>", methods=["GET"])
       def get_item(item_id):
           # fetch item from database
           return jsonify({"id": item_id, "name": "ItemName"})

       if __name__ == "__main__":
           app.run(debug=True)
       ```

### 122. **Q:** How do you handle migrations in a Python web application (e.g., Django)?
     
**Answer:**

     * In Django: use `makemigrations` to auto-generate migration files for model changes, then `migrate` to apply them.
     * Best practices: back up data, test migrations, use version control, handle data migrations if needed.

### 123. **Q:** Explain the difference between `asyncio.Task` and `concurrent.futures.Future`.
     
**Answer:**

     * `asyncio.Task`: wraps a coroutine, scheduled on event loop; can be awaited.
     * `concurrent.futures.Future`: returned by `ThreadPoolExecutor` or `ProcessPoolExecutor`; represents pending result from thread/process.
     * Both represent asynchronous results, but in different concurrency models (async I/O vs thread/process).

### 124. **Q:** What are memory views (`memoryview`) in Python and why use them?
     
**Answer:**

     * `memoryview` is a built‐in type that allows access to the memory of another binary object (bytes, bytearray) without copying. Useful for large binary data, slicing without copy.
     * Example:

       ```python
       b = bytearray(b"hello world")
       mv = memoryview(b)
       mv[0:5] = b"HELLO"
       print(b)  # bytearray(b"HELLO world")
       ```

### 125. **Q:** How does `pickle` differ from `json` when serializing Python objects?
     
**Answer:**

     * `json` serializes to text format of simple types (strings, numbers, lists, dicts) and is cross‐language, human‐readable; cannot handle arbitrary Python objects out of box.
     * `pickle` serializes and deserializes arbitrary Python objects (including classes, functions), but is Python‐specific and not secure for untrusted data.
     * Example:

       ```python
       import pickle, json
       data = {"a":1, "b":2}
       s1 = json.dumps(data)
       s2 = pickle.dumps(data)
       ```

### 126. **Q:** What is the difference between `@staticmethod` and `@classmethod`? (covered earlier)
     
**Answer:**

     * See Q29 and Q30.

### 127. **Q:** Describe how to implement a plugin architecture in Python.
     
**Answer:**

     * Use dynamic imports, registries, entry points (via `setuptools`), classes/interfaces.
     * For example, use `pkg_resources.iter_entry_points('myapp.plugins')` and load plugin classes dynamically.
     * Provide interface (abstract base class) for plugin, allow external modules to register via setup.py entry points.

### 128. **Q:** How do you ensure backward compatibility in a Python library?
     
**Answer:**

     * Use semantic versioning; maintain hierarchy of versions; deprecate features rather than remove; use warnings (`import warnings; warnings.warn(...)`); write tests against older versions; maintain clear changelog; ensure code works under older Python interpreters if supported.

### 129. **Q:** What is a “metaprogramming” technique in Python (one example)?
     
**Answer:**

     * Metaprogramming: writing code that manipulates code (classes/functions) at runtime. Example: using `type()` to dynamically create classes, or decorators that generate classes, or modifying `__class__` of object.
     * Example:

       ```python
       MyDynamicClass = type("MyDynamicClass", (object,), {"greet": lambda self: print("Hi")})
       obj = MyDynamicClass()
       obj.greet()  # “Hi”
       ```

### 130. **Q:** Explain the “Descriptor protocol” (covered in Q112).
     
**Answer:**

     * See Q112.

### 131. **Q:** How would you implement bulk asynchronous HTTP requests in Python?
     
**Answer:**

     * Use `aiohttp` (async HTTP client) + `asyncio.gather`.
     * Example:

       ```python
       import aiohttp, asyncio

       async def fetch(session, url):
           async with session.get(url) as resp:
               return await resp.text()

       async def main(urls):
           async with aiohttp.ClientSession() as session:
               tasks = [fetch(session, url) for url in urls]
               return await asyncio.gather(*tasks)

       urls = ["http://example.com"]*5
       results = asyncio.run(main(urls))
       ```

### 132. **Q:** Explain how to write thread‐safe code when sharing mutable data between threads.
     
**Answer:**

     * Use locks (`threading.Lock()`), `threading.RLock()`, `Queue` for safe producer/consumer, avoid shared mutable state when possible, use immutable objects or copy on write.
     * Example:

       ```python
       import threading

       counter = 0
       lock = threading.Lock()

       def increment():
           global counter
           with lock:
               temp = counter
               temp += 1
               counter = temp

       threads = [threading.Thread(target=increment) for _ in range(1000)]
       for t in threads: t.start()
       for t in threads: t.join()
       print(counter)  # deterministic
       ```

### 133. **Q:** How do you implement a “factory” pattern in Python?
     
**Answer:**

     * A factory returns instances of classes based on input parameter.
     * Example:

       ```python
       class Shape:
           pass

       class Circle(Shape):
           pass

       class Square(Shape):
           pass

       def shape_factory(shape_type):
           if shape_type == "circle":
               return Circle()
           elif shape_type == "square":
               return Square()
           else:
               raise ValueError("Unknown shape")

       s = shape_factory("circle")
       ```

### 134. **Q:** Explain how to manage dependencies in a large Python project.
     
**Answer:**

     * Use virtual environments (`venv`, `conda`), `requirements.txt` or `Pipfile`/`poetry`, pin versions, use CI to test on multiple python versions, use dependency injection, avoid global state.
     * Employ modules, packages, and keep code modular.

### 135. **Q:** How would you implement a decorator that takes arguments?
     
**Answer:**

     ```python
     def repeat(n):
         def decorator(func):
             def wrapper(*args, **kwargs):
                 for _ in range(n):
                     func(*args, **kwargs)
             return wrapper
         return decorator

     @repeat(3)
     def greet(name):
         print(f"Hello {name}")

     greet("Alice")
     # prints “Hello Alice” three times
     ```

### 136. **Q:** Explain how you would make Python objects picklable (i.e., suitable for serialization).
     
**Answer:**

     * Ensure that class is defined at top level (not nested); avoid unpickleable attributes (open file handles, sockets); implement `__getstate__`/`__setstate__` if needed; or use `copyreg` to register reduction.
     * Example:

       ```python
       import pickle

       class MyObj:
           def __init__(self, x):
               self.x = x

       obj = MyObj(10)
       data = pickle.dumps(obj)
       new_obj = pickle.loads(data)
       ```

### 137. **Q:** What is `__sizeof__()` method of object and how can you use it?
     
**Answer:**

     * `object.__sizeof__()` returns the memory size in bytes of the object (not including referents). For full memory footprint you may use `sys.getsizeof()` plus sum of sizes of referenced objects.
     * Example:

       ```python
       import sys
       lst = [1,2,3]
       print(sys.getsizeof(lst))
       ```

### 138. **Q:** How do you implement dynamic attribute access (e.g., `__getattr__`, `__setattr__`)?
     
**Answer:**

     * `__getattr__(self, name)`: called when attribute `name` not found via normal lookup.
     * `__setattr__(self, name, value)`: called for all attribute assignments (careful to avoid infinite recursion).
     * Example:

       ```python
       class Magic:
           def __getattr__(self, name):
               return f"No attribute {name}"
           def __setattr__(self, name, value):
               object.__setattr__(self, name, value)

       m = Magic()
       print(m.unknown)  # “No attribute unknown”
       m.x = 10
       print(m.x)        # 10
       ```

### 139. **Q:** Explain how you would perform A/B testing instrumentation in a Python web app.
     
**Answer:**

     * Design: randomize users into groups (A/B), log group assignment, track key metrics, ensure no bias.
     * Implementation: e.g., middleware that assigns `variant = hash(user_id) % 2`, injects UI variation; log to analytics or internal DB; evaluate after sufficient sample size.
     * Use feature flags, rollback capability, monitor statistical significance.

### 140. **Q:** What is “metaclass plumbing” – e.g., customizing class creation by overriding `__prepare__`, `__new__` of metaclass?
     
**Answer:**

     * `__prepare__(metacls, name, bases, **kwargs)` returns namespace used to build class body (e.g., order‐preserving dict).
     * `__new__` of metaclass can modify class attributes, attach metadata, enforce rules.
     * Example:

       ```python
       class OrderedMeta(type):
           @classmethod
           def __prepare__(metacls, name, bases):
               from collections import OrderedDict
               return OrderedDict()
           def __new__(cls, name, bases, attrs):
               print("Attributes defined in:", list(attrs.keys()))
               return super().__new__(cls, name, bases, dict(attrs))

       class My(metaclass=OrderedMeta):
           x = 1
           y = 2
           def method(self): pass
       ```

### 141. **Q:** How do you optimize Python code for speed? (e.g., using built-ins, avoid globals, etc)
     
**Answer:**

     * Use built-ins and library functions (written in C) rather than pure Python loops.
     * Minimise attribute lookups by local references.
     * Use list comprehensions, generator expressions.
     * Avoid global variables (they’re slower to access).
     * Use profiling (`cProfile`) to identify hotspots.
     * Example: replacing manual sum loop with `sum()`.

### 142. **Q:** Explain how CPython implements small integer caching and how that can affect `is` operator results. (covered earlier)
     
**Answer:**

     * See Q82.

### 143. **Q:** How would you implement a read-only attribute in a class?
     
**Answer:**

     * Use `@property` without setter.
     * Example:

       ```python
       class My:
           def __init__(self, x):
               self._x = x
           @property
           def x(self):
               return self._x

       m = My(10)
       print(m.x)    # 10
       # m.x = 20    # AttributeError
       ```

### 144. **Q:** What’s the difference between `copy.copy()` and slicing for lists (`lst[:]`)?
     
**Answer:**

     * `lst[:]` creates a shallow copy of list. Equivalent to `list(lst)` or `lst.copy()`.
     * But `copy.copy()` is generic and works for other objects too.
     * Example:

       ```python
       import copy
       lst = [1,2,3]
       a = lst[:]        # shallow copy
       b = copy.copy(lst)
       ```

### 145. **Q:** Explain how to implement a decorator that caches results with a max size (LRU cache) yourself (without using `functools.lru_cache`).
     
**Answer:**

     ```python
     from collections import OrderedDict
     def lru_cache(maxsize=128):
         def decorator(func):
             cache = OrderedDict()
             def wrapper(*args):
                 if args in cache:
                     cache.move_to_end(args)
                     return cache[args]
                 result = func(*args)
                 cache[args] = result
                 if len(cache) > maxsize:
                     cache.popitem(last=False)
                 return result
             return wrapper
         return decorator

     @lru_cache(32)
     def fib(n):
         if n < 2:
             return n
         return fib(n-1) + fib(n-2)
     ```

### 146. **Q:** What is the `@dataclass` decorator (Python 3.7+)? How is it helpful?
     
**Answer:**

     * The `@dataclass` decorator automatically generates special methods like `__init__`, `__repr__`, `__eq__`, etc., for classes that primarily store data.
     * Example:

       ```python
       from dataclasses import dataclass

       @dataclass
       class Point:
           x: int
           y: int

       p = Point(3,4)
       print(p)  # Point(x=3, y=4)
       ```

### 147. **Q:** Explain the difference between `isinstance()` and `issubclass()`.
     
**Answer:**

     * `isinstance(obj, Class)` checks if `obj` is an instance of `Class` or any subclass.
     * `issubclass(Cls, Class)` checks whether `Cls` is a subclass of `Class`.

### 148. **Q:** What are memory leaks in context of C extension modules with Python?
     
**Answer:**

     * If you write C extension modules (via `PyObject_New`, etc), you must handle reference counts properly. Failure to `Py_DECREF()` when needed can lead to memory leaks even if Python GC runs.
     * Also, if you create cycles involving C‐level objects not visible to Python’s GC, they may not be cleaned.

### 149. **Q:** Explain the “visitor pattern” and how you might implement it in Python.
     
**Answer:**

     * The visitor pattern separates algorithms from the objects on which they operate. You define a `visit` method for each concrete element type.
     * Example:

       ```python
       class Visitor:
           def visit(self, obj):
               method_name = 'visit_' + obj.__class__.__name__
               visitor = getattr(self, method_name, self.generic_visit)
               return visitor(obj)
           def generic_visit(self, obj):
               raise NotImplementedError

       class ElementA:
           pass

       class ConcreteVisitor(Visitor):
           def visit_ElementA(self, obj):
               print("Visiting ElementA")

       v = ConcreteVisitor()
       v.visit(ElementA())
       ```

### 150. **Q:** How do you implement dependency injection in Python?
     
**Answer:**

     * Inject dependencies via constructor or via setter arguments instead of hard‐coding inside class. Use interfaces (abstract base classes) so implementation can vary.
     * Example:

       ```python
       class Database:
           def query(self):
               pass

       class RealDatabase(Database):
           def query(self):
               return "real data"

       class Service:
           def __init__(self, db: Database):
               self.db = db
           def get_data(self):
               return self.db.query()

       service = Service(RealDatabase())
       print(service.get_data())
       ```

---
---

### 🔗 References
[1]: https://www.datacamp.com/blog/top-python-interview-questions-and-answers?utm_source=chatgpt.com "The 36 Top Python Interview Questions & Answers For 2025"
[2]: https://www.interviewbit.com/python-interview-questions/?utm_source=chatgpt.com "Top Python Interview Questions and Answers (2025) - InterviewBit"
[3]: https://www.geeksforgeeks.org/python-interview-questions/?utm_source=chatgpt.com "Python Interview Questions and Answers - GeeksforGeeks"
[4]: https://brainstation.io/career-guides/python-developer-interview-questions?utm_source=chatgpt.com "Python Developer Interview Questions (2025 Guide) - BrainStation"
[5]: https://en.wikipedia.org/wiki/Tim_Peters_%28software_engineer%29?utm_source=chatgpt.com "Tim Peters (software engineer)"
