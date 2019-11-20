# stdlogpj
python logging done my way

home: https://github.com/prjemian/stdlogpj

INSTALL

    pip install stdlogpj

USAGE:

    import stdlogpj
    logger = stdlogpj.standard_logging_setup("demo")
    logger.info("hello")

DEMO:

```python
#!/usr/bin/env python

import stdlogpj

logger = stdlogpj.standard_logging_setup("stdlogpj-demo")


def thing1(i):
    logger.info(f"something #{i+1}")


def main():
    logger.info("hello")
    for i in range(5):
        logger.debug("calling thing1()")
        thing1(i)
    logger.critical("complete")


if __name__ == "__main__":
    logger.warning("before main()")
    main()
    logger.error("after main(): no error, really")
```

## basic use

    logger = stdlogpj.standard_logging_setup("basic")

This creates a `./.logs/basic.log` file (creating the `.logs` 
subdirectory if it does not already exist) for any output from `logger`.

## directing logs to a specific directory

```
In [1]: import stdlogpj                                                                                                                                    

In [2]: logger = stdlogpj.standard_logging_setup("demo", log_path="/tmp/example_logs")                                                                     

In [3]: logger.debug("debug message")                                                                                                                      
D Wed-12:53:33 - debug message

In [4]: logger.info("info message")                                                                                                                        
I Wed-12:53:46 - info message

In [5]: logger.warning("warning message")                                                                                                                  
W Wed-12:53:54 - warning message

In [6]: logger.error("error message")                                                                                                                      
E Wed-12:54:02 - error message

In [7]: logger.critical("critical message")                                                                                                                
C Wed-12:54:16 - critical message

In [8]: !cat /tmp/example_logs/demo.log                                                                                                                    
|2019-11-20 12:53:33.890|DEBUG|18481|demo|<ipython-input-3-5e52fde1a181>|1|MainThread| - debug message
|2019-11-20 12:53:46.536|INFO|18481|demo|<ipython-input-4-0abdaa03b9ae>|1|MainThread| - info message
|2019-11-20 12:53:54.853|WARNING|18481|demo|<ipython-input-5-3a3eb9909f33>|1|MainThread| - warning message
|2019-11-20 12:54:02.405|ERROR|18481|demo|<ipython-input-6-ac0de87faf7f>|1|MainThread| - error message
|2019-11-20 12:54:16.537|CRITICAL|18481|demo|<ipython-input-7-0babbd2c824b>|1|MainThread| - critical message
```

## Rotate files and limit size

Using features of the [*RotatingFileHandler*](https://docs.python.org/3/library/logging.handlers.html?highlight=rotatingfilehandler#logging.handlers.RotatingFileHandler), 
it is possible to limit the size of the files by switching to a new log file,
saving the old log file(s) by appending a number.  Lower numbers are more recent.

Use this instead to limit logs to 1 MB and no more than 5 numbered (previous) log files:

```
logger = stdlogpj.standard_logging_setup("stdlogpj-demo", maxBytes=1024*1024, backupCount=5)
```
