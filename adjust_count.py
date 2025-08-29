from consumer import run_consumer
from producer import run_producer

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def adjust_count(topic, col, key, ammount=-1):

    items = run_consumer(topic)

    quantity = items[key][col]
    if quantity > 0:
        items[key][col] = quantity + ammount
        logger.info(
            f"Decremented {items[key]}. New inventory: {items[key][col]}")
    else:
        logger.warning(
            f"Inventory for {items[key]} is already zero. Cannot decrement.")

    run_producer(topic, items)


if __name__ == "__main__":
    adjust_count("inventory", "inventory", "A1")
    # adjust_count("bank", "count", "$1", -1)
