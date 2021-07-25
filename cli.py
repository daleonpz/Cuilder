from FromNothing.__main__ import main
import logging

if __name__ == '__main__':
    # create logger
    logger = logging.getLogger('FromNothing')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    main()

