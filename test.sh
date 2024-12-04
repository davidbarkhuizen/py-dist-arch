clear

cd codebase \
    && export CREATE_BUY_ORDER_PROTOCOL='http' \
    && export CREATE_BUY_ORDER_HOST='localhost' \
    && export CREATE_BUY_ORDER_PORT='8777' \
    && export CREATE_BUY_ORDER_PATH='/buy_order' \
    && export FETCH_BUY_ORDERS_PROTOCOL='http' \
    && export FETCH_BUY_ORDERS_HOST='localhost' \
    && export FETCH_BUY_ORDERS_PORT='8778' \
    && export FETCH_BUY_ORDERS_PATH='/buy_orders' \
    && python3 -m unittest discover -s test --pattern=*.py --verbose

cd ..