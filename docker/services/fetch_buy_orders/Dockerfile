FROM fetch_buy_orders_base:001
WORKDIR /xapo
COPY codebase/ ./codebase/
WORKDIR /xapo/codebase/
CMD ["python", "fetch_buy_orders_service.py"]