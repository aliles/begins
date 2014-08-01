==========================
A short tutorial on begins
==========================

The purpose of *begins* is
to help you to easily create
command line applications without
distracting you from the
purpose of you application.
Let's create an
application together to
demonstrate some of the
features of *begins*.
Our application will
generate a series of
famous Monty Python quotes.

First we will create a
minimal structure for our
application.::

    import begin
    @begin.start
    def run():
        "Monty Python quotes for all"

This application will run.
It doesn't need any ``__name__ == "__main__"`` magic.
It even has help output when it's
run with the ``-h`` flag.

Now lets make it do
something more interesting.::

    import begin
    @begin.start
    def run(name='Arthur', quest='Holy Grail', colour='blue', *knights):
        "Monty Python quotes for all"

Now our application accepts
three command line flags and
zero or more positional arguments.
The command line flags all
have default values that
can be over ridden.

Currently all these options relate
to different Monty Python quotes.
Let us separate these into
separate sub-commands.::

    import begin
    @begin.subcommand
    def name(answer):
        "What is your name?"
    
    @begin.subcommand
    def quest(answer):
        "What is your quest?"
    
    @begin.subcommand
    def colour(answer):
        "What is your favourite colour?"
    
    @begin.start
    def run():
        pass

Now our application has
three sub-commands that require
exactly one positional argument.
However, you may have noticed
there is currently no output.
We will change that now.
One way to fix this is
to use ``print`` statements
``print()`` functions.
We are not going to do that.
Instead, we are going to
configure logging.::

    import begin
    import logging

    @begin.subcommand
    def name(answer):
        "What is your name?"
        logging.info(answer)
    
    @begin.subcommand
    def quest(answer):
        "What is your quest?"
        logging.info(answer)
    
    @begin.subcommand
    def colour(answer):
        "What is your favourite colour?"
        logging.info(answer)
    
    @begin.start
    @begin.logging
    def run():
        pass

Now our application does
something useful.
But, it can only answer
one question at a time.
We can ask *begins* to
accept multiple subcommands
using a separator.
We will ignore the
sub-command definitions for brevity.::

    # Sub-commands not shown for brevity.

    @begin.start(cmd_delim='--')
    @begin.logging
    def run():
        pass

Lastly, let us create
a new sub-command that
takes a number instead of
a string.::

    @begin.subcommand
    @begin.convert(speed=int)
    def swallows(speed):
        "What is the wing speed of an unladden swallow?"
        logging.info("%d mph", speed)

You may have noticed the
introduction of the
``begin.convert`` decorator.
If the sub-command was not
decorated in this way the
``speed`` argument would
be a string.
This would cause the
sub-command to fail.
The ``begin.convert`` decorator
ensures that the ``speed``
argument will be converted
to an integer first.

This is the end for
this little tutorial.
To learn more about
*begins* you can continue
reading with the user :ref:`guide`.
