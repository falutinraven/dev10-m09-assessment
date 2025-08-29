from consumer import run_consumer
from producer import run_producer

import logging
logging.basicConfig(level=logging.WARNING)
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


def zero_all_currency():
    items = run_consumer("bank")

    for currency in items["bank"].keys():
        items["bank"][currency] = 0

    run_producer("bank", items)
