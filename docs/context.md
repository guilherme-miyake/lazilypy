# Generic Lazy Evaluation
## Solving multiple clients, credentials and contexts on large script sets

## Problem definition

Whenever there are many third-party clients/objects on a set of scripts, I usually face one or more of the following problems
* duplication of initialization code
e.g: many scripts with the same initialization
* unintended deviation initialization code
e.g: someone forgot to update one of the scripts
* large initialization costs, sometimes beyond code execution itself
e.g: getting local credentials for a service/client that is not used in any of the scripts that will be run in this context by this user
* larger boilerplate code, more code to write and maintain
e.g: a whole new class with new initialization methods
* complex initialization code, harder to understand how/what/when its doing
e.g: dependency injection, middlewares, getters/setters, class or singleton properties cached or not
* worse developer experience
e.g: getting tired of writing boilerplate, or not being sure how to handle the situation, or not understanding exactly what is happening

## Simple and usual solutions in plain Python (IMHO)

* Approach 1: have a method/property to build and return the client on use

```python
class Context:
    @cached_property
    def client_a(self) -> ClientA:
        return ClientA(arg1, arg2)

    @property
    def new_client_b(self) -> ClientB:
        return ClientB(arg1, arg2)
```
* Approach 2: plain properties with the client being initialized on startup (alternatives: you may define a traditional class with an `__init__` method or set `default_factory` for the `dataclass` fields)

```python
@dataclass
class Context:
    client_b: ClientB
    client_a: ClientA


new_context = Context(
    client_a=ClientA(arg1, arg2)
    client_b=ClientB(arg1, arg2)
)
```
## What do I call generic lazy evaluation?

Python already does some lazy evaluation mainly for iterative items/methods.
e.g: range, zip and map builtin methods.

Python also supports "lazy imports", allowing you to make local imports, which has some very particular uses.

What I have not found, is a generic and easy way to tell Python to lazily evaluate an object instance or context.

## Basic example with desired behavior
Following is a generic example for the desired basic behavior with class/instances:
```python
# creating objects with lazy evaluation will not initialize its instances
# there should be explicit typing for lazy evaluated class/objects
client_a: Lazy | ClientA = Lazy(ClientA, arg1, arg2),
client_b: Lazy | ClientB = Lazy(ClientB, arg3, arg4)
client_c: Lazy | ClientC = Lazy(ClientC, arg5, arg6)
# accessing attributes should initialize the instance 
client_a.foo  # initializes ClientA and returns foo attribute
# calling methods should also initialize the instance
client_b.bar()  # initializes ClientB, call bar method and return value
# Non initialized instances should be/access Lazy instances
print(client_c)  # should call and print Lazy object __repr__
# Initialized instances should access/get proper object instances
client_c.do_something()  # initializes ClientC, call do_something method and return value
print(client_c)  # should call and print ClientC object __repr__
```

## Why do I want it?

I believe that a generic lazy evaluation would enable me to write a solution with the best of both common solutions I provided above.

An example with my Lazilypy module would be:
```python
@dataclass
class Context:
    client_b: ClientB
    client_a: ClientA


new_context = Context(
    client_a=Lazy(ClientA, arg1, arg2),
    client_b=Lazy(ClientB, arg1, arg2)
)
```

I like this approach better because it has the following advantages:
- simple dataclass definition, with little to no advanced syntax
- instantiation of clients and credential lookup would only happen if and when necessary
- no need to wait for each provider to support/implement the feature on their own
- it can support many quality of life improvements that usually require large frameworks
