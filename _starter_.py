#!/usr/bin/env python

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import stdlogpj.stdlog as stdlogpj

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
