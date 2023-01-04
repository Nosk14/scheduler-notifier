from tasks import dtc_new_cards
import schedule
import logging
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


if __name__ == '__main__':
    logging.info("Scheduler started!")
    while True:
        schedule.run_pending()
        time.sleep(5)
